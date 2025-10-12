# ATL Tõlkeabistaja - Otsuste Dokument

**Versioon:** 1.0
**Kuupäev:** 2025-10-12
**Projekti asukoht:** `/home/d0021/Automation/ATL_tõlkeprojekt/`

---

## 📋 Projekti Ülevaade

**Nimi:** ATL Tõlkeabistaja
**Eesmärk:** Automatiseerida ja süstematiseerida ATL (Alkohoolikute Täiskasvanud Lapsed) materjalide tõlkimist inglise keelest eesti keelde

**Tehniline lahendus:**
- Keel: Python
- Esimene versioon: Terminali/käsurea rakendus (interaktiivne)
- Tulevik: Veebirakendus
- Lõppsiht: Kingitus ATL-ile, et kõik saaksid kasutada

**Failiformaadid:**
- Sisend: `.docx` ja `.txt` failid
- Väljund: samad formaadid (tõlgitud või märgendatud)

---

## 🎯 Etapid

### ETAPP 1: Terminibaasi Ehitamine 🔄 POOLELI

**Eesmärk:** Luua põhjalik terminibaas ACA/ATL terminoloogia jaoks süstemaatilise kõrvutamise kaudu

**Süstemaatiline lähenemine:**

#### 1A. EKI Terminibaasid ✅ VALMIS
- ✅ Skeemiteraapia terminisõnastik (`skt`) - 250 terminit
- ✅ DKT/DBT terminibaas (`dkt`) - 301 terminit
- ✅ Kriisinõustamise terminibaas (`kriis`) - 82 terminit
- ✅ Tervisesõnastik (`TAI`) - 645 terminit
- 🎉 **KOKKU: 1,278 terminit kogutud**
- 📊 **Glossary jaoks kasutatavad: 1,265 terminit** (eesti + inglise keeles)
- 🔧 **Tööriist:** `src/eki_koguja.py`
- 📁 **Asukoht:** `data/eki_terminid/*.json`
- 📋 **Andmed:** keel, sünonüümid, definitsioonid, lingid EKI lehele
- 📅 **Kogutud:** 2025-10-12

#### 1B. Glossary Terminid Kõrvutamine EKI-ga 📍 PRAEGU
- 📍 **Asukoht:** `/home/d0021/Documents/ATL_drive/Jagatud/Glossary_templatesonavara.docx`
- 📊 **Termineid kokku: 845** (210 täidetud + 635 tõlkimata)
- 📄 **Analüüs:** `data/glossary_analüüs.json`
- 🔄 **Protsess:**
  1. Võta KÕIK Glossary terminid (845 tk)
  2. Kõrvuta iga termin EKI 1,265 terminiga
  3. **KUI MATCH → täienda EKI vastega + viitega EKI lehele**
  4. **KUI EI MATCH → jäta tühjaks** (täidetakse hiljem)
- ⚠️ **IMPORTANT!** Glossary "draft" tõlked pole usaldusväärsed - EKI vaste asendab need

#### 1C. Päevatekstid Kõrvutamine EKI-ga ⏳ JÄRGMINE
- 📝 **Allikas:** Olemasolevad ATL päevamõtted (originaal + tõlge paaris)
- 🔄 **Protsess:**
  1. Ekstraheeri originaal + tõlge paarid
  2. Kõrvuta EKI terminibaasiga
  3. **KUI MATCH → täienda EKI vastega + viitega**
  4. Lisa ka päevatekstist leitud tõlge (võib erineda EKI-st)
- 📝 **Märkus:** Need sisaldavad praktiliselt testitud tõlkeid

**Terminibaasi andmestruktuur:**

Iga termin sisaldab:
- 🇬🇧 **Ingliskeelne termin** (nt "Inner Child")
- 🇪🇪 **Eestikeelne vaste(d)** - võib olla mitu varianti erinevatest allikatest:
  - **EKI vaste** + viide EKI lehele (autoriteetne allikas)
  - **Päevateksti tõlge** + viide kuupäevale (praktiliselt testitud)
  - **Glossary draft** (esialgne tõlge, vajab kontrollimist)
- 📝 **Kommentaarid/selgitused** (kontekst, nüansid)
- 📚 **Näited kasutusest** (laused originaaltekstidest ja tõlgetest)
- 🔗 **Allikate kategooriad** (EKI / päevatekst / draft)
- 🏷️ **Teemad** (nt "12-step terminology", "therapy", "emotions")
- ⭐ **Kinnituse staatus** (kas on ametlikult heaks kiidetud)
- ❓ **TODO: Eelistatud variant** - kui on mitu vastet, kuidas märkida eelistatud/kasutusel olev variant? (vajab läbimõtlemist)

**Terminibaasi formaat:**
- ❓ **Vajab otsust:** SQLite / JSON / CSV / muu?
  - **SQLite** - struktureeritud andmebaas, hea päringu võimalused, valmis veebirakenduseks
  - **JSON** - inimesele loetav, lihtne versioonihaldusse, hea varukoopiate jaoks
  - **CSV** - lihtsaim, saab Excelis/Google Sheets avada ja muuta

---

### ETAPP 2: Tõlkeabistaja Tööriist 📅

**Eesmärk:** Automatiseerida tõlkeprotsessi, kasutades Etapp 1-s loodud terminibaasi

**Sisend:**
- Uus ingliskeelne tekst (`.docx` või `.txt`)
- Terminibaas (Etapp 1-st)

**Funktsioonid:**

1. **Terminite tuvastamine**
   - Leia tekstist kõik teadaolevad terminid terminibaasist
   - Tuvasta ka variatsioonid (nt ainsus/mitmus, käänded)

2. **Visualiseerimine**
   - Kuva terminite asukohad tekstis
   - Märgi ära, kas termin on juba tõlgitud või mitte

3. **Tõlkevariantide pakkumine**
   - Näita kinnitatud tõlkevasteid
   - Näita näiteid varasematest tõlgetest
   - Kui on mitu varianti, las kasutaja valib

4. **Abistamine tõlkimisel**
   - Interaktiivne režiim: käi läbi kõik terminid ükshaaval
   - Lase kasutajal valida või sisestada uus tõlge
   - Salvesta uued tõlked terminibaasi

5. **Väljund**
   - Tõlgitud tekst koos märkustega
   - Raport: millised terminid leiti, millised tõlgiti, millised jäid tõlkimata

**Kasutajaliides:**
- **V1 (praegu):** Terminali/käsurea rakendus (interaktiivne)
- **V2 (tulevik):** Veebirakendus (ATL-ile kingitus)

---

## ❓ Avatud Küsimused ja Otsused

### Etapp 1 jaoks:

1. **Päevamõtete asukoht ja struktuur**
   - ❓ Kus asuvad originaal + tõlge failid?
   - ❓ Mis formaadis (docx, txt, paarid)?
   - ❓ Kuidas organiseeritud (kuupäevade kaupa, kõik ühes failis)?

2. **Glossary template struktuur**
   - ❓ Mis struktuur on `.docx` failil?
   - ❓ Kas loeme faili sisse ja vaatame?
   - ❓ Või loome struktuuri ise?

3. **Terminibaasi formaat**
   - ❓ SQLite vs JSON vs CSV?
   - 💡 **Soovitus:** JSON (lihtne alustada, loetav, git-sõbralik) + SQLite tulevikus

4. **Terminite tuvastamise strateegia**
   - ❓ Kas on ACA-spetsiifiline sõnastik termineid?
   - ❓ Või otsime automaatselt korduvad/suurtähega terminid?
   - 💡 **Võimalik lähenemine:** Kombinatsioon - alusta käsitsi valitud põhiterminitega (Inner Child, Higher Power, etc.) ja laienda automaatselt

### Etapp 2 jaoks:

5. **Tõlke töövoog**
   - ❓ Kas kasutaja tahab ise vaadata kõik terminid läbi?
   - ❓ Või automaatne asendamine kinnitatud terminite puhul?
   - 💡 **Soovitus:** Alati küsi kasutajalt kinnitust

6. **Failihaldus**
   - ❓ Kuidas salvestada tõlgitud tekstid?
   - ❓ Kas säilitada originaali ja luua uus fail?
   - ❓ Versioonihaldus?

---

## 📦 Projekti Struktuur (kavand)

```
ATL_tõlkeprojekt/
├── OTSUSED.md                 # See dokument
├── README.md                  # Projekti ülevaade ja kasutusjuhend
├── requirements.txt           # Python sõltuvused
│
├── src/                       # Lähtekood
│   ├── terminibaas/          # Terminibaasi loomine (Etapp 1)
│   │   ├── ekstrakteeri_paevamotted.py
│   │   ├── ekstrakteeri_eki.py
│   │   └── ehita_terminibaas.py
│   │
│   └── tolkeabistaja/        # Tõlkeabistaja (Etapp 2)
│       ├── leia_terminid.py
│       ├── tolgi_tekst.py
│       └── cli.py            # Käsurea liides
│
├── data/                      # Andmed
│   ├── terminibaas.json      # Põhiline terminibaas
│   ├── eki_terminid/         # EKI-st kogutud terminid
│   └── paevamotted/          # Tõlgitud päevamõtted (koopiad)
│
└── tests/                     # Testid (tulevikus)
```

---

## 🚀 Järgmised Sammud

### Kohe praegu:

1. ✅ **Kausta loomine** - `/home/d0021/Automation/ATL_tõlkeprojekt/`
2. ✅ **Otsuste dokumendi loomine** - See fail

### Järgmiseks:

3. ⏳ **Glossary template uurimine**
   - Loe sisse: `/home/d0021/Documents/ATL_drive/Jagatud/Glossary_templatesonavara.docx`
   - Uuri struktuuri
   - Otsusta andmemudel

4. ⏳ **Päevamõtete asukoha täpsustamine**
   - Kus asuvad originaal + tõlge failid?
   - Kuidas organiseeritud?

5. ⏳ **Terminibaasi formaadi otsus**
   - SQLite / JSON / CSV?

6. ⏳ **Projekti README loomine**
   - Ülevaade
   - Paigaldusjuhend
   - Kasutusjuhend

---

## 🔧 Tehnilised Otsused

### OTSUS: EKI Terminite Keelefilter Glossary Töös

**Kuupäev:** 2025-10-13

**Olukord:** EKI terminibaasid sisaldavad termineid mitmes keeles (eesti, inglise, vene, soome)

**Otsus:**
- Kõik kogutud terminid jäävad JSON failidesse alles
- Glossary võrdluseks kasutame ainult eesti ja inglise keeles termineid
- Vene, soome ja muud keeled jäävad arhiivi võimalikuks tulevikukasutuseks

**Põhjendus:**
- ATL materjalid on inglise → eesti tõlge
- Vajame inglise termineid (originaal) ja eesti vasteid (tõlge)
- Vene/soome terminid pole ATL tõlketöö jaoks esialgu vajalikud
- Säilitame kõik andmed - võib tulevikus kasulik olla

**Praktiline tegevus:**
- Filtreerin EKI andmeid analüüsimisel: ainult `keel === "eesti"` VÕI `keel === "inglise"`
- JSON failid jäävad täielikud (kõik keeled säilitatud)

---

## 📝 Märkmed

- **ADHD-sõbralik:** Järgi CODING_PRINCIPLES.md põhimõtteid
- **MVP lähenemine:** Alusta lihtsast, laienda järk-järgult
- **Läbipaistvus:** Dokumenteeri kõik otsused ja põhjused
- **Kingitus ATL-ile:** Lõppeesmärk on jagada kogukonnaga

---

**Viimati uuendatud:** 2025-10-13
**Uuendaja:** Claude AI + Kasutaja
