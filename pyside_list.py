import json
import sys
import faulthandler
faulthandler.enable()

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Efficient Grocery List Generator")

        self.stacklayout = QStackedLayout()
        
        self.main_menu_tab()    #stack index0
        self.register_tab()     #stack index1
        self.list_tab()         #stack index2

        widget = QWidget()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)

    def main_menu_tab(self):
        main_menu_layout = QVBoxLayout()
        
        toolbar = QToolBar("Store Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        main_menu_layout.addToolBar(toolbar)
        
        register_btn = QPushButton("Register a Store")
        register_btn.pressed.connect(self.activate_register)
        main_menu_layout.addWidget(register_btn)
        
        list_btn = QPushButton("Make Shopping List")
        list_btn.pressed.connect(self.activate_list)
        main_menu_layout.addWidget(list_btn)
        
        listWidget = QListWidget()

        file = open("stores.json", "r")
        content = file.read()
        stores = json.loads(content)
        for store in stores:
            listWidgetItem = QListWidgetItem(store['store_name'])
            listWidget.addItem(listWidgetItem)
        main_menu_layout.addWidget(listWidget)


        menu_widget = QWidget()
        menu_widget.setLayout(main_menu_layout)
        self.stacklayout.addWidget(menu_widget)

    def register_tab(self):
        register_layout = QVBoxLayout()

        btn = QPushButton("Cancel")
        btn.pressed.connect(self.activate_main_menu)
        register_layout.addWidget(btn)
        
        register_widget = QWidget()
        register_widget.setLayout(register_layout)
        self.stacklayout.addWidget(register_widget)
    
    def list_tab(self):
        list_layout = QHBoxLayout()
        btn = QPushButton("Cancel")
        btn.pressed.connect(self.activate_main_menu)
        list_layout.addWidget(btn)
        
        list_widget = QWidget()
        list_widget.setLayout(list_layout)
        self.stacklayout.addWidget(list_widget)
    
    def activate_main_menu(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_register(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_list(self):
        self.stacklayout.setCurrentIndex(2)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
