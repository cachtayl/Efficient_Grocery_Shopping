import json
import os
import sys

from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QAction, QApplication, QComboBox, QHBoxLayout,
                               QLabel, QLineEdit, QListWidget, QListWidgetItem,
                               QMainWindow, QPushButton, QSpinBox,
                               QStackedLayout, QTableWidget, QTableWidgetItem,
                               QToolBar, QVBoxLayout, QWidget)

basedir = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self):
        # if json db does not exist, then create one
        if os.path.exists('stores.json') == False:
            db = open("stores.json", "w")
            db.write('[]')
            db.close()
        # initialize list of stores
        self.update_stores()
        self.initUI()

    def initUI(self):
        super().__init__()
        font = self.font()
        font.setPointSize(12)
        self.window().setFont(font)

        self.stacklayout = QStackedLayout()

        self.menuTab()  # stack index0
        self.registerTab()  # stack index1

        self.setWindowTitle("Main Menu")
        self.resize(300, 300)
        self.toolbar.toggleViewAction().setChecked(False)
        self.toolbar.toggleViewAction().trigger()

        widget = QWidget()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)

    def menuTab(self):
        main_menu_layout = QVBoxLayout()

        self.toolbar = QToolBar("Store Toolbar")
        self.toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.setIconSize(QSize(30, 30))

        # Plus icon by Icons8: https://icons8.com/icon/3QiOfjluKyC9/plus
        register_btn = QAction(
            QIcon(os.path.join(basedir, "icons", "icons8-plus-24.png")), "Add Store", self)
        register_btn.setToolTip("Add a Store")
        register_btn.triggered.connect(lambda: self.changeTab(1))
        self.toolbar.addAction(register_btn)

        # Delete icon by Icons8: https://icons8.com/icon/lenQJDeFgQWn/minus
        delete_btn = QAction(
            QIcon(os.path.join(basedir, "icons", "icons8-subtract-24.png")), "Delete Store", self)
        delete_btn.setToolTip("Delete selected Store")
        delete_btn.triggered.connect(self.delete_store)
        self.toolbar.addAction(delete_btn)
        delete_btn.setEnabled(False)

        # Edit icon by Icons8: "https://img.icons8.com/ios-glyphs/30/000000/edit--v1.png"
        edit_btn = QAction(
            QIcon(os.path.join(basedir, "icons", "icons8-edit-24.png")), "Edit Store", self)
        edit_btn.setToolTip("Edit selected Store")
        edit_btn.triggered.connect(self.edit_store)
        self.toolbar.addAction(edit_btn)
        edit_btn.setEnabled(False)

        self.storesListWidget = QListWidget()

        for store in self.stores:
            listWidgetItem = QListWidgetItem(store['store_name'])
            self.storesListWidget.addItem(listWidgetItem)
        main_menu_layout.addWidget(self.storesListWidget)

        list_btn = QPushButton("Make Shopping List")
        list_btn.pressed.connect(lambda: self.changeTab(2))
        list_btn.setEnabled(False)
        main_menu_layout.addWidget(list_btn)

        # enable 'Make Shopping List' button if there is a selection
        def enable():
            if len(self.storesListWidget.selectedItems()) != 0:
                list_btn.setEnabled(True)
                delete_btn.setEnabled(True)
                edit_btn.setEnabled(True)
            else:
                list_btn.setEnabled(False)
                delete_btn.setEnabled(False)
                edit_btn.setEnabled(False)
        self.storesListWidget.itemSelectionChanged.connect(enable)

        menu_widget = QWidget()
        menu_widget.setLayout(main_menu_layout)
        self.stacklayout.addWidget(menu_widget)

    def resetMenuTab(self):
        self.storesListWidget.clear()
        for store in self.stores:
            listWidgetItem = QListWidgetItem(store['store_name'])
            self.storesListWidget.addItem(listWidgetItem)

    def update_stores(self):
        # update the stores list
        db = open("stores.json", "r")
        content = db.read()
        self.stores = json.loads(content)
        db.close()

    def delete_store(self):
        self.update_stores()
        selected = self.storesListWidget.currentItem()
        selected_idx = self.storesListWidget.row(selected)
        del self.stores[selected_idx]
        # overwrite json file with the new stores list
        json_obj = json.dumps(self.stores, indent=4)
        db = open("stores.json", "w")
        db.write(json_obj)
        db.close()

        self.storesListWidget.takeItem(selected_idx)

    def edit_store(self):
        self.update_stores()
        self.store = self.stores[self.storesListWidget.row(
            self.storesListWidget.currentItem())]
        self.setWindowTitle("Edit " + self.store['store_name'])
        self.resize(500, 300)
        self.resetRegisterTab()
        self.store_name.setText(self.store['store_name'])

        self.store.pop('store_name')
        for aisle_num in self.store.keys():
            rowPos = self.registerTableWidget.rowCount()
            category = self.store[aisle_num]
            for elem in category:
                self.registerTableWidget.insertRow(rowPos)
                self.registerTableWidget.setItem(
                    rowPos, 0, MyTableWidgetItem(str(aisle_num)))
                self.registerTableWidget.setItem(
                    rowPos, 1, MyTableWidgetItem(elem))
        self.delete_store()
        self.toolbar.toggleViewAction().trigger()
        self.resize(1000, 600)
        self.stacklayout.setCurrentIndex(1)

    def registerTab(self):
        # self.toolbar.toggleViewAction().trigger()
        register_layout = QVBoxLayout()
        aisle_layout = QVBoxLayout()

        name_label = QLabel("Store Name:")
        self.store_name = QLineEdit()
        self.store_name.setPlaceholderText("E.g. Walmart")

        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.store_name)
        aisle_layout.addLayout(name_layout)

        row_label = QLabel("Row:")
        self.row = QSpinBox()
        self.row.setMinimum(1)

        category_label = QLabel("Contains:")
        self.category = QLineEdit()
        self.category.setPlaceholderText("E.g. Desserts/Pasteries")

        row_layout = QHBoxLayout()
        row_layout.addWidget(row_label)
        row_layout.addWidget(self.row)
        row_layout.addWidget(category_label)
        row_layout.addWidget(self.category)

        self.registerTableWidget = QTableWidget()
        self.registerTableWidget.setColumnCount(2)
        self.registerTableWidget.verticalHeader().setVisible(False)
        self.registerTableWidget.setHorizontalHeaderItem(
            0, MyTableWidgetItem("Row"))
        self.registerTableWidget.setHorizontalHeaderItem(
            1, MyTableWidgetItem("Category"))
        self.registerTableWidget.setColumnWidth(0, 20)
        self.registerTableWidget.horizontalHeader().setStretchLastSection(True)

        def add_aisle():
            if self.category.text():
                rowPos = self.registerTableWidget.rowCount()
                self.registerTableWidget.insertRow(rowPos)
                self.registerTableWidget.setItem(
                    rowPos, 0, MyTableWidgetItem(str(self.row.value())))
                self.registerTableWidget.setItem(
                    rowPos, 1, MyTableWidgetItem(self.category.text()))
                self.registerTableWidget.sortItems(0, Qt.AscendingOrder)
                self.category.clear()
            else:
                None
        self.category.returnPressed.connect(add_aisle)
        add_btn = QPushButton("Add Aisle")
        add_btn.pressed.connect(add_aisle)
        row_layout.addWidget(add_btn)
        aisle_layout.addLayout(row_layout)
        aisle_layout.addWidget(self.registerTableWidget)

        def insertStore():
            self.registerTableWidget.sortItems(0, Qt.AscendingOrder)
            new_store = {"store_name": self.store_name.text()}
            for i in range(self.registerTableWidget.rowCount()):
                row = self.registerTableWidget.item(i, 0)
                row = row.text()
                category = self.registerTableWidget.item(i, 1)
                category = category.text()
                new_store.setdefault(row, []).append(category)

            self.stores.append(new_store)
            json_obj = json.dumps(self.stores, indent=4)
            db = open("stores.json", "w")
            db.write(json_obj)
            db.close()
            self.changeTab(0)

        reg_btn = QPushButton("Register")
        reg_btn.pressed.connect(insertStore)

        def cancel():
            if 'Edit' in self.windowTitle():
                insertStore()
            else:
                self.changeTab(0)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.pressed.connect(cancel)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(reg_btn)
        btn_layout.addWidget(cancel_btn)
        register_layout.addLayout(aisle_layout)
        register_layout.addLayout(btn_layout)

        register_widget = QWidget()
        register_widget.setLayout(register_layout)
        self.stacklayout.addWidget(register_widget)

    def resetRegisterTab(self):
        self.store_name.clear()
        self.row.setValue(1)
        self.category.clear()
        self.registerTableWidget.clearContents()
        self.registerTableWidget.setRowCount(0)

    def shoppingListTab(self):
        shopping_list_layout = QVBoxLayout()

        nest_layout = QVBoxLayout()

        item_layout = QHBoxLayout()
        item_label = QLabel("Item:")
        self.user_item = QLineEdit()
        self.user_item.setPlaceholderText("E.g. Bananas")

        cat_layout = QHBoxLayout()
        cat_layout.setAlignment(Qt.AlignLeft)
        categories_label = QLabel("Associated Aisle: ")
        self.categories = QComboBox()

        self.store = self.stores[self.storesListWidget.row(
            self.storesListWidget.currentItem())]
        self.nums = []
        self.store.pop('store_name')
        for aisle_num in self.store.keys():
            category = self.store[aisle_num]
            tot = ''
            for element in category:
                tot += element + ' / '
            self.categories.addItem(tot[:-2])
            self.nums.append(aisle_num)
        self.categories.setCurrentIndex(-1)

        self.shoppingTableWidget = QTableWidget()
        self.shoppingTableWidget.setColumnCount(3)
        self.shoppingTableWidget.verticalHeader().setVisible(False)
        self.shoppingTableWidget.setHorizontalHeaderItem(
            0, MyTableWidgetItem("Row"))
        self.shoppingTableWidget.setHorizontalHeaderItem(
            1, MyTableWidgetItem("Item"))
        self.shoppingTableWidget.setHorizontalHeaderItem(
            2, MyTableWidgetItem("Aisle"))
        self.shoppingTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.shoppingTableWidget.setColumnWidth(0, 20)
        self.shoppingTableWidget.setColumnWidth(1, 220)
        self.shoppingTableWidget.horizontalHeader().setStretchLastSection(True)

        def add_item():
            if self.user_item.text() and self.categories.currentIndex() != -1:
                selectedAisle_name = self.categories.currentText()
                selectedAisle_num = self.nums[self.categories.currentIndex()]
                rowPos = self.shoppingTableWidget.rowCount()
                self.shoppingTableWidget.insertRow(rowPos)
                self.shoppingTableWidget.setItem(
                    rowPos, 0, MyTableWidgetItem(selectedAisle_num))
                self.shoppingTableWidget.setItem(
                    rowPos, 1, MyTableWidgetItem(self.user_item.text()))
                self.shoppingTableWidget.setItem(
                    rowPos, 2, MyTableWidgetItem(selectedAisle_name))
                self.shoppingTableWidget.resizeColumnToContents(0)
                self.shoppingTableWidget.sortItems(0, Qt.AscendingOrder)
                self.user_item.clear()
                self.categories.setCurrentIndex(-1)
            else:
                None
        self.user_item.returnPressed.connect(add_item)
        add_btn = QPushButton("Add Item")
        add_btn.pressed.connect(add_item)

        item_layout.addWidget(item_label)
        item_layout.addWidget(self.user_item)
        cat_layout.addWidget(categories_label)
        cat_layout.addWidget(self.categories)
        nest_layout.addLayout(item_layout)
        nest_layout.addLayout(cat_layout)
        nest_layout.addWidget(add_btn)
        shopping_list_layout.addLayout(nest_layout)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.pressed.connect(lambda: self.changeTab(0))

        shopping_list_layout.addWidget(self.shoppingTableWidget)
        shopping_list_layout.addWidget(cancel_btn)

        shopping_list = QWidget()
        shopping_list.setLayout(shopping_list_layout)
        self.stacklayout.addWidget(shopping_list)

    def changeTab(self, page_idx):
        # Update the stores list every page change
        self.update_stores()
        # Leaving menu tab
        if self.stacklayout.currentIndex() == 0:
            self.toolbar.toggleViewAction().trigger()
        # Leaving shoppingList tab, will delete that page and recreate on demand
        elif self.stacklayout.currentIndex() == 2:
            currShoppingList = self.stacklayout.currentWidget()
            currShoppingList.deleteLater()

        # Switching between pages of the stacklayout
        if page_idx == 0:
            self.setWindowTitle("Main Menu")
            self.resize(300, 300)
            self.toolbar.toggleViewAction().trigger()
            self.resetMenuTab()
        elif page_idx == 1:
            self.setWindowTitle("Register Store")
            self.resize(1000, 600)
            self.resetRegisterTab()
        elif page_idx == 2:
            # create on this tab on demand
            self.shoppingListTab()
            store_name = self.storesListWidget.currentItem()
            self.setWindowTitle(store_name.text()+" Shopping List")
            self.resize(1000, 600)

        self.stacklayout.setCurrentIndex(page_idx)

# overwrite tablewidget's less than method to numerically sort
class MyTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return int(self.text()) < int(other.text())
        except:
            return QTableWidgetItem.__lt__(self, other)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Grocery Bag icon: https://icon-icons.com/icon/grocery-bag-shopping-bag-marketplace/225198
    app.setWindowIcon(QIcon(os.path.join(basedir, "icons", "grocerybag.ico")))
    window = MainWindow()
    window.show()
    app.exec_()
