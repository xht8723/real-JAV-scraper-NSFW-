import sys
import os
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtGui import QPixmap
from GUI import Ui_MainWindow
import rename
import hardlink
import scraper
import gfmerger
import util as ut

class LogSignal(QObject):
    """Signal for updating GUI logs"""
    update = Signal(str, str)

class UpdateTableSignal(QObject):
    """Signal for updating GUI table"""
    update = Signal(str, str)

#-----------------------------------------------------
# Main Window class that sets up the GUI and handles events
#-----------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_connections()
        self.log_signal = LogSignal()
        self.log_signal.update.connect(self.update_logs)
        self.init_table_model()
        self.set_pictures(resource_path('./img/alipay.png') , resource_path('./img/paypal.png'))
        self.table_update_signal = UpdateTableSignal()
        self.table_update_signal.update.connect(self.update_table)

    def set_pictures(self, left_image_path, right_image_path):
        left_pixmap = QPixmap(left_image_path)
        right_pixmap = QPixmap(right_image_path)
        self.ui.leftPicture.setPixmap(left_pixmap)
        self.ui.rightPicture.setPixmap(right_pixmap)

    def init_table_model(self):
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(['Original name', 'New name'])
        self.ui.processList.setModel(self.table_model)
        self.ui.processList.horizontalHeader().setStretchLastSection(True)

    def setup_connections(self):
        self.ui.startBt.clicked.connect(self.run_scraper)
        self.ui.actressSearch.clicked.connect(self.run_gfmerger)
        self.ui.directoryBt.clicked.connect(self.select_directory)
        self.ui.renameBt.clicked.connect(self.rename_subtitle_UI)
        self.ui.HDlinkBt.clicked.connect(self.hardlink_UI)

    def rename_subtitle_UI(self):
        self.rename_window = rename.renameWindow()
        self.rename_window.show()

    def hardlink_UI(self):
        self.hardlink_window = hardlink.hardlinkWindow()
        self.hardlink_window.show()

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.ui.Dir.setText(directory)

    def run_scraper(self):
        directory = self.ui.Dir.text()
        if not directory:
            self.update_logs("Please select a directory first.\n")
            return

        self.ui.logs.clear()
        self.table_model.removeRows(0, self.table_model.rowCount())
        self.ui.startBt.setEnabled(False)
        threading.Thread(target=self.scraper_thread, args=(directory,), daemon=True).start()

    def run_gfmerger(self):
        directory = self.ui.Dir.text()
        if not directory:
            self.update_logs("Please select a directory first.\n")
            return
        
        self.ui.logs.clear()
        self.table_model.removeRows(0, self.table_model.rowCount())
        self.ui.actressSearch.setEnabled(False)
        threading.Thread(target=self.gfmerger_thread, args=(directory,), daemon=True).start()

#-----------------------------------------------------
# Run scraper thread once button pressed.
# Scapes javguru and then javtrailers for metadata.
#-----------------------------------------------------
    def scraper_thread(self, directory, isheadless=False):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)

        def update_table(original_filename, new_folder_name):
            self.table_update_signal.update.emit(original_filename, new_folder_name)

        log_callback("\nStarting processing files...\n", "black")
        cached_NFO = ut.readJson("NFO.json")
        renameType = self.ui.folderNameCheckbox.isChecked()
        missing = [] # Stores entry for every failed javguru search
        banngoTuple = ut.findAVIn(directory, log_callback=log_callback, update_callback=update_table)
        driver = ut.startChrome("https://jav.guru/", log_callback=log_callback, isheadless=isheadless)
        for eachBanngo in banngoTuple[0]:
            ogfile = banngoTuple[1][eachBanngo]
            try:
                data = scraper.processSearchJavguru(driver, eachBanngo, ogfile, cached_NFO, log_callback=log_callback)
                ut.cdp_close_ad_tab(driver, log_callback=log_callback) # Close ad tab if it opens
            except Exception as e:
                error_type = type(e).__name__
                log_callback(f"Error: [{error_type}]{str(e)} occurred while searching {eachBanngo}\n", "red")
                log_callback(f"\n", "black")
                continue
            if data == None:
                missing.append(eachBanngo)
                log_callback(f"Failed to get search results for {eachBanngo} \n", "orange")
                log_callback(f"\n", "black")
                continue
            try:
                ut.manageFileStucture(directory, renameType, data, log_callback=log_callback, update_callback=update_table)
                log_callback(f"Processed: {data['Code']}\n")
            except Exception as e:
                error_type = type(e).__name__
                log_callback(f"Error: [{error_type}]{str(e)} occurred while processing {data['Title']}\n", "red")
                log_callback(f"\n", "black")
                continue
        ut.writeJson(cached_NFO, "NFO.json")


        if len(missing) > 0: # Stores entry for every failed javguru search
            cached_NFO = ut.readJson("NFO.json")
            ut.cdp_gotoURL(driver, "https://javtrailers.com/", log_callback=log_callback)
            for eachBanngo in missing:
                ogfile = banngoTuple[1][eachBanngo]
                try:
                    data = scraper.processSearchJavtrailers(driver, eachBanngo, ogfile, cached_NFO, log_callback=log_callback)
                except Exception as e:
                    error_type = type(e).__name__
                    log_callback(f"Error: [{error_type}]{str(e)} occurred while searching {eachBanngo}\n", "red")
                    log_callback(f"\n", "black")
                    continue
                if data == None:
                    log_callback(f"Failed to get search results for {eachBanngo}\n", "orange")
                    log_callback(f"\n", "black")
                    continue
                try:
                    ut.manageFileStucture(directory, renameType, data, log_callback=log_callback, update_callback=update_table)
                    log_callback(f"Processed: {data['Code']}\n")
                except Exception as e:
                    error_type = type(e).__name__
                    log_callback(f"Error: [{error_type}]{str(e)} occurred while processing {data['Title']}\n", "red")
                    log_callback(f"\n", "black")
                    continue

        ut.writeJson(cached_NFO, "NFO.json")
        self.ui.startBt.setEnabled(True)
        driver.quit()
        log_callback("\nFinished processing all files!\n", "green")
        log_callback(f"\n", "black")
        
#-----------------------------------------------------
# Run gfmerger thread once button pressed.
# Scapes javmodel and then javguru to format actress names under same language.
#-----------------------------------------------------
    def gfmerger_thread(self, directory, isheadless=False):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)

        def update_table(original_filename, new_folder_name):
            self.table_update_signal.update.emit(original_filename, new_folder_name)

        log_callback("\nStarting modifying names...\n", "black")
        
        cached_names = ut.readJson("names.json")
        missing = []

        try:
            Local_actors = gfmerger.searchNFO(directory, log_callback=log_callback, update_callback=update_table)
            for actor in list(Local_actors.keys()):
                if actor in cached_names:
                    gfmerger.modifyNFO(Local_actors, actor, cached_names[actor], log_callback=log_callback, update_callback=update_table)
                    log_callback(f"Adding multi Names: {cached_names[actor]}\n")
                    del Local_actors[actor]
        except Exception as e:
            error_type = type(e).__name__
            log_callback(f"Error: [{error_type}]{str(e)}\n", "red")
            log_callback(f"\n", "black")


        driver = ut.startChrome("https://javmodel.com/",log_callback=log_callback, isheadless=isheadless)
        for actor in Local_actors:
            try:
                names = gfmerger.processSearch(driver, actor, cached_names, log_callback=log_callback)
                if names == None:
                    log_callback(f"Failed to get search results for {actor}\n", "orange")
                    log_callback(f"\n", "black")
                    missing.append(actor)
                    continue
                gfmerger.modifyNFO(Local_actors, actor, names, log_callback=log_callback, update_callback=update_table)
                log_callback(f"Adding multi Names: {names}\n")
            except Exception as e:
                error_type = type(e).__name__
                log_callback(f"Error: [{error_type}]{str(e)}\n", "red")
                log_callback(f"\n", "black")
                missing.append(actor)
                continue

        cached_names = ut.formatnameJson(cached_names)
        ut.writeJson(cached_names, "names.json")

        if len(missing) > 0:
            ut.cdp_gotoURL(driver, "https://jav.guru/jav-actress-list/", log_callback=log_callback)
            cached_names = ut.readJson("names.json")
            for actor in missing:
                try:
                    names = gfmerger.processSearchJavguru(driver, actor, cached_names, log_callback=log_callback)
                    if names == None:
                        log_callback(f"Failed to get search results for {actor}\n", "orange")
                        log_callback(f"\n", "black")
                        continue
                    gfmerger.modifyNFO(Local_actors, actor, names, log_callback=log_callback, update_callback=update_table)
                    log_callback(f"Adding multi Names: {names}\n")
                except Exception as e:
                    error_type = type(e).__name__
                    log_callback(f"Error: [{error_type}]{str(e)}\n", "red")
                    log_callback(f"\n", "black")
                    continue

            cached_names = ut.formatnameJson(cached_names)
            ut.writeJson(cached_names, "names.json")

        driver.quit()
        self.ui.actressSearch.setEnabled(True)
        log_callback("\nFinished modifying names!\n", "green")
        log_callback(f"\n", "black")

    def update_logs(self, message, color = "black"):
        if color != "black":
            message = f'<span style="color:{color};">{message}</span>'
        self.ui.logs.append(message)

    def update_table(self, original_filename, new_folder_name):
        if new_folder_name:
            for row in range(self.table_model.rowCount()):
                if self.table_model.item(row, 0).text() == original_filename:
                    self.table_model.setItem(row, 1, QStandardItem(new_folder_name))
                    break
        else:
            row = self.table_model.rowCount()
            self.table_model.insertRow(row)
            self.table_model.setItem(row, 0, QStandardItem(original_filename))

#-----------------------------------------------------
# Resource path for pyinstaller
#-----------------------------------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#-----------------------------------------------------
# Main function
#-----------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

