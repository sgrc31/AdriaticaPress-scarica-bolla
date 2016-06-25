#!/usr/bin/env python3

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get('http://www.adriaticapress.com/Login.htm')

time.sleep(15)

#Login credentials
credentials_file = open('secrets.txt').readlines()
username = credentials_file[0].strip()[9:]
password = credentials_file[1].strip()[9:]
username_field = driver.find_element_by_id('txtUsername')
password_field = driver.find_element_by_id('txtPassword')
username_field.clear()
username_field.send_keys(username)
password_field.clear()
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

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
    time.sleep(2)
    nome_testata = driver.find_element_by_id('lblTitoloDettaglio').text
    identificativo_testata = driver.find_element_by_id('lblCodice').text
    numero_testata = driver.find_element_by_id('lblNumeroDettaglio').text
    barcode_testata = driver.find_element_by_id('lblBarcodeDettaglio').text
    dati_testata.extend([nome_testata, identificativo_testata, numero_testata, barcode_testata])
    lista_bolla.append(dati_testata)
