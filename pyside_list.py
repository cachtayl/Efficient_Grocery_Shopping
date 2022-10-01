import json, os, re, sys
import faulthandler
from unicodedata import name
faulthandler.enable()

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QFont, QPalette, QColor

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
        #BUG will break if json file is empty
        self.store = self.stores[0]
        db.close()
        
        self.initUI()

    def initUI(self):
        super().__init__()
        font = self.font()
        font.setPointSize(10)
        # set the font for the top level window (and any of its children):
        self.window().setFont(font)
        self.stacklayout = QStackedLayout()
        
        self.menuTab()          #stack index0
        self.registerTab()      #stack index1
        self.shoppingListTab()  #stack index2
        self.setWindowTitle("Main Menu")
        self.resize(300, 300)
        
        widget = QWidget()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)

    def menuTab(self):
        main_menu_layout = QVBoxLayout()
        
        self.toolbar = QToolBar("Store Toolbar")
        self.toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
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
          
        self.storesListWidget = QListWidget()

        for store in self.stores:
            listWidgetItem = QListWidgetItem(store['store_name'])
            self.storesListWidget.addItem(listWidgetItem)
        main_menu_layout.addWidget(self.storesListWidget)

        list_btn = QPushButton("Make Shopping List")
        list_btn.pressed.connect(lambda: self.changeTab(2))
        list_btn.setEnabled(False)
        main_menu_layout.addWidget(list_btn)
        
        #enable button if there is a selection
        def enable(): return list_btn.setEnabled(True) if len(self.storesListWidget.selectedItems()) != 0 else list_btn.setEnabled(False)
        self.storesListWidget.itemSelectionChanged.connect(enable)
            
        menu_widget = QWidget()
        menu_widget.setLayout(main_menu_layout)
        self.stacklayout.addWidget(menu_widget)
    
    def delete_store(self):
        pass
    def edit_store(self):
        pass

    def registerTab(self):
        self.toolbar.toggleViewAction().trigger()
        register_layout = QVBoxLayout() 
        aisle_layout = QVBoxLayout()
        
        name_label = QLabel("Store Name:")
        name = QLineEdit()
        name.setPlaceholderText("E.g. Walmart")
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(name)
        aisle_layout.addLayout(name_layout)

        row_label = QLabel("Row:")
        row = QSpinBox()
        row.setMinimum(1)
        
        category_label = QLabel("Contains:")
        category = QLineEdit()
        category.setPlaceholderText("E.g. Desserts/Pasteries")
        
        row_layout = QHBoxLayout()
        row_layout.addWidget(row_label)
        row_layout.addWidget(row)
        row_layout.addWidget(category_label)
        row_layout.addWidget(category)
        aisle_layout.addLayout(row_layout)

        self.registerTableWidget = QTableWidget()
        self.registerTableWidget.setColumnCount(2)
        self.registerTableWidget.verticalHeader().setVisible(False)
        self.registerTableWidget.setHorizontalHeaderItem(0, MyTableWidgetItem("Row"))
        self.registerTableWidget.setHorizontalHeaderItem(1, MyTableWidgetItem("Category"))
        self.registerTableWidget.setColumnWidth(0, 20)
        self.registerTableWidget.horizontalHeader().setStretchLastSection(True)

        def add_aisle():
            if category.text():
                rowPos = self.registerTableWidget.rowCount()
                self.registerTableWidget.insertRow(rowPos)
                self.registerTableWidget.setItem(rowPos, 0, MyTableWidgetItem(str(row.value())))
                self.registerTableWidget.setItem(rowPos, 1, MyTableWidgetItem(category.text()))
                self.registerTableWidget.sortItems(0, Qt.AscendingOrder)
                category.clear()
            else: None 
        add_btn = QPushButton("Add Item")
        add_btn.pressed.connect(add_aisle)
        aisle_layout.addWidget(add_btn)
        aisle_layout.addWidget(self.registerTableWidget)

        def insertStore():
            # new_store = {"store_name": store_name}
            pass
        reg_btn = QPushButton("Register")
        reg_btn.pressed.connect(insertStore)
    
        cancel_btn = QPushButton("Cancel")
        cancel_btn.pressed.connect(lambda: self.changeTab(0))
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(reg_btn)
        btn_layout.addWidget(cancel_btn)

        #Nesting Layouts
        register_layout.addLayout(aisle_layout)
        register_layout.addLayout(btn_layout)
        
        register_widget = QWidget()
        register_widget.setLayout(register_layout)
        self.stacklayout.addWidget(register_widget)
    
    def shoppingListTab(self):
        self.toolbar.toggleViewAction().trigger()
        shopping_list_layout = QVBoxLayout()

        nest_layout = QVBoxLayout()
        
        user_item = QLineEdit()
        user_item.setPlaceholderText("E.g. Bananas")

        self.store = self.stores[self.storesListWidget.row(self.storesListWidget.currentItem())]
        self.categories = MyComboBox()
        self.categories.setPlaceholderText("Which Aisle is this in?")
        self.categories.setCurrentIndex(-1)
        
        #alphanumeric sort for keys
        def natural_key(string_):
            return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
        self.nums = []
        self.store.pop('store_name')
        for aisle_num in sorted(self.store.keys(), key=natural_key):
            name = self.store[aisle_num]
            self.nums.append(aisle_num)
            self.categories.addItem(name)
        
        self.shoppingTableWidget = QTableWidget()
        self.shoppingTableWidget.setColumnCount(3)
        self.shoppingTableWidget.verticalHeader().setVisible(False)
        self.shoppingTableWidget.setHorizontalHeaderItem(0, MyTableWidgetItem("Row"))
        self.shoppingTableWidget.setHorizontalHeaderItem(1, MyTableWidgetItem("Item"))
        self.shoppingTableWidget.setHorizontalHeaderItem(2, MyTableWidgetItem("Aisle"))
        self.shoppingTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.shoppingTableWidget.setColumnWidth(0, 20)
        self.shoppingTableWidget.setColumnWidth(1, 220)
        self.shoppingTableWidget.horizontalHeader().setStretchLastSection(True)

        def add_item():
            if user_item.text() and self.categories.currentIndex() != -1:
                selectedAisle_name = self.categories.currentText()
                selectedAisle_num = self.nums[self.categories.currentIndex()]
                rowPos = self.shoppingTableWidget.rowCount()
                self.shoppingTableWidget.insertRow(rowPos)
                self.shoppingTableWidget.setItem(rowPos, 0, MyTableWidgetItem(selectedAisle_num))
                self.shoppingTableWidget.setItem(rowPos, 1, MyTableWidgetItem(user_item.text()))
                self.shoppingTableWidget.setItem(rowPos, 2, MyTableWidgetItem(selectedAisle_name))
                self.shoppingTableWidget.resizeColumnToContents(0)
                self.shoppingTableWidget.sortItems(0, Qt.AscendingOrder)
                user_item.clear()
                self.categories.setCurrentIndex(-1)
            else: None 
        add_btn = QPushButton("Add Item")
        add_btn.pressed.connect(add_item)
        
        nest_layout.addWidget(user_item)
        nest_layout.addWidget(self.categories)
        nest_layout.addWidget(add_btn)
        shopping_list_layout.addLayout(nest_layout)

        
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.pressed.connect(lambda: self.changeTab(0))
        
        shopping_list_layout.addWidget(self.shoppingTableWidget)
        shopping_list_layout.addWidget(cancel_btn)
        
        shopping_list = QWidget()
        shopping_list.setLayout(shopping_list_layout)
        self.stacklayout.addWidget(shopping_list)
    def resetShoppingTab(self):
        self.categories.clear()
        self.store = self.stores[self.storesListWidget.row(self.storesListWidget.currentItem())]
        self.store.pop('store_name')
        #alphanumeric sort for keys
        def natural_key(string_):
            return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
        self.nums = []
        for aisle_num in sorted(self.store.keys(), key=natural_key):
            name = self.store[aisle_num]
            self.nums.append(aisle_num)
            self.categories.addItem(name)
        self.shoppingTableWidget.clearContents()
        self.shoppingTableWidget.setRowCount(0)
    
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
        if page_idx == 0:
            self.setWindowTitle("Main Menu")
            self.resize(300, 300)
            self.toolbar.toggleViewAction().trigger()
            None
        elif page_idx == 1:
            self.setWindowTitle("Register Store")
            self.resize(500, 300)
        elif page_idx == 2:
            self.setWindowTitle("Make Shopping List")
            self.resize(500, 300)
            #Update the shopping list Tab
            self.resetShoppingTab()
        self.stacklayout.setCurrentIndex(page_idx)

#overwrite tablewidget's less than method to numerically sort
class MyTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return int(self.text()) < int(other.text())
        except:
            return QTableWidgetItem.__lt__(self, other)
class MyComboBox(QComboBox):
    # https://code.qt.io/cgit/qt/qtbase.git/tree/src/widgets/widgets/qcombobox.cpp?h=5.15.2#n3173
    def paintEvent(self, event):
        
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.Text))

        # draw the combobox frame, focusrect and selected etc.
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        painter.drawComplexControl(QStyle.CC_ComboBox, opt)

        if self.currentIndex() < 0:
            opt.palette.setBrush(
                QPalette.ButtonText,
                opt.palette.brush(QPalette.ButtonText).color().lighter(),
            )
            if self.placeholderText():
                opt.currentText = self.placeholderText()

        # draw the icon and text
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
