# Elections-scraper-projekt3
Treti projekt ne Engeto akademii kurz Python.

POPIS PROJEKTU:
Tento projekt sluzi k extrahovaniu vysledkou z parlamentnych volieb 2017. Odkaz https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

INSTALACE KNIHOVEN:
Knihovny, ktore su pouzite v kodu su ulozene v suboru 'requirements.txt'.
Pro instalaci doporucujem pouzit nove virtualne prostredie a s nainstalovanym manazerom nainstalovat knihovny:
pip --version               #overim verzi manazeru
pip install requests        #instalace knihovny requests
pip install beautifulsoup4  #instalace knihovny beautifulsoup4

SPUSTENIE PROGRAMU:
V IDLE (napr. PyCharm) subor 'projekt_3.py'
Hlavna funkcia 'scap_data_write_to_csv' ma 2 argumenty:
Argument 1 nazvany 'main_url' - v kode je pouzity link na volby pro okres Prostejov: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Argument 2 nazvany 'csv_file' - v kode je pouzity nazov csv suboru 'vysledky_prostejov.csv'

OPIS PROGRAMU:
- 'rozdelene_html' - z hlavnej url adresy uzemneho celku 'main_url' vyextrahuje vsetky data, 
z ktoreho ziskam do csv suboru cisla (do listu 'cislo_list') a nazvy (do listu 'obec_list') vsetkych obci daneho uzemneho celku (a takisto pomocny list 'http_adresy1' adries vsetkych obci daneho uzemneho celku)
- 'rozdelene_html_hlavicka' - z http adresy ulozenej pod 'http_hlavicka' (co je adresa pre Alojzov) ziskam pre csv subor zahlavie (prvy riadok),
a to najprv do listu 'hlavicka' a nasledne zapis do csv suboru,
- pocet vsech obci - pomocou dlzky len(vsechny cisla) - co je list vyextrahovanych data z 'rozdelene_html' ako 'rozdelene_html.find_all("td", {"class": "cislo"})'
Pocet vsech obci potom definuje i pocet riadkov v csv subory (okrem hlavicky)
- 'rozdelene_html_obec' - z listu http adries jednotlivych obci 'http_adresy1' vyextrahovanie dat ako su 'Voliči v seznamu', 'Odevzdané obálky', 'Platné hlasy', a hlasy pre jednotlive politicke strany

UKAZKA PRIEBEHU:
Stahuji data z vybraneho url: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_prostejov.csv.
Ukoncuji election scraper projekt_3