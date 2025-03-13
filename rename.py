from GUI import renameWindow
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QHeaderView
import os
import threading

class renameWindow(renameWindow):
    class LogSignal(QObject):
        """Signal for updating GUI logs"""
        update = Signal(str, str)

    class UpdateTableSignal(QObject):
        """Signal for updating GUI table"""
        update = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rename Subtitle")
        self.init_table_model()
        self.directoryBt.clicked.connect(self.select_dir)
        self.startBt.clicked.connect(self.run_rename)
        self.confirmBt.clicked.connect(self.run_confirm)
        self.confirmBt.setEnabled(False)
        self.log_signal = self.LogSignal()
        self.log_signal.update.connect(self.update_logs)
        self.table_update_signal = self.UpdateTableSignal()
        self.table_update_signal.update.connect(self.update_table)
        
    def select_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir:
            self.Dir.setText(dir)

    def init_table_model(self):
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(['Original name', '--> New name'])
        self.processList.setModel(self.table_model)
        header = self.processList.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    
    def update_logs(self, message, color = "black"):
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

    def run_rename(self):
        dir = self.Dir.text()
        if not dir:
            self.update_logs("Please select a directory", "red")
            return
        self.logs.clear()
        self.table_model.removeRows(0, self.table_model.rowCount())
        self.startBt.setEnabled(False)
        threading.Thread(target=self.rename_update_table, args=(dir,), daemon=True).start()

    def rename_update_table(self, dir):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)

        def update_table(original_filename, new_folder_name):
            self.table_update_signal.update.emit(original_filename, new_folder_name)

        movie_format = [
        'mp4',
        'MP4',
        'mkv',
        'rmvb',
        'AVI',
        'avi'
        ]

        subtitle_format = [
        'srt',
        'ass',
        'SRT',
        'ASS'
        ]

        try:
            file_list = os.listdir(dir)
            movie_file = []
            subtitle_file = []
            for file in file_list:
                _, extention = os.path.splitext(file)
                extention = extention[1:]  # Remove the dot from the extension
                if extention in movie_format:
                    movie_file.append(file)
                    if log_callback:
                        log_callback(f"Found movie: {file}\n")
                if extention in subtitle_format:
                    subtitle_file.append(file)
                    if log_callback:
                        log_callback(f"Found movie: {file}\n")
                    if update_table:
                        update_table(f"{file}", None)

            movie_file.sort()
            subtitle_file.sort()
            for movie, subtitle in zip(movie_file, subtitle_file):
                moviename, _ = os.path.splitext(movie)
                subtitlename, extention = os.path.splitext(subtitle)
                new_subname = moviename + extention
                if update_table:
                    update_table(subtitle, new_subname)
        except Exception as e:
            if log_callback:
                log_callback(f"Error: {str(e)}", "red")
                log_callback("", "black")
        
        self.confirmBt.setEnabled(True)
        self.startBt.setEnabled(True)
        if log_callback:
            log_callback("Listed all subtitle changes on the left.", 'green')
            log_callback("Press confirm button to actual rename the files.\n", 'green') 
            log_callback("", "black")

    def run_confirm(self):
        table_entries = {}
        try:
            for row in range(self.table_model.rowCount()):
                original_filename = self.table_model.item(row, 0).text()
                new_folder_name = self.table_model.item(row, 1).text() if self.table_model.item(row, 1) else None
                table_entries[original_filename] = new_folder_name
        except Exception as e:
            self.update_logs(f"Error: {str(e)}", "red")
            self.update_logs("","black")
        
        self.confirmBt.setEnabled(False)
        self.startBt.setEnabled(False)
        threading.Thread(target=self.rename_excute, args=(table_entries,), daemon=True).start()

    def rename_excute(self, dict):
        def log_callback(message, color="black"):
            self.log_signal.update.emit(message, color)

        try:
            for key, value in dict.items():
                if value:
                    os.rename(os.path.join(self.Dir.text(), key), os.path.join(self.Dir.text(), value))
                    if log_callback:
                        log_callback(f"Renamed {key} to {value}\n")
                else:
                    if log_callback:
                        log_callback(f"Skipped {key}\n")
                    continue
        except Exception as e:
            if log_callback:
                log_callback(f"Error: {str(e)}\n", "red")
                log_callback("", "black")

        self.startBt.setEnabled(True)
        if log_callback:
            log_callback("Finished renaming all subtitles!\n", "green")
            log_callback("", "black")

