#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QCalendarWidget, QHBoxLayout, QVBoxLayout, QDialog


class MyWin(QDialog):
    
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        
        self.initUI()
        
        
    def initUI(self):
        #Creo calendario
        self.calendar_label = QLabel('Seleziona la data', self)
        self.calendar = QCalendarWidget(self)
        #Creo i bottoni
        self.btn_download = QPushButton('Scarica Bolle', self)
        self.btn_upload = QPushButton('Carica Vendite', self)
        #Creo layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_download)
        hbox.addWidget(self.btn_upload)
        vbox.addWidget(self.calendar_label)
        vbox.addWidget(self.calendar)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle('Occupy Artoni')
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MyWin()
    sys.exit(app.exec_())
