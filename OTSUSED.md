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

### ETAPP 1: Terminibaasi Ehitamine ⏳

**Eesmärk:** Luua põhjalik terminibaas ACA/ATL terminoloogia jaoks

**Allikad:**

1. **Olemasolevad ATL päevamõtted** (originaal + tõlge paaris)
   - 📍 **Staatus:** Asukoht vajab täpsustamist
   - 📝 **Märkus:** Need sisaldavad juba tehtud tõlkeid, millest saab õppida

2. **EKI terminibaasid** (Sõnaveeb korpused)
   - ✅ Skeemiteraapia terminisõnastik (`skt`) - https://sonaveeb.ee/ds/skt
   - ✅ DKT/DBT terminibaas (`dkt`) - https://sonaveeb.ee/ds/dkt
   - ✅ Kriisinõustamise terminibaas (`kriis`) - https://sonaveeb.ee/ds/kriis
   - ✅ Tervisesõnastik (`TAI`) - https://sonaveeb.ee/ds/TAI
   - 🔧 **Tööriist:** Olemas `kogub_terminid.sh` skript automatiseeritud kogumiseks

3. **Glossary template**
   - 📍 **Asukoht:** `/home/d0021/Documents/ATL_drive/Jagatud/Glossary_templatesonavara.docx`
   - 📝 **Praegune seisund:** Tühi
   - ❓ **Vajab:** Struktuuri uurimist

**Terminibaasi andmestruktuur:**

Iga termin sisaldab:
- 🇬🇧 **Ingliskeelne termin** (nt "Inner Child")
- 🇪🇪 **Eestikeelne vaste(d)** (nt "Sisemine laps", võib olla mitu varianti)
- 📝 **Kommentaarid/selgitused** (kontekst, nüansid)
- 📚 **Näited kasutusest** (laused originaaltekstidest ja tõlgetest)
- 🔗 **Lingid/viited** (kust termin pärineb - kuupäev, dokument, allikas)
- 🏷️ **Kategooria/teemad** (nt "12-step terminology", "therapy", "emotions")
- ⭐ **Kinnituse staatus** (kas on ametlikult heaks kiidetud tõlge või variant)

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

## 📝 Märkmed

- **ADHD-sõbralik:** Järgi CODING_PRINCIPLES.md põhimõtteid
- **MVP lähenemine:** Alusta lihtsast, laienda järk-järgult
- **Läbipaistvus:** Dokumenteeri kõik otsused ja põhjused
- **Kingitus ATL-ile:** Lõppeesmärk on jagada kogukonnaga

---

**Viimati uuendatud:** 2025-10-12
**Uuendaja:** Claude AI + Kasutaja
