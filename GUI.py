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
        
        self.startBt = QPushButton("Start scrapping")
        self.startBt.setObjectName("startBt")
        group_layout.addWidget(self.startBt, 2, 0, 1, 2)

        self.actressSearch = QPushButton("Format actress names")
        self.actressSearch.setObjectName("actressSearch")
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
