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
except FileNotFoundError:
    print('Impossibile trovare file \"secrets.txt\"'
          ' contenente le credenziali d\'accesso.\n'
          'Il programma verrà terminato.')
    sys.exit(1)

start_time = time.time()
driver = webdriver.Chrome()
driver.get('http://www.adriaticapress.com/Login.htm')

time.sleep(15)

#Login credentials
username_field = driver.find_element_by_id('txtUsername')
password_field = driver.find_element_by_id('txtPassword')
username_field.clear()
username_field.send_keys(username)
password_field.clear()
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)
time.sleep(5)
#Pagina bolla di prova, da modificare TODO
driver.get('http://www.adriaticapress.com/Bolla.htm-24/06/2016-B')
time.sleep(20) #Il caricamendo delle bolle è spesso lento TODO

#Rendo l'header statico, così da non creare problemi con lo scroll
driver.execute_script('$(".superHeader").css({position: "static"});')

lista_bolla = []
elenco_link_testate = driver.find_elements_by_css_selector('a[id^=\"ctl00_MainContent_dlBolla_ctl\"]')

for link in elenco_link_testate:
    dati_testata = []
    driver.execute_script('arguments[0].scrollIntoView();', link)
    link.click()
    #time.sleep(3)
    #nome_testata = driver.find_element_by_id('lblTitoloDettaglio').text
    nome_testata = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'lblTitoloDettaglio')))
    identificativo_testata = driver.find_element_by_id('lblCodice').text
    numero_testata = driver.find_element_by_id('lblNumeroDettaglio').text
    barcode_testata = driver.find_element_by_id('lblBarcodeDettaglio').text
    dati_testata.extend([nome_testata, identificativo_testata, numero_testata, barcode_testata])
    lista_bolla.append(dati_testata)

#Scrivo l'output su .csv
output_file = open('bolla.csv', 'w')
output_writer = csv.writer(output_file)
output_writer.writerow(['Testata', 'Pubblicazione', 'Numero', 'Barcode'])
for row in lista_bolla:
    output_writer.writerow(row)
output_file.close()
driver.close()
total_time = time.time() - start_time
print('Dump completato in ' + str(round(total_time)) + ' secondi.')
