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

## 🎯 Development Milestones

**For detailed milestone descriptions, see [PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)**

**Current Status:**
- ✅ **Milestone 1A:** EKI Terminology collected (1,265 terms)
- 📍 **Milestone 1B:** Glossary matching with EKI (in progress)
- ⏳ **Milestone 1C:** Extract from daily meditations (next)
- 💡 **Milestone 1D:** Collaboration opportunities (optional)

**Summary:**
- **Milestone 1:** Terminology Database (foundation for everything)
- **Milestone 2:** Personal CLI Translation Assistant
- **Milestone 3:** Estonian Community Tool
- **Milestone 4:** Multi-Language Platform

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

### OTSUS: Failiformaadid (MVP vs Tulevikuplaanad)

**Kuupäev:** 2025-10-14

**MVP (V1):**
- ✅ `.docx` (Word dokumendid)
- ✅ `.txt` (lihttekst)
- 📝 **PDF failid** - esialgu kopeerin sisu käsitsi, pole probleemi (MVP lähenemine!)

**Tulevikus (kui vaja):**
- 📋 `.pdf` tugi automaatne (Python: PyPDF2, pdfplumber, pypdf)
- 📋 OCR tugi (skaneeritud/pildifailidest dokumendid - tesseract, pytesseract)

**Põhjendus:**
- MVP-first: keskendume põhifunktsioonidele
- PDF käsitsi kopeerimine ei ole praegu probleem
- Lisame täiendava võimekuse siis, kui see muutub vajalikuks

---

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

### OTSUS: GitHub Organization Structure

**Kuupäev:** 2025-10-14

**Milestones = Development Phases (3 major milestones)**
- Each milestone represents one complete phase of development
- Clear, high-level goals
- Human-readable names (not codes like "phase-1")

**Issues = Specific tasks**
- Concrete, actionable work items
- Can be assigned, tracked, closed
- Linked to milestones

**Labels = Categories within milestones**
- Group related issues together
- Examples: "terminology-database", "cli-tool", "documentation", "web-interface"
- Allow filtering and organization
- Multiple labels per issue possible
- Labels help organize issues WITHIN each milestone

**Why this works:**
- Simple and clear structure
- Not over-engineered
- Easy to understand at a glance
- Labels provide flexibility for grouping without rigid hierarchy
- Follows passion project philosophy (human-readable, not corporate)
- GitHub doesn't support sub-milestones, but labels achieve similar organization

---

## 💡 Tulevikuvisiooni (Future Ideas)

### 🌍 Universaalne Tõlkeplatvorm - Suur Unistus

**Visioon:** Muuta see ATL-spetsiifiline tööriist universaalseks, mitmekeelseks tõlkeplatvormiks, mida erinevad kogukonnad saaksid kasutada.

**Võimalused:**

#### 1. Veebipõhine Platvorm (Online + Offline)
- 🌐 **Veebipõhine liides** - ligipääsetav kõigile, kõikjal
- 💾 **Offline režiim** - töötab ka ilma internetita (PWA - Progressive Web App)
- 📱 **Responsiivne** - töötab nii arvutis, tahvlis kui telefonis

#### 2. Mitme Keelepaari Tugi
- 🇬🇧 → 🇪🇪 Inglise → Eesti (praegune fookus)
- 🇪🇪 → 🇫🇮 Eesti → Soome
- 🇬🇧 → 🇫🇮 Inglise → Soome
- 🇬🇧 → 🇸🇪 Inglise → Rootsi
- ...ja teised keelekombinatsioonid

#### 3. Organisatsiooni Haldus ja Kasutajaõigused
**ACA/ATL võiks:**
- 📤 **Tekstid üles laadida** platvormile
- 👥 **Kasutajate õiguste määramine:**
  - Tõlkijad (saavad tõlkida)
  - Ülevaatajad (saavad kinnitada/kommenteerida)
  - Administraatorid (haldavad projekte ja kasutajaid)
- ✅ **Ülevaatuse töövoog:**
  - Tõlkija teeb tõlke
  - Saadab ülevaatajale lihtsalt ühe linnukesega ✓
  - Ülevaataja saab kommenteerida, kinnitada või tagasi saata
- 📊 **Progressi jälgimine:**
  - Mitu teksti on tõlkimisel
  - Mitu ootab ülevaatust
  - Mitu on valmis

#### 4. Koostöö ja Versioonihaldus
- 👥 **Mitme tõlkija koostöö** samal tekstil
- 📝 **Kommentaarid ja arutelud** terminite kohta
- 🔄 **Versioonide ajalugu** - näed, kes mida muutis ja millal
- 🔀 **Tõlkevariantide võrdlemine** - vali parim variant

#### 5. Kogukonnale Avatud
- 🎁 **Tasuta kasutada** ACA/ATL-ile ja teistele 12-sammu kogukondadele
- 🌱 **Avatud lähtekoodiga** - teised võivad panustada ja täiendada
- 📚 **Terminibaasid jagatavad** - kogukonnad saavad oma terminibaase jagada
- 🔌 **API** - võimalus integreerida teiste süsteemidega

#### 6. Intelligentsed Funktsioonid
- 🤖 **Masintõlke integratsioon** (DeepL, Google Translate) - kui termin puudub
- 💡 **Automaatne terminite tuvastamine** - leiab uued terminid tekstist
- 📊 **Statistika ja analüütika** - millised terminid on kõige sagedamini kasutatud
- 🔍 **Otsing läbi kõigi projektide** - leia, kuidas termin on varem tõlgitud

### 🎯 Etapiline Teostus (Realistlik Plaan)

**Faas 1:** ATL-spetsiifiline CLI tööriist ✅ (praegu)
**Faas 2:** ATL-spetsiifiline veebiversioon (MVP)
**Faas 3:** Kasutajaõigused ja ülevaatuse töövoog
**Faas 4:** Mitme organisatsiooni tugi (multi-tenant)
**Faas 5:** Mitme keelepaari tugi
**Faas 6:** Avatud platvorm kõigile kogukondadele

### 💭 Miks See On Oluline

See pole lihtsalt tööriist - see on **kingitus kogukonnale**, mis:
- 🤝 Võimaldab kvaliteetsemat ja järjepidevamat tõlkimist
- ⚡ Kiirendab tõlkeprotsessi märkimisväärselt
- 👥 Hõlbustab koostööd tõlkijate ja ülevaatajate vahel
- 📚 Säilitab teadmisi ja parimaid praktikaid
- 🌍 Võib aidata paljusid teisi kogukondi üle maailma

**Eriti olulised on väikeste keelte rääkijad:**
- 🇪🇪🇫🇮🇮🇸🇱🇹🇱🇻🇲🇹 Väikestel keeltel on vähe tõlkeressursse
- Vähe professionaalseid tõlkijaid ja terminibaase
- Masintõlge halvem kui suurte keelte puhul
- See tööriist võiks pakkuda neile süstemaatilist lahendust

**Vabatahtlikud programmeerijad:**
- Kui prototüüp on valmis JA kasulik, saab teha ülemaailmse üleskutse
- Hästi dokumenteeritud projekt on lihtne kaasata teisi
- Selge eesmärk (aitab kogukonda) on motiveeriv

**"Ma teen seda, sest ma saan seda programmeerimisega teha - ja see on mu kingitus kogukonnale!"** 🎁❤️

---

## 📝 Märkmed

- **ADHD-sõbralik:** Järgi CODING_PRINCIPLES.md põhimõtteid
- **MVP lähenemine:** Alusta lihtsast, laienda järk-järgult
- **Läbipaistvus:** Dokumenteeri kõik otsused ja põhjused
- **Kingitus ATL-ile:** Lõppeesmärk on jagada kogukonnaga

---

**Viimati uuendatud:** 2025-10-14
**Uuendaja:** Claude AI + Kasutaja
