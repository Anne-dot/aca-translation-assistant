# EKI Terminibaasid - Kogutud Andmed

**Kogumise kuupäev:** 2025-10-12

## 📊 Ülevaade

Selles kaustas on EKI (Eesti Keele Instituut) Sõnaveeb terminibaasidest kogutud terminid koos täieliku sisuga.

**Kokku kogutud:** **1,278 terminit**

## 📁 Failid

| Fail | Termineid | Terminibaas | Kontakt |
|------|-----------|-------------|---------|
| `eki_kriis_20251012.json` | 82 | Kriisinõustamine | Kirsti Talu (kirstit@gmail.com) |
| `eki_skt_20251012.json` | 250 | Skeemiteraapia | Kaia Kastepõld-Tõrs (skeemiteraapia@gmail.com) |
| `eki_dkt_20251012.json` | 301 | Dialektilise käitumisteraapia | dkteesti@gmail.com |
| `eki_TAI_20251012.json` | 645 | Tervisesõnastik | Ruth Erm (ruth.erm@tai.ee) |

## 📋 Andmestruktuur

Iga JSON fail sisaldab:

### Metaandmed
```json
{
  "metaandmed": {
    "terminibaas_kood": "skt",
    "terminibaas_nimi": "Skeemiteraapia terminisõnastik",
    "terminibaas_url": "https://sonaveeb.ee/ds/skt",
    "kontakt": "Kaia Kastepõld-Tõrs (skeemiteraapia@gmail.com)",
    "kogumise_kuupaev": "2025-10-12T...",
    "terminite_arv": 250
  }
}
```

### Terminid
Iga termin sisaldab:
```json
{
  "termin": "emotsionaalne deprivatsioon",
  "link": "https://sonaveeb.ee/search/unif/dlall/skt/...",
  "taht": "e",
  "keel": "eesti",
  "synonyymid": [],
  "definitsioon": "eeldus, et vajadus ja soov emotsionaalse toe järele..."
}
```

**Väljad:**
- **termin** - Termini nimi (eesti, inglise, vene või soome keeles)
- **link** - Otsene link EKI lehele
- **taht** - Täht, millelt termin leiti (navigeerimiseks)
- **keel** - Termini keel (eesti, inglise, vene, soome)
- **synonyymid** - Sünonüümide nimekiri (kui on)
- **definitsioon** - Täielik professionaalne definitsioon EKI-st

## 🔍 Näited Terminitest

### Kriisinõustamine (kriis)
- **akuutkriis** (eesti): "traumaatilist mõju omava kriisiolukorra kogemise esimesest hetkest 30-40 päeva pikkune periood"
- **kaastundeväsimus** (eesti): "emotsionaalse ja füüsilise kurnatuse seisund..."
- **crisis intervention** (inglise): "lühiajaline kriisi- ja traumateadlik psühhosostsiaalne sekkumine"

### Skeemiteraapia (skt)
- **abandonment** (inglise): "eeldus, et kõik elu jooksul loodud tähtsad suhted lõpevad"
- **emotsionaalne deprivatsioon** (eesti): "eeldus, et vajadus ja soov emotsionaalse toe järele ei saa kunagi piisavalt täidetud"
- **terve täiskasvanu olek** (eesti): "üks funktsionaalsetest olekutest..."
- **Inner Child / lapse olek** (eesti): "üks kategooria skeemi olekutest..."

### DKT (dkt)
- **emotsionaalne düsregulatsioon** (eesti): "võimetus reguleerida emotsioone"
- **mindfulness** (inglise): "teadlik kohalolek"
- **distress tolerance** (inglise): "stressi talumise oskused"

### Tervisesõnastik (TAI)
- **social exclusion** (inglise): "sotsiaalne tõrjutus"
- **subjective well-being** (inglise): "subjektiivne heaolu"
- **vulnerability** (inglise): "haavatavus"

## 🎯 Kasutamine

### Python-is JSON failide lugemine:
```python
import json

# Lae skeemiteraapia terminid
with open('eki_skt_20251012.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Vaata metaandmeid
print(f"Terminibaas: {data['metaandmed']['terminibaas_nimi']}")
print(f"Termineid: {data['metaandmed']['terminite_arv']}")

# Otsi terminit
for term in data['terminid']:
    if 'abandonment' in term['termin'].lower():
        print(f"{term['termin']}: {term['definitsioon']}")
```

## ⚙️ Kuidas Need Koguti

**Skript:** `/src/eki_koguja.py`

**Protsess:**
1. Kontrollib, millised tähed on terminibaasis saadaval
2. Külastab iga tähe lehte (nt `https://sonaveeb.ee/ds/skt/a`)
3. Ekstraktib terminite nimekirja
4. Iga termini kohta külastab detaillehte
5. Kogub kõik andmed: keel, sünonüümid, definitsioon
6. Salvestab JSON formaati

**Aeg:** ~0.7 sek/termin (koos pausidega serverile)

## 🔗 Allikad

Kõik andmed pärinevad EKI Sõnaveeb terminibaasidest:
- https://sonaveeb.ee/collections
- https://eki.ee

**Usaldusväärsus:** ⭐⭐⭐⭐⭐ VÄGA KÕRGE (ametlik keeleinstituut)

## 📝 Märkused

- Terminid sisaldavad eesti, inglise, vene ja soome keelseid vasteid
- Mõned terminid on mitmekeelsed (nt "Inner Child" ja "lapse olek")
- Definitsioonid on professionaalsed ja EKI poolt kinnitatud
- Andmed on kogutud 2025-10-12, uuendamiseks käivita skript uuesti

## 🎯 Kasutamine ATL Projektis

Need terminid on mõeldud kasutamiseks:
1. **Glossary võrdluseks** - võrdle ATL Glossary tõlkimata terminitega
2. **Tõlkeabi** - leia professionaalsed eestikeelsed vasted
3. **Kvaliteedi kontroll** - kontrolli olemasolevaid tõlkeid EKI vastu
4. **Konteksti mõistmine** - loe definitsioonid, et mõista termineid paremini

---

**Järgmine samm:** Võrdle neid termineid ATL Glossary 635 tõlkimata terminiga!
