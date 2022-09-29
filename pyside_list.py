import json
import os
import sys
import faulthandler
faulthandler.enable()

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        # if json db does not exist, then create one
        if os.path.exists('stores.json') == False: 
            db = open("stores.json", "w")
            db.write('[]')
            db.close()
        #initialize list of stores
        db = open("stores.json", "r")
        content = db.read()
        self.stores = json.loads(content)
        self.store = self.stores[0]
        db.close()
        
        self.initUI()

    def initUI(self):
        super().__init__()
        font = self.font()
        font.setPointSize(10)
        # set the font for the top level window (and any of its children):
        self.window().setFont(font)
        self.setWindowTitle("Efficient Grocery List Generator")
        self.stacklayout = QStackedLayout()
        
        self.main_menu_tab()    #stack index0
        self.register_tab()     #stack index1
        self.shopping_list_tab()         #stack index2

        widget = QWidget()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)

    def main_menu_tab(self):
        main_menu_layout = QVBoxLayout()
        
        self.toolbar = QToolBar("Store Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.toggleViewAction().setChecked(False)
        self.toolbar.toggleViewAction().trigger()
        
        #Plus icon by Icons8: https://icons8.com/icon/3QiOfjluKyC9/plus
        register_btn = QAction(QIcon("./icons/icons8-plus-24.png"), "Add Store", self)
        register_btn.setToolTip("Add a Store")
        register_btn.triggered.connect(lambda: self.changeTab(1))
        self.toolbar.addAction(register_btn)
        
        #Delete icon by Icons8: https://icons8.com/icon/lenQJDeFgQWn/minus
        delete_btn = QAction(QIcon("./icons/icons8-subtract-24.png"), "Delete Store", self)
        delete_btn.setToolTip("Delete selected Store")
        delete_btn.triggered.connect(self.delete_store)
        self.toolbar.addAction(delete_btn)

        #Edit icon by Icons8: "https://img.icons8.com/ios-glyphs/30/000000/edit--v1.png"
        edit_btn = QAction(QIcon("./icons/icons8-edit-24.png"), "Edit Store", self)
        edit_btn.setToolTip("Edit selected Store")
        edit_btn.triggered.connect(self.edit_store)
        self.toolbar.addAction(edit_btn)
          
        self.listWidget = QListWidget()

        for store in self.stores:
            listWidgetItem = QListWidgetItem(store['store_name'])
            self.listWidget.addItem(listWidgetItem)
        main_menu_layout.addWidget(self.listWidget)

        list_btn = QPushButton("Make Shopping List")
        list_btn.pressed.connect(lambda: self.changeTab(2))
        list_btn.setEnabled(False)
        main_menu_layout.addWidget(list_btn)
        
        #disable the shopping list button when an item isn't selected
        self.listWidget.itemSelectionChanged.connect(lambda: list_btn.setEnabled(True) 
                                                        if len(self.listWidget.selectedItems()) != 0 
                                                        else list_btn.setEnabled(False))
        # self.store = self.stores[self.listWidget.row(self.listWidget.currentItem())]
            
        menu_widget = QWidget()
        menu_widget.setLayout(main_menu_layout)
        self.stacklayout.addWidget(menu_widget)
    
    def delete_store(self):
        pass
    def edit_store(self):
        pass
    def register_tab(self):
        self.toolbar.toggleViewAction().trigger()
        register_layout = QVBoxLayout() 
        btn = QPushButton("Cancel")
        btn.pressed.connect(lambda: self.changeTab(0))
        register_layout.addWidget(btn)
        
        register_widget = QWidget()
        register_widget.setLayout(register_layout)
        self.stacklayout.addWidget(register_widget)
    
    def shopping_list_tab(self):
        self.toolbar.toggleViewAction().trigger()
        shopping_list_layout = QHBoxLayout()
        btn = QPushButton("Cancel")
        btn.pressed.connect(lambda: self.changeTab(0))
        shopping_list_layout.addWidget(btn)
        
        shopping_list = QWidget()
        shopping_list.setLayout(shopping_list_layout)
        self.stacklayout.addWidget(shopping_list)
    
    def changeTab(self, page_idx):
        #update the stores list every page change
        db = open("stores.json", "r")
        content = db.read()
        self.stores = json.loads(content)
        db.close()
        #leaving main menu
        if self.stacklayout.currentIndex() == 0:
            self.toolbar.toggleViewAction().trigger()
            None
        #entering main menu
        elif page_idx == 0:
            self.toolbar.toggleViewAction().trigger()
            None
        if page_idx == 2:
            self.store = self.stores[self.listWidget.row(self.listWidget.currentItem())]
            print(self.store)
        self.stacklayout.setCurrentIndex(page_idx)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
