"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Marek Dembický
email: marodembo@gmail.com
discord: Mark D. #8143
"""

import sys
import bs4
import csv
import requests

list_arguments = sys.argv
main_url = list_arguments[1]
csv_file = list_arguments[2]

odpoved = requests.get(main_url) # parsovana odpoved na typ GET
rozdelene_html = bs4.BeautifulSoup(odpoved.text, features='html.parser')
print(f'Stahuji data z vybraneho url: {main_url}')

# zisk listu http adries jednotlivych obci
http_adresy = []
for td_class_cislo in rozdelene_html.find_all('td', {'class': 'cislo'}):
    for link in td_class_cislo:
        http_adresy.append(('https://volby.cz/pls/ps2017nss/' + link.get('href')))

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
# nasledny zapis hlavicky z listu do csv suboru:

with open(csv_file, encoding='utf-8', newline='', mode="w") as vysledny_soubor_csv:
    zapisovac = csv.writer(vysledny_soubor_csv)
    zapisovac.writerow(hlavicka)
    vysledny_soubor_csv.close()

print(f'UKLADAM DO SOUBORU: {csv_file}.')
# Zisk listu jednotlivych dat (riadok 2 az ...) ako su cislo, nazov, ... pre vsetky obce
obec_list = []
cislo_list = []
vsechny_obce = rozdelene_html.find_all("td", {"class": "overflow_name"}) #vyextrahovanie z main_url nazvu jednotlivych obci
vsechny_cisla = rozdelene_html.find_all("td", {"class": "cislo"}) #vyextrahovanie z main_url vsech cisel jednotlivych obci
x = len(vsechny_cisla)
for i in range(0, x): #vyextrahovanie do listu a nasledny zapis kazdeho riadku do csv suboru (okrem hlavicky)
    cislo_list.append(vsechny_cisla[i].get_text()) #vyextrahovanie hodnoty cisla obce do pomocneho listu 'cislo_list'
    obec_list.append(vsechny_obce[i].get_text()) #vyextrahovanie nazvu obce do pomocneho listu 'obec_list'
    odpoved_obec = requests.get(http_adresy[i])
    rozdelene_html_obec = bs4.BeautifulSoup(odpoved_obec.text, features='html.parser') #vyextrahovanie data jednotlivych obci zo zoznamu http adries jednotlivych obci
    row_obec = [] #zisk dat ako su cislo, nazov, ... pre kazdu obec
    row_obec.append(cislo_list[i])
    row_obec.append(obec_list[i])
    row_obec.append(rozdelene_html_obec.find('td', {'headers': 'sa2'}).get_text())  # 'Voliči v seznamu'
    row_obec.append(rozdelene_html_obec.find('td', {'headers': 'sa5'}).get_text())  # 'Odevzdané obálky'
    row_obec.append(rozdelene_html_obec.find('td', {'headers': 'sa6'}).get_text())  # 'Platné hlasy'
    strany_obec_part1 = rozdelene_html_obec.find_all('td', {'headers': 't1sa2 t1sb3'}) # hlasy pre jednotlive politicke strany cast1
    strany_obec_part2 = rozdelene_html_obec.find_all('td', {'headers': 't2sa2 t2sb3'}) # hlasy pre jednotlive politicke strany cast2
    for a in strany_obec_part1:
        row_obec.append(a.get_text())
    for a in strany_obec_part2[:-1]:
        row_obec.append(a.get_text())
    # zapis dat ako su cislo, nazov, ... pre kazdu obec z listu row_obec do csv suboru
    with open(csv_file, encoding='utf-8', newline='', mode="a") as vysledny_soubor_csv:
        zapisovac = csv.writer(vysledny_soubor_csv)
        zapisovac.writerow(row_obec)
        vysledny_soubor_csv.close()
print('Ukoncuji election scraper projekt_3')