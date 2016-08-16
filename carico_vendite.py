#!/usr/bin/env python3

import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Check file credenziali. TODO se il file non esiste, crearlo
try:
    credentials_file = open('secrets.txt').readlines()
    username = credentials_file[0].strip()[9:]
    password = credentials_file[1].strip()[9:]
    #credentials_file.close()
except FileNotFoundError:
    print('Impossibile trovare file \"secrets.txt\"'
          ' contenente le credenziali d\'accesso.\n'
          'Il programma verrà terminato.')
    print('Uscita per errore critico dopo {} secondi'.format(round(time.time() - start_time)))
    sys.exit(1)

dr = webdriver.Chrome()
dr.get('http://www.adriaticapress.com/Login.htm')
time.sleep(5)

#Login
username_field = WebDriverWait(dr, 15).until(EC.presence_of_element_located((By.ID, 'txtUsername')))
password_field = WebDriverWait(dr, 15).until(EC.presence_of_element_located((By.ID, 'txtPassword')))
username_field.clear()
username_field.send_keys(username)
password_field.clear()
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

time.sleep(5)

dr.get('http://www.adriaticapress.com/Vendita.htm')
time.sleep(5)
elemento_controllo = WebDriverWait(dr, 300).until(EC.invisibility_of_element_located((By.ID, 'loaderBodyPage')))
time.sleep(5)

dr.find_element_by_id('imgMostraRicerca').click()
input_ean = dr.find_element_by_name('txtTitoloRI')
input_qtt = dr.find_element_by_name('txtQ')

with open('vendite.csv') as venditecsv:
    reader_vendite = csv.DictReader(venditecsv)
    for row in reader_vendite:
        input_ean.clear()
        input_ean.send_keys(row['Barcode'])
        input_qtt.clear()
        input_qtt.send_keys(row['Qtt'])
        dr.find_element_by_name('btnCercaRI').click()


