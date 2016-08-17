#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QCalendarWidget, QHBoxLayout, QVBoxLayout


class MyWin(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        #Creo calendario
        calendar_label = QLabel('Seleziona la data', self)
        calendar = QCalendarWidget(self)
        #Creo i bottoni
        btn_download = QPushButton('Scarica Bolle', self)
        btn_upload = QPushButton('Carica Vendite', self)
        #Creo layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(btn_download)
        hbox.addWidget(btn_upload)
        vbox.addWidget(calendar_label)
        vbox.addWidget(calendar)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MyWin()
    sys.exit(app.exec_())
