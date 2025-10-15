# Manuaalse Ülevaatuse Juhend - Terminibaas

Juhend `data/aca-glossary-eki.json` faili käsitsi ülevaatamiseks ja uuendamiseks.

## Ülevaade

Vaatad üle 826 Glossary terminit, mis on võrreldud 564 EKI terminiga.
- 10 terminit juba automaatselt matchitud
- 816 terminit vajavad manuaalset ülevaatust
- Eesmärk: leia lisamatche, märgi homonüümid, valideeri olemasolevad matchid

## Failid

**Peamine fail, mida muudad:**
- `data/aca-glossary-eki.json` - terminibaas (JSON formaat)

**Abimaterjalid (ainult vaatamiseks):**
- `data/glossary-review.csv` - 826 Glossary terminit, tähestikulises järjekorras
- `data/eki-terms.csv` - 564 EKI EN→ET paari, tähestikulises järjekorras

## Töövoog

**1. Ava failid**
```bash
code data/aca-glossary-eki.json
# Ava CSV failid Excelis/Google Sheetsis vaatamiseks
```

**2. Ülevaatuse protsess**
- Kontrolli esmalt 10 automaatselt matchitud terminit
- Otsi lisamatche, võrreldes EN termineid käsitsi
- Märgi homonüümid (terminid, millel mitu tähendust)
- Checkpoint iga 25 termini järel (salvesta!)

**3. Valideeri JSON pärast muudatusi**
```bash
python3 -m json.tool data/aca-glossary-eki.json > /dev/null
```
Kui ei anna errorit → JSON on korrektne ✅

## JSON Struktuur

### Homonüümi lisamine (uus sense)

Kui leiad, et terminil on mitu tähendust (nt "abuse" - nimisõna ja tegusõna):

```json
"abuse": {
  "english": "Abuse (n.)",
  "letter": "A",
  "glossary_row": 15,
  "senses": [
    {
      "sense_id": 1,
      "match_status": "matched",
      "match_confidence": "exact",
      "part_of_speech": "noun",
      "domain": "psychology/therapy",
      "eki_variants": [...],
      "synonyms": [],
      "preferred_variant": null,
      "notes": "kuritarvitamine"
    },
    {
      "sense_id": 2,
      "match_status": "unmatched",
      "match_confidence": "none",
      "part_of_speech": "verb",
      "domain": "",
      "eki_variants": [],
      "synonyms": [],
      "preferred_variant": null,
      "notes": "kuritarvitama"
    }
  ]
}
```

### Käsitsi matchi lisamine

Kui leiad CSV-st käsitsi matchi:

```json
{
  "sense_id": 1,
  "match_status": "matched",
  "match_confidence": "manual",
  "part_of_speech": "noun",
  "domain": "psychology/therapy",
  "eki_variants": [
    {
      "estonian": "kaastunne",
      "source": "eki_skt",
      "link": "https://sonaveeb.ee/search/unif/dlall/skt/kaastunne",
      "definition": "kopeeri EKI CSV-st definitsioon siia"
    }
  ],
  "synonyms": [],
  "preferred_variant": null,
  "notes": ""
}
```

## Väljade Väärtused

### `match_status`
- `"matched"` - EKI-st leitud vaste (eki_variants täidetud)
- `"unmatched"` - vastet pole veel (eki_variants tühi)
- `"definition_only"` - ainult definitsioon, ET termin puudub

### `match_confidence`
- `"exact"` - automaatne täpne match
- `"fuzzy"` - automaatne ligikaudne match
- `"manual"` - sina leidsid käsitsi CSV-st
- `"none"` - ei ole matchitud

### `part_of_speech`
- `"noun"` - nimisõna
- `"verb"` - tegusõna
- `"adjective"` - omadussõna
- `"adverb"` - määrsõna
- `null` - teadmata/mitteoluline

### `preferred_variant`
- `null` - pole veel valitud
- `0` - esimene variant eki_variants array'st
- `1` - teine variant, jne

## Checkpoint
Salvesta fail iga 25 termini järel ja valideeri JSON!
