import sys
import os
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from GUI import Ui_MainWindow
import scraper
import gfmerger

class LogSignal(QObject):
    update = Signal(str, str)

class UpdateTableSignal(QObject):
    update = Signal(str, str)

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
        self.table_model.setHorizontalHeaderLabels(['Original', '--> New'])
        self.ui.processList.setModel(self.table_model)
        self.ui.processList.horizontalHeader().setStretchLastSection(True)

    def setup_connections(self):
        self.ui.startBt.clicked.connect(self.run_scraper)
        self.ui.actressSearch.clicked.connect(self.run_gfmerger)
        self.ui.directoryBt.clicked.connect(self.select_directory)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.ui.Dir.setText(directory)

    def run_scraper(self):
        isheadless = self.ui.isHeadlessCheckbox.isChecked()
        directory = self.ui.Dir.text()
        if not directory:
            self.update_logs("Please select a directory first.\n")
            return

        self.ui.logs.clear()
        self.ui.startBt.setEnabled(False)
        threading.Thread(target=self.scraper_thread, args=(directory, isheadless), daemon=True).start()

    def run_gfmerger(self):
        isheadless = self.ui.isHeadlessCheckbox.isChecked()
        directory = self.ui.Dir.text()
        if not directory:
            self.update_logs("Please select a directory first.\n")
            return
        
        self.ui.logs.clear()
        self.ui.actressSearch.setEnabled(False)
        threading.Thread(target=self.gfmerger_thread, args=(directory, isheadless), daemon=True).start()

    def scraper_thread(self, directory, isheadless=False):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)

        def update_table(original_filename, new_folder_name):
            self.table_update_signal.update.emit(original_filename, new_folder_name)

        try:
            scraper.findAVIn(directory, log_callback=log_callback, update_callback=update_table)

            driver = scraper.startFirefox(log_callback=log_callback, isheadless=isheadless)
            metadataList = scraper.processSearch(driver, directory, log_callback=log_callback)

            for metadata in metadataList:
                data = scraper.parseInfo(metadata, log_callback=log_callback)
                try:
                    scraper.manageFileStucture(directory, data, log_callback=log_callback, update_callback=update_table)
                    log_callback(f"Processed: {data['Code']}\n")
                except Exception as e:
                    log_callback(f"Error: {str(e)} occurred while processing {data['Title']}\n")
            
            log_callback("\nFinished processing all files!\n", "green")
            self.ui.startBt.setEnabled(True)
            driver.quit()
        except Exception as e:
            log_callback(f"Error: {str(e)}\n", "red")
        finally:
            driver.quit()
            self.ui.startBt.setEnabled(True)
    
    def gfmerger_thread(self, directory, isheadless=False):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)
        
        try:
            Local_actors = gfmerger.searchNFO(directory, log_callback=log_callback)
            driver = gfmerger.startFirefox(log_callback=log_callback, isheadless=isheadless)
            for actor in Local_actors:
                innerHTML = gfmerger.processSearch(driver, actor, log_callback=log_callback)
                if innerHTML == None:
                    log_callback(f"Failed to get search results for {actor}\n", "orange")
                    continue
                names = gfmerger.processCardInfo(innerHTML, log_callback=log_callback)
                gfmerger.modifyNFO(Local_actors, actor, names, log_callback=log_callback)
                log_callback(f"Adding multi Names: {names}\n")
            log_callback("\nFinished modifying names!\n", "green")
            self.ui.actressSearch.setEnabled(True)
            driver.quit()
        except Exception as e:
            log_callback(f"Error: {str(e)}\n", "red")
        finally:
            driver.quit()
            self.ui.actressSearch.setEnabled(True)
            


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
        self.ui.processList.scrollToBottom()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

