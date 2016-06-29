#!/usr/bin/env python3

import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


def get_bolla(tipo_bolla):
    #Inserisco elemento di controllo sul caricamento della bolla vera e propria
    elemento_controllo = WebDriverWait(dr, 150).until(EC.invisibility_of_element_located((By.ID, 'loaderBodyPage')))
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
        nome_testata = WebDriverWait(dr, 20).until(EC.presence_of_element_located((By.ID, 'lblTitoloDettaglio'))).text
        identificativo_testata = dr.find_element_by_id('lblCodice').text
        numero_testata = dr.find_element_by_id('lblNumeroDettaglio').text
        barcode_testata = dr.find_element_by_id('lblBarcodeDettaglio').text
        dati_testata.extend([nome_testata, identificativo_testata, numero_testata, barcode_testata])
        lista_bolla.append(dati_testata)
    #Scrivo bolla su file. TODO nome file appropiato (tipo bolla, data)
    output_file = open('bolla_{}_{}.csv'.format(tipo_bolla, time.strftime('%d%m%y')), 'w')
    output_writer = csv.writer(output_file)
    output_writer.writerow(['Testata', 'Pubblicazione', 'Numero', 'Barcode'])
    for row in lista_bolla:
        output_writer.writerow(row)
    print('File {} creato'.format(output_file.name))
    output_file.close()



start_time = time.time()

#Check file credenziali. TODO se il file non esiste, crearlo
try:
    credentials_file = open('secrets.txt').readlines()
    username = credentials_file[0].strip()[9:]
    password = credentials_file[1].strip()[9:]
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

#Scarico bolla B
dr.get('http://www.adriaticapress.com/Bolla.htm-24/06/2016-B')
try:
    if dr.title == 'Errore di runtime':
        raise ValueError('testo raise')
    get_bolla('B')
except WebDriverException:
    print('Si è verificato un errore imprevisto, la bolla di tipo B'
          'non verrà scaricata')
except ValueError:
    print('Bolla tipo B non presente, continuo con il programma')

#Scarico bolla C
dr.get('http://www.adriaticapress.com/Bolla.htm-24/06/2016-C')
try:
    if dr.title == 'Errore di runtime':
        raise ValueError('testo raise')
    get_bolla('C')
except WebDriverException:
    print('Si è verificato un errore imprevisto, la bolla di tipo C'
          ' non verrà scaricata')
except ValueError:
    print('Bolla tipo C non presente, continuo con il programma')

    
dr.close()
print('Operazione completata in {} secondi'.format(round(time.time() - start_time)))

#Nel caso sia preferibile passare attraverso la pagina 'SelezionaBolle'
#Gestisco il dropdown tramite xpath, in alternativa avrei potuto anche
#utiizzare il costrutto 'Select' fornito da Selenium.
#Per ulteriori info cfr https://stackoverflow.com/a/28613320
#driver.find_element_by_xpath('//select[@id=\"ddlBolle\"]/option[@value=\"{}\"]'.format(time.strftime('%d/%m/%Y'))).click()
