"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Marek Dembický
email: marodembo@gmail.com
discord: Mark D. #8143
"""

import bs4
import csv
import requests

main_url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'  # adresa Prostejov = argument1
# parsovana odpoved na typ GET
odpoved = requests.get(main_url)
rozdelene_html = bs4.BeautifulSoup(odpoved.text, features='html.parser')

# zisk listu http adries jednotlivych obci
http_adresy0 = []
http_adresy1 = []
for link in rozdelene_html.find_all('a'):
    http_adresy0.append(link.get('href'))
for i in http_adresy0[5:-2:2]:
    i = 'https://volby.cz/pls/ps2017nss/' + i
    http_adresy1.append(i)  # adresy1 - zoznam vsech http adress

# zisk hlavicky do csv suboru - prvy riadok
hlavicka = []
hlavicka.append(rozdelene_html.find('th', {'id': 't1sb1'}).get_text())  # zisk v hlavicke 'cislo'
hlavicka.append(rozdelene_html.find('th', {'id': 't1sb2'}).get_text())  # zisk v hlavicke 'nazev'
# Zisk v hlavicke vsetkych ostatnych kolon cez adresu obce napr. Alojzov
http_hlavicka = 'https://volby.cz/pls/ps2017nss/ps311?XJAZYK=CZ&XKRAJ=12&XOBEC=506761&XVYBER=7103&xf=1'
odpoved_hlavicka = requests.get(http_hlavicka)
rozdelene_html_hlavicka = bs4.BeautifulSoup(odpoved_hlavicka.text, features='html.parser')
hlavicka.append(rozdelene_html_hlavicka.find('th', {'id': 'sa2'}).get_text())
hlavicka.append(rozdelene_html_hlavicka.find('th', {'id': 'sa5'}).get_text())
hlavicka.append(rozdelene_html_hlavicka.find('th', {'id': 'sa6'}).get_text())
hlavicka_part1 = rozdelene_html_hlavicka.find_all('td', {'headers': 't1sa1 t1sb2'})
hlavicka_part2 = rozdelene_html_hlavicka.find_all('td', {'headers': 't2sa1 t2sb2'})
for a in hlavicka_part1:
    hlavicka.append(a.get_text())
for a in hlavicka_part2[:-1]:
    hlavicka.append(a.get_text())

# zapis hlavicky z listu do csv suboru:
vysledny_soubor_csv = open("vysledky_prostejov.csv", encoding='utf-8', newline='', mode="w")
zapisovac = csv.writer(vysledny_soubor_csv)
zapisovac.writerow(hlavicka)
vysledny_soubor_csv.close()

# zisk listu jednotlivych data ako su cislo, nazov, ... pre vsetky obce
obec_list = []
cislo_list = []
cislo_obec_list = []
vsechny_obce = rozdelene_html.find_all("td", {"class": "overflow_name"})
vsechny_cisla = rozdelene_html.find_all("td", {"class": "cislo"})
x = len(vsechny_cisla)
for i in range(0, x):
    obec_list.append(vsechny_obce[i].get_text())
    cislo_list.append(vsechny_cisla[i].get_text())
    odpoved_obec = requests.get(http_adresy1[i])
    rozdelene_html_obec = bs4.BeautifulSoup(odpoved_obec.text, features='html.parser')
    row_obec = []
    row_obec.append(obec_list[i])
    row_obec.append(cislo_list[i])
    row_obec.append(rozdelene_html_obec.find('td', {'headers': 'sa2'}).get_text())  # registered numbers - 3rd column C
    row_obec.append(rozdelene_html_obec.find('td', {'headers': 'sa5'}).get_text())  # envelopes numbers - 4th column D
    row_obec.append(rozdelene_html_obec.find('td', {'headers': 'sa6'}).get_text())  # valid numbers - 5th column E
    strany_obec_part1 = rozdelene_html_obec.find_all('td', {'headers': 't1sa2 t1sb3'})
    strany_obec_part2 = rozdelene_html_obec.find_all('td', {'headers': 't2sa2 t2sb3'})

    for a in strany_obec_part1:
        row_obec.append(a.get_text())
    for a in strany_obec_part2[:-1]:
        row_obec.append(a.get_text())

    # zapis dat ako su cislo, nazov, ... pre kazdu obec z listu row_obec do csv suboru
    vysledny_soubor_csv = open("vysledky_prostejov.csv", encoding='utf-8', newline='', mode="a")
    zapisovac = csv.writer(vysledny_soubor_csv)
    zapisovac.writerow(row_obec)
    vysledny_soubor_csv.close()