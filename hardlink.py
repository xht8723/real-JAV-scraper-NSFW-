from GUI import hardlinkWindow
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QHeaderView
import os
import threading


class hardlinkWindow(hardlinkWindow):
    class LogSignal(QObject):
        """Signal for updating GUI logs"""
        update = Signal(str, str)

    class UpdateTableSignal(QObject):
        """Signal for updating GUI table"""
        update = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hardlinks")
        self.init_table_model()
        self.sourcedirectoryBt.clicked.connect(self.select_sourcedir)
        self.targetdirectoryBt.clicked.connect(self.select_targetdir)
        self.startBt.clicked.connect(self.run_hardlink)
        self.log_signal = self.LogSignal()
        self.log_signal.update.connect(self.update_logs)
        self.table_update_signal = self.UpdateTableSignal()
        self.table_update_signal.update.connect(self.update_table)

    def select_sourcedir(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir:
            self.sourceDir.setText(dir)
    
    def select_targetdir(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir:
            self.targetDir.setText(dir)

    def init_table_model(self):
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(['Original file path', '--> Hardlink path'])
        self.processList.setModel(self.table_model)
        header = self.processList.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def update_logs(self, message, color="black"):
        if color != "black":
            message = f'<span style="color:{color};">{message}</span>'
        self.logs.append(message)

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

    def run_hardlink(self):
        sourcedir = self.sourceDir.text()
        targetdir = self.targetDir.text()
        if not sourcedir:
            self.update_logs("Please select directory", "red")
            self.update_logs("", "black")
            return
        if not targetdir:
            targetdir = sourcedir

        self.logs.clear()
        self.table_model.removeRows(0, self.table_model.rowCount())
        self.startBt.setEnabled(False)
        threading.Thread(target=self.hardlink, args=(sourcedir, targetdir,), daemon=True).start()

    def hardlink(self, sourcedir, targetdir):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)
        def update_table(original_filename, new_folder_name):
            self.table_update_signal.update.emit(original_filename, new_folder_name)

        for file in os.listdir(sourcedir):
            source = os.path.join(sourcedir, file)
            newname = "(hardlink) " + file
            target = os.path.join(targetdir, newname)
            if os.path.isfile(source):
                try:
                    os.link(source, target)
                    update_table(source, None)
                    update_table(source, target)
                    log_callback(f"Hardlinked {source} to {target}\n")
                except Exception as e:
                    log_callback(f"Error: {str(e)}\n", "red")
                    log_callback("", "black")
            else:
                log_callback(f"Skipped {source} (not a file)\n", "orange")
                log_callback("", "black")
        self.startBt.setEnabled(True)
        if log_callback:
            log_callback("Finished making hardlinks!", "green")
            log_callback("","black")