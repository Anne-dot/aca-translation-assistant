# ACA Translation Assistant / ATL Tõlkeabistaja

**Translation assistant tool for Estonian ACA (Adult Children of Alcoholics) materials**

Tõlkeabistaja tööriist ATL (Alkohoolikute Täiskasvanud Lapsed) materjalide tõlkimiseks inglise keelest eesti keelde.

---

## 🎯 Eesmärk

See projekt loob süstemaatilise tööriista ACA/ATL terminoloogia haldamiseks ja materjalide tõlkimiseks, et:

- Hoida terminoloogiat järjepidevana
- Kiirendada tõlkeprotsessi
- Koguda kokku kinnitatud tõlkevasted
- Õppida olemasolevatest tõlgetest
- Jagada kogukonnaga (lõppeesmärk)

---

## 📋 Projekt

### Etapp 1: Terminibaasi Ehitamine (praegu arenduses)

Ehitame põhjaliku terminibaasi, mis kogub terminoloogiat:
- Olemasolevatest tõlgitud päevamõtetest
- EKI (Eesti Keele Instituut) terminibaasidest
- Professionaalsetest allikatest

### Etapp 2: Tõlkeabistaja (tulevikus)

Interaktiivne tööriist, mis:
- Leiab tekstist terminid
- Pakub kinnitatud tõlkevasteid
- Abistab tõlkimisel
- Õpib uutest tõlgetest

---

## 🚀 Staatus

**Hetkeseisund:** Planeerimine ja algne seadistus

- ✅ Projekti struktuur loodud
- ✅ Otsuste dokument koostatud
- ⏳ Terminibaasi andmemudel (arenduses)
- ⏳ Terminite ekstraktor (tulemas)

Vaata detailset plaani: [OTSUSED.md](OTSUSED.md)

---

## 🛠️ Tehnoloogia

- **Keel:** Python 3.x
- **Failiformaadid:** `.docx`, `.txt`
- **Terminibaas:** JSON (praegu), SQLite (tulevikus)
- **Interface:** CLI (käsurida) → Veebirakendus (tulevikus)

---

## 📁 Projekti Struktuur

```
ATL_tõlkeprojekt/
├── README.md                  # See fail
├── OTSUSED.md                 # Detailne otsuste dokument
├── requirements.txt           # Python sõltuvused (tulemas)
│
├── src/                       # Lähtekood (tulemas)
│   ├── terminibaas/          # Terminibaasi loomine
│   └── tolkeabistaja/        # Tõlkeabistaja
│
└── data/                      # Andmed (tulemas)
    └── terminibaas.json      # Terminibaas
```

---

## 📖 Dokumentatsioon

- **[OTSUSED.md](OTSUSED.md)** - Projekti otsused, plaan ja avatud küsimused
- **README.md** - See fail (projekti ülevaade)

---

## 🤝 Kaastöö

See projekt on arendamisel ja lõppeesmärk on anda see kingitusena ATL kogukonnale.

Praegu: privaatne arendus
Tulevikus: avalik repo koos kasutusjuhendiga

---

## 📝 License

MIT License (tulemas)

---

## 📧 Kontakt

Küsimused ja ettepanekud: [tuleb lisada]

---

**Versioon:** 0.1.0-alpha
**Viimati uuendatud:** 2025-10-12
