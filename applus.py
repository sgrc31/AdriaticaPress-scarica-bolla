#!/usr/bin/env python3

import sys
import time
import csv
import os
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QCalendarWidget, QHBoxLayout, QVBoxLayout, QDialog, QTextEdit, QFileDialog, QMessageBox
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException


class MyWin(QDialog):
    
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        
        self.initUI()
        
        
    def initUI(self):
        #Creo calendario
        self.calendar_label = QLabel('Seleziona la data', self)
        self.calendar = QCalendarWidget(self)
        self.stringa_data = time.strftime('%d/%m/%Y') # per far si che ci sia un valore all'avvio, da inserire con strftime
        self.stringa_data_per_nome_file = time.strftime('%d%m%y')
        #Creo i bottoni
        self.btn_download = QPushButton('Scarica Bolle', self)
        self.btn_upload = QPushButton('Carica Vendite', self)
        #Creo widget testo per output
        self.mio_testo = QTextEdit(self)
        self.mio_testo.setReadOnly(True)
        self.mio_testo.setMaximumHeight(50)
        #Creo layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_download)
        hbox.addWidget(self.btn_upload)
        vbox.addWidget(self.calendar_label)
        vbox.addWidget(self.calendar)
        vbox.addLayout(hbox)
        vbox.addWidget(self.mio_testo)
        self.setLayout(vbox)
        self.calendar.clicked[QDate].connect(self.set_date)
        #self.btn_download.clicked.connect(lambda: self.test_funct('ciccio')) #uso lambda per passare ulteriori argomenti al segnale
        self.btn_download.clicked.connect(self.scarica_bolle)
        self.btn_upload.clicked.connect(self.carica_vendite)
        self.setWindowTitle('Occupy Artoni')
        self.show()

    def test_funct(self):
        self.mio_testo.setPlainText('valore')

    def inizio_scarica_bolle(self):
        return self.mio_testo.setPlainText('Inizio il dowload delle bolle...\n')


    def scarica_bolle(self):
        #Definisco la procedura di scarico
        def scarica_bolla(tipo_bolla):
            #Inserisco elemento di controllo sul caricamento della bolla vera e propria
            elemento_controllo = WebDriverWait(dr, 300).until(EC.invisibility_of_element_located((By.ID, 'loaderBodyPage')))
            time.sleep(1)
            #Rendo header statico, così da non interferier nello scroll
            dr.execute_script('$(".superHeader").css({position: "static"});')
            lista_bolla = []
            elenco_link_testate = dr.find_elements_by_css_selector('a[id^=\"ctl00_MainContent_dlBolla_ctl\"]')
            for link in elenco_link_testate:
                dati_testata = []
                #Assicurarsi che il link sia visibile prima di clickarlo
                dr.execute_script('arguments[0].scrollIntoView();', link)
                link.click()
                nome_testata = WebDriverWait(dr, 300).until(EC.presence_of_element_located((By.ID, 'lblTitoloDettaglio'))).text
                identificativo_testata = dr.find_element_by_id('lblCodice').text
                numero_testata = dr.find_element_by_id('lblNumeroDettaglio').text
                try:
                    barcode_testata = dr.find_element_by_id('lblBarcodeDettaglio').text
                except NoSuchElementException:
                    barcode_testata = 'non presente'
                dati_testata.extend([nome_testata, identificativo_testata, numero_testata, barcode_testata])
                lista_bolla.append(dati_testata)
            #Scrivo bolla su file. TODO nome file appropiato (tipo bolla, data)
            output_file = open('bolla_{}_{}.csv'.format(tipo_bolla, self.stringa_data_per_nome_file), 'w')
            output_writer = csv.writer(output_file)
            output_writer.writerow(['Testata', 'Pubblicazione', 'Numero', 'Barcode'])
            for row in lista_bolla:
                output_writer.writerow(row)
            self.mio_testo.insertPlainText('{} File {} creato\n'.format(time.strftime('%H:%M'), output_file.name))
            output_file.close()
                
        #Identificazione
        try:
            with open('secrets.txt') as credentials_file:
                credentials_file_list = list(credentials_file.readlines())
                username = credentials_file_list[0].strip()[9:]
                password = credentials_file_list[1].strip()[9:]
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setText('File credenziali non presente')
            msg.setWindowTitle('testtitolo')
            msg.setStandardButtons(QMessageBox.Ok)
            return msg.exec_()
            #return self.mio_testo.setPlainText('credenziali non presenti')
        dr = webdriver.PhantomJS()
        dr.set_window_size(1920, 1080)
        dr.get('http://www.adriaticapress.com/Login.htm')
        time.sleep(5)
        username_field = WebDriverWait(dr, 15).until(EC.presence_of_element_located((By.ID, 'txtUsername')))
        password_field = WebDriverWait(dr, 15).until(EC.presence_of_element_located((By.ID, 'txtPassword')))
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        #Scarico prima bolla
        dr.get('http://www.adriaticapress.com/Bolla.htm-{}-B'.format(self.stringa_data))
        try:
            if dr.title == 'Errore di runtime':
                raise ValueError('testo raise')
            scarica_bolla('B')
        except WebDriverException:
            self.mio_testo.insertPlainText('errore imprev\n')
        except ValueError:
            self.mio_testo.insertPlainText('{} Bolla tipo B non presente\n'.format(time.strftime('%H:%M')))

        #Scarico seconda bolla
        dr.get('http://www.adriaticapress.com/Bolla.htm-{}-C'.format(self.stringa_data))
        try:
            if dr.title == 'Errore di runtime':
                raise ValueError('testo raise')
            scarica_bolla('C')
        except WebDriverException:
            self.mio_testo.insertPlainText('errore imprev\n')
        except ValueError:
            self.mio_testo.insertPlainText('{} Bolla tipo C non presente\n'.format(time.strftime('%H:%M')))

        #Chiudo tutto
        dr.close()
        self.mio_testo.insertPlainText('{} Procedura terminata\n'.format(time.strftime('%H:%M')))

    def set_date(self, date):
        self.stringa_data = date.toString('dd/MM/yyyy')
        self.stringa_data_per_nome_file = date.toString('ddMMyy')

    def test_funct3(self):
        self.mio_testo.setPlainText(self.stringa_data)

    def carica_vendite(self):
        filename = QFileDialog.getOpenFileName(self, 'Seleziona file vendite', os.path.abspath(os.path.dirname('.')))[0]
        #Per selezionare una cartella invece che un file
        #dirname = QFileDialog.getExistingDirectory(None, 'Select a folder:', '/', QFileDialog.ShowDirsOnly)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWin()
    sys.exit(app.exec_())
