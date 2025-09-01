### **Sveučilište Jurja Dobrile u Puli**
### **Fakultet Informatike u Puli**

<br>
<br>

## **Završni rad**

### **Razvoj i implementacija plugina za arheološka istraživanja u QGIS-u**

<br>
<br>

**Izradio:** Leo Matošević
**Mentor:** izv. prof. dr. sc. Darko Etinger

---

### **Sažetak**
Ovaj rad opisuje razvoj i implementaciju QGIS plugina **ArheologijaPlus**, dizajniranog za digitalizaciju i standardizaciju terenske arheološke dokumentacije. Plugin omogućuje unos, pohranu, uređivanje i izvoz podataka o stratigrafskim jedinicama (SJ) izravno unutar QGIS okruženja. Time se smanjuje dvostruki unos podataka, minimiziraju greške i stvara integrirana prostorna baza podataka koja povezuje grafičku i atributnu dokumentaciju iskopavanja.

---

### **1. Uvod**
GIS (Geografski informacijski sustav) alati postali su neizostavan dio suvremenih arheoloških istraživanja. QGIS, kao vodeći otvoreni GIS softver, pruža moćnu platformu za analizu prostornih podataka. Međutim, standardne GIS funkcionalnosti često nisu dovoljne za specifične potrebe arheološke dokumentacije, poput detaljnog opisa stratigrafskih jedinica.

Plugin **ArheologijaPlus** razvijen je kako bi premostio taj jaz. Njegov je cilj zamijeniti tradicionalne papirnate obrasce digitalnim sučeljem unutar QGIS-a, omogućujući arheolozima da sve podatke (prostorne, opisne, relacijske) vode na jednom mjestu. Time se povećava točnost, učinkovitost i potencijal za daljnje analize.

#### **1.1. Koncept Stratigrafske Jedinice (SJ)**
Stratigrafska jedinica (SJ) je temeljni koncept oko kojeg je plugin izgrađen. Ona predstavlja najmanji, logički odvojiv "događaj" zabilježen u tlu (npr. sloj zemlje, ukop, zid). Svakoj jedinici dodjeljuje se jedinstveni broj te se detaljno dokumentiraju njezine karakteristike, sadržaj i prostorni odnosi s drugim jedinicama. Plugin ArheologijaPlus digitalizira upravo taj proces dokumentiranja.

### **2. Korištene tehnologije**
* **Python:** Glavni programski jezik korišten za razvoj cjelokupne logike plugina.
* **PyQGIS (QGIS Python API):** Omogućuje interakciju plugina s QGIS-om – upravljanje slojevima, podacima, mapom i korisničkim sučeljem.
* **Qt5 i PyQt5:** Framework za izradu grafičkog korisničkog sučelja (GUI). Sučelje plugina (forma za unos podataka) izgrađeno je pomoću ovih tehnologija.
* **Qt Designer:** Vizualni alat za dizajniranje `.ui` datoteka koje definiraju izgled korisničkog sučelja.
* **ReportLab:** Python biblioteka za programsko generiranje PDF dokumenata, korištena za izvoz unesenih podataka u standardizirani obrazac.
* **QGIS Plugin Builder & pb_tool:** Alati korišteni za inicijalno postavljanje strukture projekta i olakšavanje razvojnog ciklusa.

### **3. Arhitektura i opis plugina**
Plugin slijedi standardnu QGIS strukturu i sastoji se od nekoliko ključnih datoteka:

* `ArheologijaPlus.py`: Jezgra plugina. Upravlja inicijalizacijom, integracijom u QGIS sučelje (alatna traka, izbornik), upravlja `dock` prozorom te povezuje korisničke akcije s glavnim funkcionalnostima (spremanje, učitavanje, izvoz). Također sadrži logiku za stvaranje i upravljanje GeoPackage slojem (`Stratigrafske_Jedinice`) koji služi kao baza podataka.
* `ArheologijaPlus_dialog.py`: Upravlja logikom korisničkog sučelja (forme). Definira metode za prikupljanje podataka iz forme (`get_data`), popunjavanje forme podacima iz odabranog objekta (`set_data`) i čišćenje forme (`clear_data`).
* `ArheologijaPlus_dialog_base.ui`: XML datoteka kreirana u Qt Designeru koja definira vizualni raspored svih elemenata sučelja (polja za unos, gumbi, tabovi).
* `export_pdf.py`: Modul zadužen za generiranje PDF izvještaja. Sadrži funkciju koja prikuplja podatke, stvara sliku karte odabranog objekta i pomoću biblioteke ReportLab slaže sve elemente u formatirani A4 dokument.

Rad plugina temelji se na interakciji između QGIS-a i prilagođenog sučelja. Kada korisnik odabere poligon na karti, plugin automatski učitava njegove atribute u formu. Nakon unosa ili izmjene, podaci se spremaju natrag u atributnu tablicu GeoPackage sloja.

![Prikaz dijela sučelja plugina]([https://i.imgur.com/GzB0LdF.png](https://media.discordapp.net/attachments/913822778988331009/1412205422286213262/image.png?ex=68b7724a&is=68b620ca&hm=07c7b3b0a3148dcb987a8f6b7620fcfc7a7e0f8adc8cace2d0055f99b731f7e7&=&format=webp&quality=lossless&width=841&height=960)
*Slika 1: Prikaz korisničkog sučelja plugina unutar QGIS-a*

### **4. Funkcionalnosti**
* **Automatsko stvaranje baze podataka:** Prilikom prvog pokretanja, plugin automatski stvara GeoPackage datoteku (`ArheologijaDB.gpkg`) sa slojem `Stratigrafske_Jedinice` i svom potrebnom strukturom (poljima) za unos podataka.
* **Integrirano sučelje za unos:** Unutar QGIS-a otvara se *dock* prozor s preglednom formom koja sadrži sva polja potrebna za opis stratigrafske jedinice, čime se zamjenjuje papirnati obrazac.
* **Dinamičko povezivanje s kartom:** Odabirom poligona na vektorskom sloju, podaci o toj stratigrafskoj jedinici automatski se učitavaju u formu. Poništavanjem odabira, forma se čisti i spremna je za novi unos.
* **Spremanje podataka:** Uneseni podaci spremaju se kao atributi vezani uz odgovarajući poligon u GeoPackage sloju, čime se osigurava trajna pohrana unutar QGIS projekta.
* **Izvoz u PDF:** Plugin omogućuje generiranje standardiziranog PDF obrasca za odabranu stratigrafsku jedinicu jednim klikom. PDF dokument uključuje sve unesene podatke i automatski generiranu sliku karte s lokacijom odabrane SJ.

### **5. Zaklučak**
Plugin ArheologijaPlus uspješno demonstrira kako se prilagođenim softverskim rješenjima može značajno unaprijediti proces arheološke dokumentacije. Integracijom unosa podataka izravno u GIS okruženje, postiže se veća učinkovitost, točnost i standardizacija. Podaci postaju odmah prostorno kontekstualizirani i spremni za daljnje složene analize. Time se ne samo olakšava terenski rad, već se otvaraju i nove mogućnosti za istraživanje i interpretaciju arheoloških nalazišta. Budući da su arheološki podaci neponovljivi, alati poput ArheologijaPlusa osiguravaju da se oni zabilježe na najprecizniji i najpotpuniji mogući način.

### **6. Literatura**
1.  Spatial without Compromise · QGIS Web Site. [https://qgis.org/](https://qgis.org/)
2.  Documentation for QGIS 3.40 — QGIS Documentation. [https://docs.qgis.org/3.40/en/docs/index.html](https://docs.qgis.org/3.40/en/docs/index.html)
3.  PyQGIS Developer Cookbook — QGIS Documentation. [https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html](https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html)
4.  Riverbank Computing | Introduction. [https://www.riverbankcomputing.com/software/pyqt/](https://www.riverbankcomputing.com/software/pyqt/)
5.  reportlab. PyPI. [https://pypi.org/project/reportlab/](https://pypi.org/project/reportlab/)
