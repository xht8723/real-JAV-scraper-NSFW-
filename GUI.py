from PySide6.QtWidgets import (QApplication, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy, QTableView, QTextBrowser, 
    QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox)
from PySide6.QtCore import Qt, QMetaObject, QCoreApplication, QRect

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        main_layout = QHBoxLayout(self.centralwidget)
        
        # Left side layout
        left_layout = QVBoxLayout()
        pic_layout = QHBoxLayout()
        pic_layout.setAlignment(Qt.AlignLeft)
        
        self.processList = QTableView(self.centralwidget)
        self.processList.setObjectName("processList")
        self.processList.setGeometry(QRect(20, 20, 421, 421))
        left_layout.addWidget(self.processList)
        
        self.util_box = QGroupBox("Other utilities")
        self.util_box.setObjectName("util_box")
        util_layout = QHBoxLayout(self.util_box)

        self.HDlinkBt = QPushButton("Hardlinks")
        self.HDlinkBt.setObjectName("Hardlinks")
        self.HDlinkBt.setToolTip("Create hardlinks for all files in the directory to target directory")
        util_layout.addWidget(self.HDlinkBt)
        self.renameBt = QPushButton("Rename subtitles")
        self.renameBt.setObjectName("Rename subtitles")
        self.renameBt.setToolTip("Rename subtitles to match the movie file names. (Sort alphabetically)")
        util_layout.addWidget(self.renameBt)
        left_layout.addWidget(self.util_box)

        self.info = QLabel(self.centralwidget)
        self.info.setObjectName("info")
        self.info.setWordWrap(True)
        self.info.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.info)

        self.leftPicture = QLabel()
        self.leftPicture.setObjectName(u"leftPicture")
        #self.leftPicture.setGeometry(QRect(10, 510, 100, 100))
        self.leftPicture.setScaledContents(True)
        self.leftPicture.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.leftPicture.setAlignment(Qt.AlignLeft)
        self.leftPicture.setMaximumSize(50, 50)
        pic_layout.addWidget(self.leftPicture)

        self.rightPicture = QLabel()
        self.rightPicture.setObjectName(u"rightPicture")
        #self.rightPicture.setGeometry(QRect(331, 510, 100, 100))
        self.rightPicture.setScaledContents(True)
        self.rightPicture.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rightPicture.setAlignment(Qt.AlignLeft)
        self.rightPicture.setMaximumSize(50, 50)
        pic_layout.addWidget(self.rightPicture)

        self.info.setGeometry(QRect(120, 510, 201, 100))
        left_layout.addLayout(pic_layout)


        # Right side layout
        right_layout = QVBoxLayout()
        
        self.groupBox = QGroupBox("Select Directory:")
        self.groupBox.setObjectName("groupBox")
        group_layout = QGridLayout(self.groupBox)
        
        self.Dir = QLineEdit()
        self.Dir.setObjectName("Dir")
        self.Dir.setAlignment(Qt.AlignCenter)
        group_layout.addWidget(self.Dir, 0, 0)
        
        self.directoryBt = QToolButton()
        self.directoryBt.setObjectName("directoryBt")
        self.directoryBt.setText("...")
        group_layout.addWidget(self.directoryBt, 0, 1)
        
        self.isHeadlessCheckbox = QCheckBox("Headless Mode")
        self.isHeadlessCheckbox.setObjectName("isHeadlessCheckbox")
        self.isHeadlessCheckbox.setToolTip("Hide browser window")
        #group_layout.addWidget(self.isHeadlessCheckbox, 1, 0, 1, 2)

        self.folderNameCheckbox = QCheckBox("Use code only as folder name")
        self.folderNameCheckbox.setObjectName("codeAsFolderNameCheckbox")
        self.folderNameCheckbox.setToolTip("'yyy-xxx' will be used as folder name instead of 'yyy-xxx[Studio][Title][Year]'")
        group_layout.addWidget(self.folderNameCheckbox, 4, 0, 1, 2)
        
        self.startBt = QPushButton("Start scrapping")
        self.startBt.setObjectName("startBt")
        group_layout.addWidget(self.startBt, 2, 0, 1, 2)

        self.actressSearch = QPushButton("Format actress names")
        self.actressSearch.setObjectName("actressSearch")
        self.actressSearch.setToolTip("Will search for exsisting actress names online for JP/CN/EN names, adjust NFO files to make actress appear as same person in Jellyfin")
        group_layout.addWidget(self.actressSearch, 3, 0, 1, 2)
        
        right_layout.addWidget(self.groupBox)
        
        self.logs = QTextBrowser()
        self.logs.setObjectName("logs")
        right_layout.addWidget(self.logs)
        
        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Real JAV Scrapper")
        self.startBt.setText("Start")
        self.actressSearch.setText("Format actress names")
        self.directoryBt.setText("...")
        self.info.setText("Please consider supporting me!  :D")
        self.isHeadlessCheckbox.setText("Headless Mode")
        self.folderNameCheckbox.setText("Simple folder name(AV code only)")


class hardlinkWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hardlinks")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        # Main layout
        main_layout = QHBoxLayout(self.centralwidget)
        
        # Left side layout
        left_layout = QVBoxLayout()
        pic_layout = QHBoxLayout()
        pic_layout.setAlignment(Qt.AlignLeft)
        
        self.processList = QTableView(self.centralwidget)
        self.processList.setObjectName("processList")
        left_layout.addWidget(self.processList)

        # Right side layout
        right_layout = QVBoxLayout()
        
        self.groupBox = QGroupBox("Select source directory:")
        self.groupBox.setObjectName("groupBox")
        group_layout = QGridLayout(self.groupBox)
        
        self.sourceDir = QLineEdit()
        self.sourceDir.setObjectName("sourceDir")
        self.sourceDir.setAlignment(Qt.AlignCenter)
        group_layout.addWidget(self.sourceDir, 0, 0)
        
        self.sourcedirectoryBt = QToolButton()
        self.sourcedirectoryBt.setObjectName("directoryBt")
        self.sourcedirectoryBt.setText("...")
        group_layout.addWidget(self.sourcedirectoryBt, 0, 1)

        self.groupBox2 = QGroupBox("Select target directory:")
        self.groupBox2.setObjectName("groupBox2")
        group_layout = QGridLayout(self.groupBox2)

        self.targetDir = QLineEdit()
        self.targetDir.setObjectName("targetDir")
        self.targetDir.setAlignment(Qt.AlignCenter)
        group_layout.addWidget(self.targetDir, 0, 0)

        self.targetdirectoryBt = QToolButton()
        self.targetdirectoryBt.setObjectName("directoryBt")
        self.targetdirectoryBt.setText("...")
        group_layout.addWidget(self.targetdirectoryBt, 0, 1)
        
        self.startBt = QPushButton("Make Hardlinks")
        self.startBt.setObjectName("HDstartBt")
        right_layout.addWidget(self.groupBox)
        right_layout.addWidget(self.groupBox2)
        right_layout.addWidget(self.startBt)

        self.logs = QTextBrowser()
        self.logs.setObjectName("logs")
        right_layout.addWidget(self.logs)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        
        self.setCentralWidget(self.centralwidget)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Hardlinks")

class renameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("rename subtitles")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        # Main layout
        main_layout = QHBoxLayout(self.centralwidget)
        
        # Left side layout
        left_layout = QVBoxLayout()
        pic_layout = QHBoxLayout()
        pic_layout.setAlignment(Qt.AlignLeft)
        
        self.processList = QTableView(self.centralwidget)
        self.processList.setObjectName("processList")
        left_layout.addWidget(self.processList)

        self.confirmBt = QPushButton("Confirm above changes")
        self.confirmBt.setObjectName("confirmBt")
        left_layout.addWidget(self.confirmBt)

        # Right side layout
        right_layout = QVBoxLayout()
        
        self.groupBox = QGroupBox("Select Directory:")
        self.groupBox.setObjectName("groupBox")
        group_layout = QGridLayout(self.groupBox)
        
        self.Dir = QLineEdit()
        self.Dir.setObjectName("Dir")
        self.Dir.setAlignment(Qt.AlignCenter)
        group_layout.addWidget(self.Dir, 0, 0)
        
        self.directoryBt = QToolButton()
        self.directoryBt.setObjectName("directoryBt")
        self.directoryBt.setText("...")
        group_layout.addWidget(self.directoryBt, 0, 1)
        
        self.startBt = QPushButton("List subtitles")
        self.startBt.setObjectName("RenameBt")
        group_layout.addWidget(self.startBt, 2, 0, 1, 2)
        
        right_layout.addWidget(self.groupBox)
        
        self.logs = QTextBrowser()
        self.logs.setObjectName("logs")
        right_layout.addWidget(self.logs)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        
        self.setCentralWidget(self.centralwidget)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Rename subtitles")