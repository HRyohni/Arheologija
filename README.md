# Sveučilište Jurja Dobrile u Puli
## Fakultet Informatike u Puli

<br>
<br>
<br>
<br>

**Leo Matošević**

# Razvoj i implementacija plugina za arheološka istraživanja u QGIS-u
### Završni rad

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

**Izradio:** Leo Matošević <br>
**Mentor:** izv. prof. dr. sc. Darko Etinger

***

## Sadržaj

* Uvod
* Što je Stratigrafska Jedinica u Kontekstu?
* Korištene tehnologije
    * Što je QGIS?
    * Python
    * PyQGIS
    * Qt i PyQt5
    * QGIS Plugin Builder i pb\_tool
    * ReportLab
* Opis plugina ArheologijaPlus
    * ArheologijaPlus.py
        * `__init__(self, iface)`
        * `initGui(self)`
        * `unload(self)`
        * `run(self)`
        * `populate_form_from_selection(self)`
        * `save_data_to_layer(self)`
        * `exportToPdf(self)`
        * `setup_database_layer(self)`
    * ArheologijaPlus\_dialog.py
        * `__init__(self, parent=None)`
        * `get_data(self)`
        * `Set_data(self,data)`
        * `clear_data(self)`
    * ArheologijaPlus\_dialog\_base.ui
    * export\_pdf.py
        * `_export_map_image(iface, feature)`
* Funkcionalnosti plugina
* Analiza postojećih ograničenja
* Zaključak
* Literatura

***

## Uvod
Digitalne tehnologije i GIS sustavi danas igraju ključnu ulogu u arheološkim istraživanjima. Uvođenje GIS-a u arheologiju dovelo je do velikog unaprjeđenja. GIS omogućuje arheolozima da prikupljaju, pohranjuju, analiziraju i vizualiziraju prostorne podatke na načine koji su prije bili nezamislivi. Korištenjem GIS(Geographic Information System) alata, istraživači mogu precizno georeferencirati nalazišta, pratiti artefakte u prostoru te provoditi složene analize poput mjerenja udaljenosti, izračuna površina. Takvi alati omogućuju dublje razumijevanje prostornih odnosa. Integracijom raznih skupova podataka (npr. planova iskopavanja, satelitskih snimaka, LIDAR (detekcijski sustav koji radi na principu radara) modela terena, povijesnih karata) u jedinstven GIS projekt, arheolozi mogu uočiti korelacije i obrasce koji bi inače ostali skriveni. QGIS, kao besplatni otvoreni GIS softver, posebno je značajan u arheologiji. Osim što je pristupačan (open source licenca) i platformno neovisan, QGIS je iznimno prilagodljiv, njegova otvorena arhitektura omogućuje korisnicima dodavanje vlastitih promjena i pluginova prema potrebi. Mogućnost integriranja i mijenjanja GIS softvera prema vlastitim zahtjevima, posebno aktivnom open-source zajednicom korisnika i programera, dovela je do kontinuiranog usavršavanja QGIS-a. Time je QGIS postao idealna radna okolina za prostorne analize u arheologiji, omogućuje da svi podaci (prostorni, atributivni, multimedijski) budu objedinjeni u jednom sustavu, što ubrzava rad i povećava točnost interpretacija. Međutim, arheološka istraživanja često imaju specifične zahtjeve koje generalni GIS alati ne pružaju u potpunosti. Standardni GIS omogućuje upravljanje prostornim podacima, ali arheolozi često trebaju unositi i analizirati vrlo detaljne podatke iskopavanja (npr. stratigrafske jedinice, konteksti i nalazi) te provoditi specifične analize (poput analize vidljivosti s obzirom na reljef, rekonstrukcije granica naselja na temelju nalaza i sl.). Tu nastaje potreba za prilagođenim pluginovima unutar QGIS-a koji mogu podržati takve specifične zadatke. Ovaj završni rad je fokusiran na razvoj i implementaciju QGIS plugina naziva ArheologijaPlus, namijenjenog podršci arheološkim istraživanjima kroz QGIS. Kroz poglavlja u nastavku opisano je korištene tehnologije, arhitekturu i funkcionalnosti samog plugina, način na koji se integrira u QGIS sučelje.

## Što je Stratigrafska Jedinica u Kontekstu?
Kako bi se u potpunosti razumjela svrha i funkcionalnost plugina ArheologijaPlus, ključno je prvo definirati temeljni koncept oko kojeg je cijeli alat izgrađen: stratigrafsku jedinicu (SJ). Stratigrafska jedinica je osnovna, fundamentalna jedinica arheološkog zapisa i analize. Ona predstavlja najmanji, fizički i logički odvojiv "događaj" zabilježen u tlu. Svaka stratigrafska jedinica je trag jednog jedinstvenog događaja u vremenu, bez obzira na to je li taj događaj trajao trenutak ili stoljeće. U praksi, arheolog na terenu identificira ove jedinice na temelju razlika u boji, sastavu (teksturi), zbijenosti (konzistenciji) i sadržaju (prisutnosti nalaza). Svakoj prepoznatoj jedinici dodjeljuje se jedinstveni broj (npr. SJ 101, SJ 102), nakon čega slijedi njeno detaljno dokumentiranje.

## Korištene tehnologije
Razvoj QGIS plugina ArheologijaPlus oslanja se na niz modernih tehnologija i biblioteka, od programskih jezika do GIS alata. U nastavku su opisane su najvažnije korištene tehnologije i alati:

### Što je QGIS?
QGIS je besplatan i otvoreni (open-source) geografski informacijski sustav. Kao desktop aplikacija, omogućuje korisnicima pregledavanje, uređivanje, analizu i vizualizaciju geoprostornih podataka. S obzirom na to da je razvijen kao OSGeo (Open Source Geospatial Foundation), QGIS predstavlja jedno od najpopularnijih i najmoćnijih rješenja u svijetu GIS-a, koriste ga pojedinci, akademske institucije, tvrtke i organizacije. Jedna od najvažnijih karakteristika QGIS-a, posebno relevantna za ovaj projekt, jest njegova iznimna proširivost putem dodataka (pluginova). Korištenjem programskog jezika Python i PyQGIS sučelja, programeri mogu kreirati prilagođene alate koji proširuju osnovne funkcionalnosti QGIS-a.

### Python
Python je interpretirani jezik visoke razine koji QGIS koristi kao skriptni jezik i jezik za razvoj dodataka (plugina). QGIS je opremljen integriranim Python API (tzv. PyQGIS), što omogućuje da pomoću Pythona pristupe GIS funkcionalnostima i objektima unutar QGIS-a. Plugin ArheologijaPlus u potpunosti je napisan u Pythonu koristeći PyQGIS za interakciju s QGIS-om.

### PyQGIS
PyQGIS (QGIS Python API) je skup Python klasa i funkcija koje odražavaju funkcionalnosti QGIS aplikacije. Putem PyQGIS-a plugin može upravljati mapama, slojevima, prostornim podacima i korisničkim sučeljem QGIS-a. U našem pluginu PyQGIS se koristi, primjerice, za čitanje i pisanje podataka u QGIS projekt (putem klasa kao što je `QgsProject`), za dodavanje elemenata sučelja (npr. dodavanje alata na alatnu traku QGIS-a) te za prikaz poruka korisniku kroz QGIS-ov sučelje. PyQGIS tako omogućuje da plugin nije samostalna aplikacija, nego se ugrađuje u postojeći QGIS i nadograđuje ga specifičnim funkcijama.

### Qt i PyQt5
Za izgradnju grafičkog sučelja plugin koristi Qt framework, odnosno njegovu Python inačicu PyQt5. Qt je sustav za izradu GUI aplikacija, a QGIS-ovo sučelje je temeljeno na Qt-u. Kroz PyQt5 plugin definira dijaloške prozore, kontrole (npr. gumbe, tekstualna polja, padajuće izbornike) i njihov raspored. Konkretno, ArheologijaPlus plugin ima glavni prozor (implementiran kao dock prozor u QGIS-u) s desecima kontrola za unos arheoloških podataka, te su kontrole definirane PyQt5 klasama (`QWidget`, `QLineEdit`, `QComboBox` itd.). Za dizajn sučelja korišten je i Qt Designer, grafički alat koji omogućuje vizualno kreiranje `.ui` datoteka (XML). U projektu se nalazi datoteka `ArheologijaPlus_dialog_base.ui` koja opisuje izgled i elemente formi. Ta se datoteka pri učitavanju plugina dinamički učitava pomoću PyQt-a i pretvara u odgovarajući GUI objekt. Dizajn se može mijenjati u Designeru, a Python kod jednostavno učitava aktualnu verziju forme. PyQt5 također omogućuje povezivanje događaja (klikova, promjena vrijednosti i sl.) s python funkcijama unutar plugina.

### QGIS Plugin Builder i pb_tool
Inicijalna struktura plugina generirana je alatom QGIS Plugin Builder, koji postavlja osnovne datoteke i direktorije prema QGIS standardu (npr. predloške za `__init__.py`, osnovne klase, ikonu, `metadata.txt` i dr.). Uz Plugin Builder korišten je i `pb_tool` (Plugin Builder Tool), skriptni sustav za kompajliranje i instalaciju plugina tijekom razvoja. Alat `pb_tool` olakšava prevođenje `.ui` datoteka i `.qrc` datoteka u Python kod te kopiranje plugina u QGIS-ov direktorij za dodatke radi testiranja. Plugin Builder i `pb_tool` je korišten u početnoj fazi.

### ReportLab
Za potrebe izvoza podataka u PDF format, plugin koristi Python biblioteku ReportLab. ReportLab omogućuje programsko kreiranje PDF dokumenata, uključujući crtanje teksta, tablica, linija i drugih elemenata na stranicu. ReportLab generira izlazni dokument, ispunjeni formular stratigrafske jedinice, tako da precizno odgovara predlošku papirnatog obrasca koji se koristi u terenskoj dokumentaciji. Korištenje ReportLaba je logično rješenje za automatsko generiranje izvještaja odnosno umjesto ručnog popunjavanja papira na terenu, arheolog unosi podatke digitalno, a plugin potom može iz tih podataka izraditi standardizirani PDF dokument spreman za ispis ili digitalno arhiviranje. Osim navedenih, plugin koristi i standardne Python biblioteke.

## Opis plugina ArheologijaPlus
Plugin ArheologijaPlus razvijen je sa ciljem digitalizacije terenske dokumentacije unutar QGIS-a, prvenstveno fokusiran na stratigrafske jedinice (SJ) iskopavanja. Struktura plugina prati standardnu QGIS organizaciju dodataka. U korijenskom direktoriju plugina nalaze se glavne Python datoteke i resursi.

* `__init__.py` je inicijalizacijska skripta koja QGIS-u daje do znanja da se radi o Python paketu i služi kao ulazna točka za pokretanje plugina.
* `ArheologijaPlus.py` je glavna datoteka plugina koja sadrži osnovnu logiku. Ona je odgovorna za integraciju s QGIS sučeljem, kao što je stvaranje unosa u izborniku, gumba na alatnoj traci te povezivanje akcija korisnika s funkcionalnostima plugina.
* `ArheologijaPlus_dialog.py` je python klasa koja upravlja korisničkim sučeljem (dijalogom). Preuzima vizualne elemente definirane u `.ui` datoteci i povezuje ih s kodom.
* `ArheologijaPlus_dialog_base.ui` je XML datoteka kreirana u Qt Designeru. Sadrži vizualni raspored i svojstva svih elemenata korisničkog sučelja.
* `resources.qrc` je XML datoteka koja specificira vanjske resurse, poput ikona, koje plugin koristi. Pomoću QGIS alata (pyrcc) ova se datoteka prevodi u `resources.py` datoteku koju Python može izravno koristiti.
* `icon.png` je ikona koja predstavlja plugin unutar QGIS sučelja.
* `metadata.txt` je datoteka s metapodacima o pluginu, kao što su ime, opis, verzija, autor, kategorija i drugi podaci koji se prikazuju u QGIS Plugin Manageru.
* `export_pdf.py` je dodatna datoteka koja služi za izvoz podataka u pdf

### ArheologijaPlus.py
Ova datoteka je glavni dio plugina ArheologijaPlus. U njoj se definira glavna klasa `ArheologijaPlus` koja upravlja cjelokupnom funkcionalnošću dodatka. To uključuje inicijalizaciju dodatka, stvaranje korisničkog sučelja (alatne trake i menija), upravljanje bazom podataka za arheološke stratigrafske jedinice, obradu korisničkih unosa, spremanje podataka i izvoz podataka u PDF format.

#### `__init__(self, iface)`
`__init__` je konstruktor klase `ArheologijaPlus` koji se poziva prilikom inicijalizacije dodatka unutar QGIS-a. On sprema referencu na QGIS sučelje (`iface`), određuje putanju do direktorija dodatka, te inicijalizira prazne varijable za akcije, meni, alatnu traku, dock widget, dijalog i ciljni sloj. Ove varijable su kasnije korištene za pohranu referenci na odgovarajuće objekte i upravljanje njima.

* `self.iface`: ključni objekt iz QGIS API-ja koji predstavlja glavno sučelje (interface) QGIS aplikacije. Dodatak ga dobiva prilikom pokretanja i služi kao glavni komunikacijski kanal s QGIS-om. Korišten je za dodavanje novih elemenata poput alatnih traka i menija, pristupati aktivnim slojevima, prikazivati poruke korisniku i općenito upravljanje dodatka unutar QGIS okruženja.
* `self.iface.addToolBar(...)`: metoda QGIS sučelja (`iface`) koja stvara i dodaje novu, praznu alatnu traku u glavni prozor QGIS-a. Koristi se za stvaranje zasebne alatne trake na kojoj je gumb za pokretanje funkcionalnosti dodatka, čineći ga lako dostupnim korisniku.

#### `add_action(self, icon_path, text, callback, parent=None)`
Ova metoda služi za stvaranje i dodavanje akcija, odnosno gumba, u meni i alatnu traku dodatka. Metoda učitava ikonu s navedene putanje, stvara novu akciju s ikonom i tekstom, te povezuje `triggered` signal s `callback` metodom koja će se izvršiti prilikom klika. Akcija se zatim dodaje u meni dodatka, alatnu traku i internu listu akcija radi lakšeg upravljanja, te se na kraju vraća kao rezultat.

* `QIcon(icon_path)`: klasa iz PyQt5 biblioteke koja stvara objekt ikone iz slikovne datoteke koja se nalazi na zadanoj putanji. Korištena je za gumb u alatnoj traci i stavka u meniju da imaju prepoznatljivu vizualnu ikonu, što poboljšava korisničko iskustvo.
* `QAction(...)`: klasa iz PyQt5 koja predstavlja korisničku akciju, koja se može prikazati kao stavka u meniju ili gumb na alatnoj traci. Ovdje se koristi za stvaranje jedinstvenog elementa koji će, kada ga korisnik aktivira, pokrenuti glavnu funkcionalnost dodatka.
* `action.triggered.connect(callback)`: ključni mehanizam PyQt5 sustava signala i utora. On povezuje događaj (signal) `triggered`, koji se emitira svaki put kada korisnik klikne na akciju, s `callback` metodom koja se treba izvršiti kao odgovor. Na ovaj se način definira što će se točno dogoditi kada korisnik klikne na gumb dodatka.
* `self.iface.addPluginToMenu(...)`: metoda QGIS sučelja koja dodaje prethodno stvorenu `QAction` u meni dodatka unutar glavnog menija QGIS-a, čineći funkcionalnost dostupnom i putem tekstualnog izbornika.
* `self.toolbar.addAction(...)`: metoda koja dodaje istu `QAction` na alatnu traku i čini ju vidljivom kao gumb za brzi pristup.

#### `initGui(self)`
Ova se metoda poziva prilikom učitavanja dodatka i služi za inicijalizaciju grafičkog korisničkog sučelja. Ona sastavlja putanju do ikone dodatka te poziva prethodno definiranu metodu `add_action` kako bi se stvorilo gumb na alatnoj traci i stavku u meniju. Klikom na taj gumb pokrenut će se glavna `run` metoda dodatka.

#### `unload(self)`
Ova se metoda poziva kada se dodatak isključuje ili deinstalira, a njena je svrha počistiti sve elemente korisničkog sučelja koje je dodatak stvorio. Metoda prekida signal za promjenu selekcije kako bi se izbjegle greške, uklanja dock widget iz QGIS sučelja, te prolazi kroz sve stvorene akcije i uklanja ih iz menija i alatne trake prije brisanja same alatne trake.

* `self.target_layer.selectionChanged.disconnect(...)`: Ova naredba prekida vezu između signala `selectionChanged` (koji se emitira pri promjeni selekcije na sloju) i metode koja je na njega bila spojena da se "počisti" veze prilikom gašenja dodatka i spriječilo da se QGIS pokušava izvršiti kod koji više ne postoji, što bi dovelo do grešaka.
* `self.iface.removeDockWidget(...)`: Uklanja dock widget (prozor s formom) iz glavnog prozora QGIS-a, vraćajući sučelje u stanje kakvo je bilo prije pokretanja dodatka.
* `self.iface.removePluginMenu(...)` i `self.iface.removeToolBarIcon(...)`: Ove metode služe za uredno uklanjanje stavke iz menija i gumba s alatne trake, čime se dodatak u potpunosti uklanja iz korisničkog sučelja.

#### `run(self)`
Ovo je glavna metoda koja se izvršava kada korisnik klikne na gumb dodatka. Ona najprije poziva metodu za postavljanje ili stvaranje sloja baze podataka. Ako sloj nije uspješno postavljen, prekida se. Ukoliko dock widget ne postoji, stvara se novi. Zatim se signal za promjenu selekcije na ciljnom sloju povezuje s metodom za popunjavanje forme. Na kraju, dock widget se dodaje u desno područje QGIS prozora i prikazuje korisniku.

* `QDockWidget(...)`: klasa iz PyQt5 koja stvara poseban prozor (widget) koji se može primijeniti na rubove glavnog prozora aplikacije, pomicati ili ostaviti da lebdi. Tako se forma lako integrirala u QGIS sučelje, umjesto da bude odvojeni, lebdeći prozor.
* `self.dock_widget.setWidget(self.dialog)`: Postavlja prethodno stvoreni dijalog (formu za unos) kao glavni sadržaj unutar `QDockWidget`-a.
* `self.dialog.pushButtonExport.clicked.connect(...)`: još jedan primjer povezivanja signala i utora. Ovdje se signal `clicked` (koji se emitira pri kliku mišem) gumba `pushButtonExport` (koji je definiran u `.ui` datoteci i dostupan preko `self.dialog` objekta) povezuje s metodom `exportToPdf`.
* `self.target_layer.selectionChanged.connect(...)`: iznimno važna naredba iz QGIS API-ja. Ona povezuje signal `selectionChanged` vektorskog sloja s metodom `populate_form_from_selection`. To znači da će QGIS automatski pozvati metodu svaki put kada korisnik na karti odabere ili odznači neki poligon na sloju Stratigrafske\_Jedinice, omogućujući dinamičko popunjavanje forme.

#### `populate_form_from_selection(self)`
Ova se metoda poziva svaki put kada se promijeni selekcija na ciljnom sloju. Ako je odabran točno jedan objekt, njegovi podaci se učitavaju u formu za unos. U suprotnom, ako nije odabrano, forma se čisti, omogućava jasnu promjenu i informacije podataka.

* `self.target_layer.selectedFeatures()`: metoda QGIS vektorskog sloja koja vraća listu svih trenutno odabranih objekata (u QGIS terminologiji, "features") na tom sloju. Tako se vraćaju podaci poligona kojeg je korisnik upravo odabrao.
* `feature.attribute(field.name())`: je metoda QGIS objekta (feature) koja dohvaća vrijednost njegovog atributa za zadani naziv polja. Unutar petlje, ova se metoda koristi za iterativno čitanje svih atributa odabranog poligona i njihovu pohranu za daljnju obradu.

#### `save_data_to_layer(self)`
Ova metoda sprema podatke unesene u formu u ciljni sloj. Kao geometriju za novi unos koristi geometriju trenutno odabranog poligona na aktivnom sloju, čime se osigurava da novi zapis ima prostornu komponentu.

* `self.iface.messageBar().pushMessage(...)`: Prikazuje informativnu poruku korisniku u traci za poruke na vrhu QGIS prozora. Korištena je za pružanje povratnih informacija o uspjehu ili greška operacija, što je bolja praksa od korištenja standardnih iskačućih prozora.
* `self.iface.activeLayer()`: Pozivom ove funkcije/metode dohvaća se referenca na trenutno aktivni (selektirani) sloj unutar QGIS panela, što omogućuje daljnju selekciju specifičnog poligona radi korištenja njegove geometrije.
* `isinstance(..., QgsVectorLayer)`: služi za provjeru pripadnosti objekta određenoj klasi. Njenom se primjenom osigurava da je aktivni sloj doista vektorskog tipa, što je nužan korak validacije prije pokušaja dohvata poligonskih objekata.
* `selected_features[0].geometry()`: Dohvaća geometrijski objekt (u ovom slučaju, poligon) iz odabranog feature-a. Geometrija sadrži sve informacije o obliku i položaju poligona u prostoru.
* `self.target_layer.startEditing()`: Pokreće sesiju uređivanja na sloju. U QGIS-u, sve promjene na podacima (dodavanje, brisanje, izmjena) moraju se odvijati unutar ovakve sesije.
* `QgsFeature()`: Stvara novi, prazan QGIS objekt (feature) koji se kasnije može popuniti podacima i geometrijom te dodati u sloj.
* `feature.setGeometry(...)`: Ova metoda služi za definiranje geometrije novostvorenog feature objekta, pri čemu se kao ulazni podatak koristi geometrija preuzeta s prethodno odabranog poligona.
* `feature.setAttribute(...)`: Postavlja vrijednost atributa za novostvoreni feature u odgovarajuće polje.
* `self.target_layer.addFeature(...)`: Dodaje popunjeni feature u sloj. U ovom trenutku, promjena je još uvijek samo privremena, unutar sesije uređivanja.
* `self.target_layer.commitChanges()`: Trajno sprema sve promjene napravljene unutar sesije uređivanja u izvornu datoteku (GeoPackage).
* `self.target_layer.rollBack()`: Poništava sve promjene napravljene unutar sesije ako je došlo do greške prilikom dodavanja feature-a, osiguravajući integritet podataka.

#### `exportToPdf(self)`
Ova metoda pokreće proces izvoza podataka u PDF format za trenutno odabrani objekt. To se postiže pozivanjem vanjske funkcije `export_to_pdf`, kojoj se prosljeđuju potrebni podaci.

#### `setup_database_layer(self)`
Ova ključna metoda provjerava postoji li u projektu sloj pod nazivom Stratigrafske\_Jedinice(koji se kreira tijekom pokretanja plugina). Ako sloj ne postoji, metoda stvara novu GeoPackage bazu podataka (`ArheologijaDB.gpkg`) i unutar nje novi sloj s unaprijed definiranim poljima koja su potrebna za unos arheoloških podataka.

* `QgsProject.instance()`: Vraća instancu trenutno otvorenog QGIS projekta, omogućujući pristup svim njegovim dijelovima, poput liste slojeva.
* `.mapLayersByName(layer_name)`: Metoda `QgsProject` objekta koja pretražuje sve slojeve u projektu po zadanom imenu i vraća listu pronađenih slojeva.
* `QgsVectorLayer(...)`: konstruktor koji stvara objekt vektorskog sloja iz izvora podataka. Specifična sintaksa `"{putanja}|layername={ime}"` se koristi za učitavanje točno određenog sloja iz GeoPackage datoteke koja može sadržavati više slojeva.
* `layer.isValid()`: Metoda koja provjerava je li sloj uspješno učitan i ispravan. Važna provjera kako bi se izbjegle greške ako je datoteka oštećena ili putanja nije ispravna.
* `.addMapLayer(layer)`: Metoda `QgsProject` objekta koja dodaje sloj u trenutni projekt, čineći ga vidljivim u panelu slojeva i na karti.
* `QgsField(...)`: Klasa koja definira jedno polje (stupac) za tablicu atributa, specificirajući njegov naziv i tip podatka.
* `QVariant.Int`, `QVariant.String`, itd.: Ovo su enumeracije tipova podataka iz Qt okvira koje se koriste za definiranje tipa polja u QGIS sloju (npr. cijeli broj, tekst, decimalni broj).

### ArheologijaPlus_dialog.py
Ova datoteka definira logiku iza korisničkog sučelja (forme) za unos podataka. Povezuje elemente sučelja (polja za unos, potvrdne okvire itd.) definirane u `ArheologijaPlus_dialog_base.ui` s Python kodom, omogućujući čitanje podataka iz forme i postavljanje podataka u nju.

#### `__init__(self, parent=None)`
Ovo je konstruktor klase dijaloga. On dinamički učitava `.ui` datoteku, većim dijelom kreirana u Qt Designeru, i iz nje stvara Python klasu. Nakon pozivanja konstruktora nadređene klase, metoda `setupUi(self)` postavlja sve elemente korisničkog sučelja, poput gumba i polja za unos, unutar samog dijaloga.

* `uic.loadUiType(...)`: korisna funkcija iz PyQt5 koja u stvarnom vremenu učitava `.ui` datoteku (koja je u XML formatu) i od nje dinamički stvara Python klasu u memoriji. Ovo je bitno za povezivanje vizualnog dizajna, napravljenog u Qt Designeru, s Python kodom, bez potrebe za ručnim pisanjem koda za svaki gumb i polje.
* `QtWidgets.QDialog`: osnovna klasa iz PyQt5 biblioteke za sve dijaloge, odnosno samostalne prozore. Klasa `ArheologijaPlusDialog` nasljeđuje ovu klasu kako bi imala svu osnovnu funkcionalnost prozora (npr. naslovnu traku, mogućnost zatvaranja).
* `self.setupUi(self)`: metoda koja dolazi iz klase stvorene pomoću `loadUiType`. Inicijalizira i postavlja sve widgete (gumbe, polja za unos, tabove...) definirane u `.ui` datoteci unutar dijaloga, čineći ih dostupnima u kodu (npr. kao `self.pushButtonSave`).

#### `get_data(self)`
Ova metoda prikuplja sve podatke koje je korisnik unio u formu i vraća ih kao rječnik (dictionary). Za svaki element sučelja (widget) koristi se odgovarajuća metoda za dohvaćanje njegove vrijednosti.

* `.value()`: Ova metoda se koristi za widgete koji se koritsti brojevima, kao što su `QSpinBox` i `QDoubleSpinBox`. Ona vraća trenutnu numeričku vrijednost koju je korisnik unio ili odabrao.
* `.currentText()`: Koristi se za `QComboBox` (padajući izbornik). Vraća tekstualni sadržaj trenutno odabrane stavke kao string, što je pogodno za spremanje u bazu podataka.
* `.text()`: Ova metoda se koristi za `QLineEdit`. Vraća cjelokupni tekst koji se trenutno nalazi u polju kao string.
* `.date()`: Koristi se za `QDateEdit` (widget za odabir datuma). Vraća `QDate` objekt koji predstavlja trenutno odabrani datum, a koji se kasnije može formatirati ili spremiti.
* `.isChecked()`: Primjenjuje se na `QCheckBox`. Vraća logičku (boolean) vrijednost: `True` ako je okvir označen, a `False` ako nije.
* `.toPlainText()`: Koristi se za `QTextEdit` ili `QPlainTextEdit`. Vraća cjelokupni tekst iz polja kao običan string, bez ikakvih informacija o stiliziranju.

#### `Set_data(self,data)`
Ova metoda popunjava formu s podacima iz prosljeđenog rječnika data, a obično se poziva kada korisnik odabere postojeći objekt na karti koji je već ispunjen.

* `.setValue()`, `.setCurrentText()`, `.setText()`, `.setDate()`, `.setChecked()`: Služe za postavljanje njihovog stanja ili vrijednosti. Njihovom primjenom vrši se programsko popunjavanje forme podacima preuzetim iz atributa odabranog QGIS objekta, što korisniku omogućuje pregled i naknadnu izmjenu postojećih podataka.

#### `clear_data(self)`
Ova metoda čisti sva polja u formi, vraćajući ih na početno, prazno stanje. Poziva se kada korisnik poništi odabir objekta na karti ili kada treba pripremiti formu za potpuno novi unos.

* `.setCurrentIndex(0)`: Ova metoda postavlja odabir u padajućem izborniku (`QComboBox`) na prvi element (indeks 0), što je način resetiranja kontrole.
* `.clear()`: Jednostavna metoda koja briše sav tekst iz tekstualnog polja.
* `QDate.currentDate()`: Ova metoda dohvaća trenutni sistemski datum u obliku `QDate` objekta. Njena primjena, prilikom resetiranja sučelja, omogućuje automatsko postavljanje polja za unos datuma na tekući dan, čime se olakšava i ubrzava korisnički unos.

### ArheologijaPlus_dialog_base.ui
`ArheologijaPlus_dialog_base.ui` je XML datoteka kreirana pomoću alata Qt Designer. Ona ne sadrži izvršnu logiku, već isključivo definira vizualni izgled i strukturu korisničkog sučelja za unos podataka. Datoteka specificira koji se sve widgeti (gumbi, polja za unos, tabovi, itd.) nalaze na formi, njihova svojstva (veličinu, naziv, tekst), te njihov međusobni raspored. Ovakav pristup odvaja dizajn sučelja od programske logike.

### export_pdf.py
Ova datoteka sadrži svu logiku potrebnu za generiranje detaljnog PDF izvještaja za pojedinačnu stratigrafsku jedinicu. Koristi vanjsku biblioteku `reportlab` za stvaranje i strukturiranje PDF dokumenta, te QGIS API za dinamičko generiranje slike karte odabranog poligona.

#### `_export_image(iface, feature)`
Ova Python funkcija, nazvana `_export_image`, služi za automatsko generiranje slikovne datoteke (PNG) koja prikazuje određeni geografski objekt (`feature`) s karte. Funkcija koristi QGIS-ov sustav za izradu ispisa (Layout) kako bi stvorila vizualno uredan prikaz objekta s malom marginom oko njega, koristeći sve slojeve koji su trenutno vidljivi na glavnoj karti u QGIS-u.

* `QgsLayout(...)`: Stvara novi, prazan layout (prikaz za ispis) unutar QGIS projekta. Layout je poput praznog papira na koji se mogu dodavati elementi poput mapa, legendi i teksta.
* `QgsLayoutItemMap(...)`: Stvara mapu kao jedan od elemenata koji se može dodati u layout.
* `feature.geometry().boundingBox()`: Ova metoda vraća minimalni prostorni obuhvat koji u potpunosti sadržava geometriju zadanog objekta. Njena primjena omogućuje automatsko definiranje područja prikaza na karti, čime se osigurava da je odabrani poligon pozicioniran u središtu i vidljiv u cijelosti.
* `item.setExtent(...)`: Postavlja geografski obuhvat (granice) koji će biti prikazan u mapi unutar layouta.
* `QgsLayoutExporter(...)`: Klasa iz QGIS API-ja koja upravlja procesom izvoza (exporta) layouta u različite formate, poput slike ili PDF-a.
* `exporter.exportToImage(...)`: Konkretna metoda koja izvršava izvoz cijelog layouta u slikovnu datoteku na zadanu putanju, s definiranim postavkama kvalitete.

#### `export_to_pdf(dlg, iface, selected_feature)`
Ovo je glavna funkcija za izvoz koja se poziva iz glavnog modula dodatka. Prvo prikuplja sve podatke iz forme za unos i pita korisnika gdje želi spremiti PDF datoteku. Zatim registrira potrebne fontove koji omogućuju ispravan prikaz hrvatskih znakova. Cilj funkcije je slaganje PDF dokumenta element po element, koristeći `reportlab` tablice i paragrafe kako bi se replicirao izgled standardnog obrasca. Na kraju, generira konačni PDF dokument.

* `QFileDialog.getSaveFileName(...)`: Metoda iz PyQt5 koja prikazuje standardni sistemski dijalog za spremanje datoteke. Omogućuje korisniku da odabere lokaciju i naziv za svoj PDF.
* `pdfmetrics.registerFont(TTFont(...))`: biblioteke koja omogućuje registraciju vanjskog `.ttf` fonta za korištenje unutar dokumenta. Njenom primjenom uvodi se font DejaVu Sans, čime se, zahvaljujući njegovoj podršci za hrvatske dijakritičke znakove (č, ć, ž, š, đ), osigurava ispravan prikaz teksta u generiranom PDF-u.
* `SimpleDocTemplate(...)`: Osnovna klasa iz ReportLab-a koja predstavlja čitav PDF dokument. Inicijalizira dokument s određenom veličinom stranice (A4) i marginama.
* `Table`, `Paragraph`, `Spacer`, `PageBreak`, `ReportLabImage`: predstavljaju osnovne gradivne elemente (tzv. Flowables) za izgradnju strukture PDF dokumenta. Njihovim kombiniranjem oblikuje se složeni sadržaj obrasca, pri čemu `Table` služi za tablični prikaz, `Paragraph` za tekstualne odlomke, `Spacer` za stvaranje vertikalnog razmaka, `PageBreak` za prijelom stranice, a `ReportLabImage` za umetanje prethodno generirane slike karte.
* `doc.build(elements)`: Ključna metoda ReportLab dokumenta. Ona uzima listu svih prethodno pripremljenih elemenata (tablica, tekstova, slika) i iscrtava ih redom u PDF datoteku, stvarajući konačni dokument.

## Funkcionalnosti plugina
Funkcionalnosti ArheologijaPlus plugina proizlaze iz njegove arhitekture i dizajna korisničkog sučelja. Plugin korisniku omogućuje sljedeće ključne stvari:

* **Unos i uređivanje arheoloških podataka**
    kroz bogatu formu (dock panel) korisnik može unijeti sve potrebne informacije o jednoj stratigrafskoj jedinici ili kontekstu iskopavanja. To uključuje deskriptivne podatke, prostorne odnose i bilješke o nalazima. Forma u suštini zamjenjuje papirnati obrazac za SJ, čineći podatke odmah digitalno dostupnima. Korisnik može ispunjavati polja proizvoljnim redoslijedom.

* **Spremanje podataka u QGIS projekt**
    pritiskom na gumb "Spremi u projekt" (implementiran kroz `pushButtonSave`) korisnik može trajno pohraniti unesene podatke unutar trenutnog QGIS projekta. To znači da su podaci vezani uz `.qgz` datoteku i bit će dostupni sljedeći put kada se taj projekt otvori. Ova funkcionalnost je izuzetno korisna u praksi arheološki tim može imati QGIS projekt za cijelo iskopavanje. Kada se za par dana nastavi rad ili netko drugi preuzme dokumentaciju, dovoljno je otvoriti projekt svi prethodno uneseni podatci ću biti tu.

* **Integracija s QGIS GUI**
    plugin se uklapa u QGIS korisničko sučelje. Nakon instalacije, korisnik ga pronalazi u izborniku `Dodaci (Plugins)` pod kategorijom "ArheologijaPlus", a može ga staviti i na toolbar radi bržeg pristupa. Klikom na opciju otvara se bočni panel (dock widget) pod nazivom "Arheologija Plus". Taj panel se ponaša kao i ostali QGIS paneli može se usidriti uz rub prozora, promijeniti mu veličinu, minimizirati ili odvojiti. Ovakva integracija je važna jer omogućuje korisniku da istovremeno gleda prostornu situaciju na karti i unosi podatke. Kada se podaci uspješno spreme ili učitaju, na vrhu QGIS prozora iskače zelena traka s porukom "Novi unos je spremljen", što je standardni QGIS način obavještavanja (tzv. message bar ili toast). U slučaju greške (primjerice, nedostaju fontovi za PDF), plugin generira crvenu error poruku na istom mjestu.

* **Izvoz dokumentacije u PDF**
    jedna od značajki je automatsko kreiranje PDF izvještaja. Klikom na gumb "Export" u sučelju plugina, korisnik pokreće proceduru generiranja PDF-a. Tada se od njega traži da odabere lokaciju i naziv datoteke na disku. Nakon potvrde, plugin prikuplja sve unesene podatke i slaže PDF dokument koji je formatiran kao standardizirani list stratigrafske jedinice. U tom PDF-u, na jednom listu A4 formata, nalaze se svi bitni podaci: u zaglavlju broj SJ i osnovne informacije o lokalitetu i datumu, zatim blok za podatke o poziciji (sonda, sektor, kvadrat, visine), blok za opisne karakteristike (sastav, boja, konzistencija, oblik i dimenzije), te dalje rubrike za stratigrafske odnose i nalaze. Tekstualni opisi (Općeniti opis, Bilješke) bit će ispisani u za njih predviđenim poljima više linijski. Konačan PDF je digitalna verzija terenskog konteksta formulara te odgovara standardima dokumentacije. Prednost je što se ovakav PDF može odmah pohraniti u projektni arhiv, S obzirom da ReportLab generira PDF programatski, potencijal za grešku u prepisivanju podataka s papira eliminiran je ono što je uneseno u plugin završi u izvješću točno kako je upisano.

* **Visoka prilagodljivost i proširivost**
    arhitektura plugina je takva da se mogu dodavati nove funkcionalnosti bez velikih zahvata u postojeći kod. Primjer je već izdvojeni modul za PDF, primjerice, može se dodati modul za izvoz u Excel/CSV (za statističku analizu) ili modul za sinkronizaciju podataka s vanjskom bazom podataka (npr. slanje zapisa u PostgreSQL/PostGIS bazu na serveru).

## Analiza postojećih ograničenja
Korištenje GeoPackage (`.gpkg`) datoteke kao primarnog spremnika podataka optimalno je za individualne projekte. Takav pristup postaje limitirajući faktor u kolaborativnim okruženjima gdje više istraživača istovremeno radi na istom projektu. Nedostatak mehanizma za simultani više korisnički pristup može dovesti do konflikata u verzijama podataka i otežava centralizirano upravljanje. Potrebna je nadogradnja plugina kako bi podržavao povezivanje na centralizirane sustave za upravljanje bazama podataka, prvenstveno PostgreSQL s PostGIS ekstenzijom. Time bi se omogućio siguran i efikasan višekorisnički rad, centralizirano upravljanje podacima te bi se značajno poboljšala skalabilnost sustava za velike projekte.

U trenutnoj verziji ne implementira naprednu validaciju korisničkog unosa. To otvara mogućnost za unos nekonzistentnih ili netočnih podataka (npr. unos teksta u numerička polja), što dugoročno može pokvariti kvalitetu i pouzdanost cjelokupne baze podataka. Nužno je implementirati pravila za validaciju unosa na razini korisničkog sučelja. Nadalje, preporučuje se uvođenje kontroliranih rječnika za deskriptivna polja (npr. boja, sastav tla) kako bi se osigurala terminološka uniformnost i olakšale buduće analize.

Funkcionalnost izvoza podataka isključivo u PDF format zadovoljava potrebe generiranja standardiziranih izvještaja, ali ograničava daljnju obradu i analizu. Nedostatak opcija za izvoz u strojno čitljive formate, poput CSV-a ili JSON-a, otežava integraciju s drugim analitičkim i statističkim alatima. Potrebno je proširiti funkcionalnosti izvoza. Razmatranje implementacije modula za uvoz podataka iz drugih izvora također bi povećalo fleksibilnost plugina.

Suvremena arheološka dokumentacija u velikoj mjeri ovisi o vizualnim zapisima. Trenutna verzija ne omogućuje pridruživanje fotografija, crteža ili drugih multimedijalnih datoteka zapisima o stratigrafskim jedinicama, čime se gubi važan sloj kontekstualnih informacija. Potrebno je implementirati funkcionalnost koja bi korisnicima omogućila povezivanje vanjskih datoteka (slika, dokumenata) s pojedinim zapisima u bazi podataka, čime bi se stvorio cjelovit digitalni arhiv stratigrafske jedinice.

## Zaključak
Razvoj plugina ArheologijaPlus pokazuje kako se suvremena arheološka metodologija može unaprijediti integracijom digitalnih alata unutar GIS okruženja. Ovaj plugin konkretno rješava potrebe dokumentiranja stratigrafskih jedinica i drugih terenskih podataka, pružajući arheolozima jedno objedinjeno sučelje za unos, spremanje i izvoz podataka. Prednosti takvog pristupa su višestruke. Poboljšana učinkovitost i točnost unosa podataka izravno na terenu u digitalni oblik smanjuje dvostruki posao (ručni zapis pa naknadno pretipkavanje) i minimizira greške koje se pri tome mogu pojaviti. Korištenje strukturiranog formulara u pluginu osigurava da istraživač ne zaboravi zabilježiti nijednu važnu kategoriju podatka (jer su sve rubrike pred njim). Istovremeno, jednom uneseni podaci lako su pretraživi i usporedivi. Plugin osigurava da su zapisi formata uniformni, što je bitno kad više ljudi radi na projektu ili kad se podaci dijele s drugima. Generiranjem PDF obrazaca koji prate standarde struke, digitalna dokumentacija postaje ravnopravna zamjena papirnatoj, može se i višestruko kopirati bez gubitka kvalitete, slati elektronički i uključivati u digitalne izvještaje. Elektronička baza podataka stratigrafskih jedinica uz prostorne reference stvara temelje za naprednije analize. Arheološki podaci su neponovljivi jer se iskop ne može ponoviti, stoga uz ArheologijaPlus puno je lakše zabilježiti ih na najbolji mogući način. Spoj GIS-a i specifičnih plugina, kao što je ArheologijaPlus, predstavlja korak naprijed prema toj svrsi.

## Literatura
* Spatial without Compromise · QGIS Web Site. https://qgis.org/
* Documentation for QGIS 3.40 — QGIS Documentation documentation. https://docs.qgis.org/3.40/en/docs/index.html
* PyQGIS Developer Cookbook — QGIS Documentation documentation. https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html
* Riverbank Computing | Introduction. https://www.riverbankcomputing.com/software/pyqt/
* reportlab. PyPI. https://pypi.org/project/reportlab/
* HRyohni.GitHub - HRyohni/Arheologija: Arheologija. GitHub. https://github.com/HRyohni/Arheologija
