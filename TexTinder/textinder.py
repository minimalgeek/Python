import sys
from pymongo import MongoClient
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.Qt import Qt

class MongoManager(object):
    
    def __init__(self):
        self.db = MongoClient('localhost', 27017).python_import
        self.collection = self.db.fomc_articles
        self.cursor = self.collection.find({ 'urgency': { '$exists': False } })
        self.max_cursor_idx = self.cursor.count() - 1
        self.cursor_idx = -1
    
    def fetch_new(self):
        if self.cursor_idx < self.max_cursor_idx:
            self.cursor_idx += 1
            return self.cursor[self.cursor_idx]
        return None

    def update_urgency(self, item, is_urgent):
        self.collection.update_one(
            {
                '_id': item['_id']
            },
            {'$set': {
                    'urgency': is_urgent
                }
            })

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.mongo_manager = MongoManager()
        self.title = 'TexTinder'
        self.width = 1280
        self.height = 800
        self.init_ui()
        self.fetch_new()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.center()

        font = QFont()
        font.setPointSize(16)
        
        self.textbox = QLabel(self)
        self.textbox.setStyleSheet("border: 2px solid")
        self.textbox.setWordWrap(True)
        self.textbox.setFont(font)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setGeometry(QRect(40, 40, 1200, 650))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.textbox)

        self.button_normal = QPushButton('not urgent', self)
        self.button_normal.setGeometry(QRect(230, 710, 200, 60))
        self.button_normal.clicked.connect(self.not_urgent)
        self.button_normal.setFont(font)

        self.skip = QPushButton('skip', self)
        self.skip.setGeometry(QRect(530, 710, 200, 60))
        self.skip.clicked.connect(self.skip_current)
        self.skip.setFont(font)

        self.button_urgent = QPushButton('URGENT!!!!!', self)
        self.button_urgent.setGeometry(QRect(830, 710, 200, 60))
        self.button_urgent.clicked.connect(self.urgent)
        self.button_urgent.setFont(font)

        self.show()

    def center(self):
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

    def fetch_new(self):
        self.current_item = self.mongo_manager.fetch_new()
        self.textbox.setText(self.current_item['content'])

    @pyqtSlot()
    def urgent(self):
        self.mongo_manager.update_urgency(self.current_item, 1)
        self.fetch_new()

    @pyqtSlot()
    def skip_current(self):
        self.fetch_new()

    @pyqtSlot()
    def not_urgent(self):
        self.mongo_manager.update_urgency(self.current_item, 0)
        self.fetch_new()

if __name__ == '__main__':
    qtapp = QApplication(sys.argv)
    ex = App()
    sys.exit(qtapp.exec_())
