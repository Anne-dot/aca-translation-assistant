# TBX-Basic Standard vs Sinu Plaanitud Struktuur

**Eesmärk:** Võrrelda TBX-Basic standardit sellega, mida olen planeerinud

**Allikad:**
- TBX-Basic v1.2.1 (ISO 30042:2019)
- FUTURE_IDEAS.md "Variant Structure" sektsioon
- Issue #7 kommentaarid (termComplexity, componentLookups)
- Issue #10 (glossary_manager, status tracking)

**Kuupäev:** 2025-10-16

---

## 📋 TL;DR (ADHD Summary)

### ✅ Hea uudis:
**Sinu plaanid ja TBX-Basic sobivad hästi kokku!** Väikeste kohandustega saad mõlemad eelised.

### 🎯 Peamine soovitus:
Kasuta **TBX-Basic struktuuri + ATL custom fields** (hübriid lähenemisviis)

### ⚡ 3 peamist otsust:

| # | Küsimus | Otsus |
|---|---------|-------|
| 1️⃣ | **Transaction history:** Täielik või lihtne? | ✅ Täielik - kogu ajalugu `transactions[]` array |
| 2️⃣ | **atl_in_use vs atl_approved:** Üks või mõlemad? | ✅ Variant C - Mõlemad eraldi (`atl_status` + `usage_status`) |
| 3️⃣ | **Component lookups:** Concept või term level? | ✅ Hübriid - andmed `_metadata`, viide `has_components: true` |

### 📊 Sobivuse skoor:

```
✅ Sobib hästi:       ████████░░  80%
✅ Kohandused:        ██████████  20% (kõik otsustatud 2025-10-16)
❌ Ei sobi:           ░░░░░░░░░░   0%
```

**Kõik 3 otsust tehtud:** Transaction history (täielik), Status tracking (Variant C), Component lookups (hübriid)

---

## 🚀 Kiire tegevusplaan:

1. ✅ **Loe üle:** See dokument (15 min) - DONE
2. ✅ **Otsusta:** 3 küsimust - DONE (2025-10-16)
3. ⏸️ **Kinnita:** Lõppstruktuur (vt näide read 384-547)
4. ⏸️ **Migratsioon:** Loo `migrate_to_tbx_structure.py`

---

## ❓ 3 otsust, mis vaja teha:

### Otsus 1: Transaction History ✅ OTSUSTATUD

**Küsimus:** Kas tahad kogu ajalugu või ainult viimane update?

| Variant | Kirjeldus | Keerukus |
|---------|-----------|----------|
| **A) Lihtne** | Ainult viimane update (`updated_by`, `updated_date`) | 🟢 Lihtne |
| **B) Täielik** | Kogu ajalugu array-na (`transactions[]`) | 🟡 Keskmine |

**✅ OTSUS: B) Täielik** - Kaasteeline tahab kogu transaction history

**Plussid:**
- ✅ Kogu ajalugu nähtav (kes, millal, miks)
- ✅ Saab jälgida otsuste evolutsiooni
- ✅ TBX-Basic compliant (`transacGrp`)
- ✅ Hea dokumentatsioon ja accountability

**Miinused:**
- ⚠️ Keerulisem andmestruktuur
- ⚠️ Rohkem andmeid (suurem JSON)
- ⚠️ Vajab korralikku transaction management logikat

---

### Otsus 2: atl_in_use vs atl_approved - VAJAB OTSUST

**Küsimus:** Kas kasutada ühte või mõlemat staatust? Mis on erinevus?

**Variant A: Ainult `atl_approved` (üks staatus)**

Tähendus: "ATL on selle termini ametlikult heaks kiitnud"

| Plussid | Miinused |
|---------|----------|
| ✅ Lihtne - üks selge staatus | ⚠️ Ei eristä "kasutuses" vs "heaks kiidetud" |
| ✅ Vähem valikuid = vähem segadust | ⚠️ Ei näita päevatekstide tegelikku kasutust |
| ✅ Sobib kui workflow on: review → approve | ⚠️ Ajaloolised terminid (enne review't) kaovad |

**Kasutusjuht:**
- ATL review team vaatab läbi ja kinnitab: `atl_approved`
- Kõik muu on `candidate` või `rejected`

---

**Variant B: Ainult `atl_in_use` (üks staatus)**

Tähendus: "Seda terminit kasutatakse hetkel ATL päevatekstides"

| Plussid | Miinused |
|---------|----------|
| ✅ Näitab tegelikku kasutust | ⚠️ Ei näita kas termin on "ametlikult heaks kiidetud" |
| ✅ Lihtne tuvastada (otsi päevatekstidest) | ⚠️ Võib muutuda aja jooksul (kui kasutus lõpeb) |
| ✅ Praktiline lähenemine | ⚠️ Ei jäädvusta review otsuseid |

**Kasutusjuht:**
- Analüüsi päevatekste → märgi terminid mis leitakse: `atl_in_use`
- Review'ta uued kandidaadid ja lisa need ka päevatekstidesse

---

**Variant C: Mõlemad eraldi (kaks staatust) ⭐ PAINDLIK**

Tähendus:
- `atl_in_use` = Praegu kasutusel päevatekstides (faktiline)
- `atl_approved` = Review team on heaks kiitnud (ametlik otsus)

| Plussid | Miinused |
|---------|----------|
| ✅ Maksimum info - mõlemad aspektid nähtavad | ⚠️ Keerulisem - kaks staatust paralleelselt |
| ✅ Näitab erinevust: "de facto" vs "de jure" | ⚠️ Võivad olla vastuolus (in_use aga mitte approved) |
| ✅ Ajalugu säilib (vanad terminid `in_use` ilma `approved`) | ⚠️ Vajab selget loogikat kuidas neid kombineerida |
| ✅ Paindlik - saab mõlemat trackida | ⚠️ Rohkem tööd (mõlemaid tuleb uuendada) |

**Kasutusjuhud:**

**Näide 1: Uus termin**
```json
{
  "term": "täiskasvanud laps",
  "workflow": {
    "atl_status": "atl_approved",      // Review team kiitis heaks
    "usage_status": "atl_in_use",      // Ja kasutame päevatekstides
    "approvedDate": "2025-10-16",
    "firstUsedDate": "2025-10-16"
  }
}
```

**Näide 2: Ajalooline termin (enne review'd)**
```json
{
  "term": "sõltlane",
  "workflow": {
    "atl_status": "candidate",         // Pole veel review'tud
    "usage_status": "atl_in_use",      // Aga kasutame juba
    "firstUsedDate": "2024-01-15"
  }
}
```

**Näide 3: Heakskiidetud aga mitte veel kasutusel**
```json
{
  "term": "täiskasvanu laps",
  "workflow": {
    "atl_status": "atl_approved",      // Review team kiitis heaks
    "usage_status": "candidate",       // Aga pole veel päevatekstides
    "approvedDate": "2025-10-16"
  }
}
```

**Näide 4: Kasutusel aga tagasi lükatud (deprecated)**
```json
{
  "term": "addikt",
  "workflow": {
    "atl_status": "rejected",          // Review lükkas tagasi
    "usage_status": "atl_in_use",      // Aga vanad tekstid kasutavad veel
    "rejectedDate": "2025-10-16",
    "rejectedReason": "Too clinical"
  }
}
```

---

**✅ OTSUSTATUD: Variant C** (2025-10-16)

**Põhjendus:** ATL tekstides on ajalooliselt kasutatud termineid, mis pole veel review'tud. Vajame eristust "kasutuses" vs "heaks kiidetud".

**Kasutatavad väljad:**
- `atl_status`: review otsus (`candidate`, `atl_approved`, `rejected`)
- `usage_status`: faktiline kasutus (`not_in_use`, `atl_in_use`, `formerly_in_use`)

---

### Otsus 3: componentLookups Asukoht ✅ OTSUSTATUD

**Küsimus:** Kas `componentLookups` peaks olema concept või term level?

**✅ OTSUS: Mõlemad!** - Concept level (EN komponendid) + Term level (ET tõlked)

**Põhjendus:**

Komponendid tulevad EN terminist:
```
"addictive behavior" → komponendid: ["addictive", "behavior"]
```

Iga komponendi tõlked on keelespetsiifilised:
```
EN: "addictive" → ET: "sõltuvuslik", "addiktiivne", "sõltlane"
EN: "behavior" → ET: "käitumine", "käitumisviis"
```

**Struktuur:**

```json
{
  "id": "c001",
  "subjectField": "ACA terminology",
  "languages": {
    "en": {
      "terms": [
        {
          "term": "addictive behavior",
          "partOfSpeech": "noun",
          "componentLookups": {
            "addictive": {
              "term": "addictive",
              "partOfSpeech": "adjective",
              "definitions": [...],
              "link": "https://sonaveeb.ee/..."
            },
            "behavior": {
              "term": "behavior",
              "partOfSpeech": "noun",
              "definitions": [...],
              "link": "https://sonaveeb.ee/..."
            }
          }
        }
      ]
    },
    "et": {
      "terms": [
        {
          "term": "addiktiivne käitumine",
          "partOfSpeech": "noun",
          "componentLookups": {
            "addictive": {
              "componentEn": "addictive",
              "translations": [
                {
                  "term": "sõltuvuslik",
                  "source": "Sõnaveeb",
                  "partOfSpeech": "adjective"
                },
                {
                  "term": "addiktiivne",
                  "source": "Sõnaveeb",
                  "partOfSpeech": "adjective"
                }
              ]
            },
            "behavior": {
              "componentEn": "behavior",
              "translations": [
                {
                  "term": "käitumine",
                  "source": "Sõnaveeb",
                  "partOfSpeech": "noun"
                }
              ]
            }
          }
        }
      ]
    }
  },
  "_metadata": {
    "termComplexity": "complex",
    "componentTerms": ["addictive", "behavior"],
    "isGlossaryTerm": true
  }
}
```

**Plussid:**
- ✅ EN komponendid EN terms juures (loogiline)
- ✅ ET tõlked ET terms juures (loogiline)
- ✅ Iga termin näeb oma komponentide tõlkeid
- ✅ Keelespetsiifiline info õiges kohas
- ✅ Aitab tõlkimisel (näed komponentide võimalikke tõlkeid)

**Miinused:**
- ⚠️ Duplikatsioon kui mitu ET terminit (kõigil samad komponendid)
- ⚠️ Keerulisem struktuur

**Alternatiiv - Concept level AINULT:**

```json
{
  "id": "c001",
  "_metadata": {
    "termComplexity": "complex",
    "componentTerms": ["addictive", "behavior"],
    "componentLookups": {
      "en": {
        "addictive": {...},
        "behavior": {...}
      },
      "et": {
        "addictive": [{term: "sõltuvuslik"}, {term: "addiktiivne"}],
        "behavior": [{term: "käitumine"}]
      }
    }
  }
}
```

**Mis on parem?**

| Aspekt | Term level | Concept level |
|--------|------------|---------------|
| **Loogilisus** | ✅ Info termini juures | ⚠️ Info metadata sees |
| **Duplikatsioon** | ⚠️ Kui mitu ET terminit | ✅ Üks kord concept'is |
| **Kasutamine** | ✅ Lihtne: vaata terminit | ⚠️ Pead otsima metadata'st |
| **JSON size** | ⚠️ Suurem (duplikatsioon) | ✅ Väiksem (üks kord) |

**Hübriid soovitus:**

**Concept level:** Kõik EN komponendid + kõik ET tõlked
**Term level:** Viide komponentidele (ei dubleerida)

```json
{
  "id": "c001",
  "languages": {
    "en": {
      "terms": [{
        "term": "addictive behavior",
        "hasComponents": true  // Viide
      }]
    },
    "et": {
      "terms": [{
        "term": "addiktiivne käitumine",
        "hasComponents": true  // Viide
      }]
    }
  },
  "_metadata": {
    "componentTerms": ["addictive", "behavior"],
    "componentLookups": {
      "en": {
        "addictive": {
          "term": "addictive",
          "partOfSpeech": "adjective",
          "link": "..."
        },
        "behavior": {
          "term": "behavior",
          "partOfSpeech": "noun",
          "link": "..."
        }
      },
      "et": {
        "addictive": [
          {"term": "sõltuvuslik", "source": "Sõnaveeb"},
          {"term": "addiktiivne", "source": "Sõnaveeb"}
        ],
        "behavior": [
          {"term": "käitumine", "source": "Sõnaveeb"}
        ]
      }
    }
  }
}
```

**Selle variandi plussid:**
- ✅ Ei duplitseeri andmeid
- ✅ Kõik component info ühes kohas
- ✅ Term level näitab et komponendid eksisteerivad
- ✅ Väiksem JSON size

**SOOVITUS:** Hübriid - andmed `_metadata.componentLookups`, viide `has_components: true` termini juures

---

## 📦 Lõppstruktuur Vastavalt Otsustele:

```json
{
  "id": "c001",
  "subjectField": "ACA terminology",
  "languages": {
    "en": {
      "xml:lang": "en",
      "terms": [
        {
          "term": "addictive behavior",
          "partOfSpeech": "noun",
          "administrativeStatus": "preferredTerm-admn-sts",
          "source": "WSO ACA Glossary",
          "hasComponents": true,
          "transactions": [
            {
              "type": "origination",
              "responsibility": "Anne",
              "date": "2025-10-15",
              "action": "Added from WSO Glossary"
            }
          ]
        }
      ]
    },
    "et": {
      "xml:lang": "et",
      "definition": "Sõltuvust iseloomustav käitumismuster",
      "terms": [
        {
          "term": "addiktiivne käitumine",
          "partOfSpeech": "noun",
          "administrativeStatus": "preferredTerm-admn-sts",
          "source": "WSO ACA Glossary",
          "hasComponents": true,
          "workflow": {
            "atl_status": "atl_approved",
            "usage_status": "atl_in_use",
            "approvedBy": "ATL consensus",
            "approvedDate": "2025-10-16",
            "firstUsedDate": "2025-10-16"
          },
          "usageExamples": [
            {
              "source": "Daily Meditation 2024-03-15",
              "enContext": "We recognize our addictive behavior patterns.",
              "etTranslation": "Me tunnistame oma addiktiivseid käitumismustreid.",
              "translatorNote": {
                "author": "Külli J",
                "date": "2025-10-16",
                "explanation": "Kasutasin 'addiktiivne' mitte 'sõltuvuslik', sest see on otsesem ja vähem kliiniline.",
                "keyInsight": "ATL kontekstis on oluline säilitada isiklik toon."
              }
            }
          ],
          "transactions": [
            {
              "type": "origination",
              "responsibility": "Anne",
              "date": "2025-10-15",
              "action": "Added from WSO Glossary"
            },
            {
              "type": "modification",
              "responsibility": "ATL consensus",
              "date": "2025-10-16",
              "action": "Approved as preferred term",
              "statusChange": "candidate → atl_approved"
            }
          ]
        },
        {
          "term": "sõltuvuslik käitumine",
          "partOfSpeech": "noun",
          "administrativeStatus": "deprecatedTerm-admn-sts",
          "source": "Sõnaveeb SKT",
          "hasComponents": true,
          "workflow": {
            "atl_status": "rejected",
            "usage_status": "not_in_use",
            "rejectedBy": "ATL review team",
            "rejectedDate": "2025-10-16"
          },
          "note": "Too clinical, not ACA tone",
          "transactions": [
            {
              "type": "origination",
              "responsibility": "System",
              "date": "2025-10-15",
              "action": "Found in Sõnaveeb lookup"
            },
            {
              "type": "modification",
              "responsibility": "ATL review team",
              "date": "2025-10-16",
              "action": "Rejected - too clinical tone",
              "statusChange": "candidate → rejected"
            }
          ]
        },
        {
          "term": "sõltlane käitumine",
          "partOfSpeech": "noun",
          "administrativeStatus": "admittedTerm-admn-sts",
          "source": "Sõnaveeb",
          "hasComponents": true,
          "workflow": {
            "atl_status": "candidate",
            "usage_status": "not_in_use",
            "addedDate": "2025-10-15"
          },
          "transactions": [
            {
              "type": "origination",
              "responsibility": "System",
              "date": "2025-10-15",
              "action": "Found in Sõnaveeb lookup"
            }
          ]
        }
      ]
    }
  },
  "_metadata": {
    "termComplexity": "complex",
    "componentTerms": ["addictive", "behavior"],
    "isGlossaryTerm": true,
    "componentLookups": {
      "en": {
        "addictive": {
          "term": "addictive",
          "partOfSpeech": "adjective",
          "definitions": ["causing or tending to cause addiction"],
          "link": "https://sonaveeb.ee/search/unif/dlall/dsall/addictive"
        },
        "behavior": {
          "term": "behavior",
          "partOfSpeech": "noun",
          "definitions": ["the way in which one acts or conducts oneself"],
          "link": "https://sonaveeb.ee/search/unif/dlall/dsall/behavior"
        }
      },
      "et": {
        "addictive": [
          {
            "term": "sõltuvuslik",
            "partOfSpeech": "adjective",
            "source": "Sõnaveeb",
            "link": "https://sonaveeb.ee/..."
          },
          {
            "term": "addiktiivne",
            "partOfSpeech": "adjective",
            "source": "Sõnaveeb",
            "link": "https://sonaveeb.ee/..."
          }
        ],
        "behavior": [
          {
            "term": "käitumine",
            "partOfSpeech": "noun",
            "source": "Sõnaveeb",
            "link": "https://sonaveeb.ee/..."
          },
          {
            "term": "käitumisviis",
            "partOfSpeech": "noun",
            "source": "Sõnaveeb",
            "link": "https://sonaveeb.ee/..."
          }
        ]
      }
    }
  }
}
```

**Eelised:**
- ✅ TBX-Basic compliant (eksporditav)
- ✅ Kogu transaction history säilib (otsus 1)
- ✅ ATL workflow: `atl_status` + `usage_status` (otsus 2, variant C)
- ✅ Component lookups `_metadata` sees, viide `has_components` (otsus 3)
- ✅ Selge ja hästi struktureeritud

---

## 📖 Detailne võrdlus

---

## Eelnevalt plaanitud struktuur (FUTURE_IDEAS.md)

### Variant Structure

```json
{
  "variants": [
    {
      "estonian": "sõltuvuslik käitumine",
      "status": "rejected",
      "rejectedBy": "ATL review team",
      "rejectedDate": "2025-10-16",
      "rejectedReason": "Too clinical, not ACA tone"
    },
    {
      "estonian": "addiktiivne käitumine",
      "status": "atl_approved",
      "approvedBy": "ATL consensus",
      "approvedDate": "2025-10-16"
    }
  ]
}
```

### Põhikontseptsioonid:

1. **Mitmed variandid** - iga termin võib omada mitmeid tõlkevariante
2. **Individuaalne staatus** - iga variant oma staatusega
3. **ATL workflow staatused:**
   - `atl_approved` - ATL on heaks kiitnud
   - `atl_in_use` - Praegu kasutusel ATL päevatekstides
   - `candidate` - Ootab läbivaatamist
   - `rejected` - Selgelt tagasi lükatud

4. **Metadata staatuse kohta:**
   - Heakskiidetud: `approved_by`, `approved_date`
   - Tagasilükatud: `rejected_by`, `rejected_date`, `rejected_reason`

5. **is_glossary_term** - eristab ametlikke ACA termineid komponent-terminitest
6. **derivedFrom** - array, mis jälgib allika glossaari termineid

### Component Terms (Issue #7, FUTURE_IDEAS.md)

```json
{
  "addictive": {
    "isGlossaryTerm": false,
    "derivedFrom": ["addictive behavior", "addictive thinking"],
    "componentLookups": {
      "sonaveeb": [...]
    }
  },
  "addictive behavior": {
    "isGlossaryTerm": true,
    "termComplexity": "complex",
    "componentTerms": ["addictive", "behavior"],
    "variants": [...]
  }
}
```

---

## TBX-Basic Standard

### Variant Structure

```xml
<langSec xml:lang="et">
  <termSec>
    <term>sõltuvuslik käitumine</term>
    <termNote type="partOfSpeech">noun</termNote>
    <termNote type="administrativeStatus">deprecatedTerm-admn-sts</termNote>
    <note>Too clinical, not ACA tone</note>
  </termSec>
  <termSec>
    <term>addiktiivne käitumine</term>
    <termNote type="partOfSpeech">noun</termNote>
    <termNote type="administrativeStatus">preferredTerm-admn-sts</termNote>
  </termSec>
</langSec>
```

### Põhikontseptsioonid:

1. **Mitmed termSec elemendid** - iga variant eraldi termSec sees
2. **Standardne administrativeStatus:**
   - `preferredTerm-admn-sts` - Eelistatud termin (kasuta seda!)
   - `admittedTerm-admn-sts` - Lubatud alternatiiv
   - `deprecatedTerm-admn-sts` - Aegunud (ära kasuta)
   - `supersededTerm-admn-sts` - Asendatud teise terminiga

3. **Transaction tracking:**
   - `transactionType`: "origination", "modification"
   - `responsibility`: isik/organisatsioon
   - `date`: kuupäev

4. **Notes** - vabatekst märkused (nt tagasilükkamise põhjus)

---

## Võrdlus: Väljad ja Kontseptsioonid

| Funktsioon | Sinu Plaan | TBX-Basic | Sobivus |
|------------|-----------|-----------|---------|
| **Mitmed variandid** | `variants` array | Mitmed `termSec` elemendid | ✅ Sama idee |
| **Variant staatus** | `status` field | `administrativeStatus` | ⚠️ Erinevad väärtused |
| **Heakskiitmine** | `approved_by`, `approved_date` | `transacGrp` (origination/modification) | ⚠️ Erinevad nimed |
| **Tagasilükkamine** | `rejected_by`, `rejected_date`, `rejected_reason` | `note` + `deprecatedTerm-admn-sts` | ⚠️ Erinevad nimed |
| **Märkused** | `rejected_reason` | `note` | ✅ Sama |
| **is_glossary_term** | `is_glossary_term: true/false` | - | ❌ Puudub standardis |
| **derivedFrom** | `derivedFrom` array | - | ❌ Puudub standardis |
| **termComplexity** | `termComplexity` (ISO 1087) | - | ➕ Hea lisa! |
| **componentTerms** | `componentTerms` array | - | ➕ Hea lisa! |
| **componentLookups** | `componentLookups` object | - | ➕ Hea lisa! |

---

## Staatuse Väärtused - Detailne Võrdlus

### TBX-Basic Standard Väärtused

| Väärtus | Tähendus | Kasutus |
|---------|----------|---------|
| `preferredTerm-admn-sts` | Eelistatud termin | Kasuta SEDA terminit |
| `admittedTerm-admn-sts` | Lubatud termin | Aktsepteeritav alternatiiv |
| `deprecatedTerm-admn-sts` | Aegunud termin | Ära kasuta, aga eksisteerib |
| `supersededTerm-admn-sts` | Asendatud termin | Asendatud uue terminiga |

### Sinu Plaanitud ATL Väärtused

| Väärtus | Tähendus | Kasutus |
|---------|----------|---------|
| `atl_approved` | ATL heakskiidetud | ATL on läbi vaadanud ja heaks kiitnud |
| `atl_in_use` | ATL kasutuses | Praegu aktiivselt kasutusel ATL päevatekstides |
| `candidate` | Kandidaat | Ootab ATL läbivaatamist |
| `rejected` | Tagasilükatud | ATL lükkas selgelt tagasi |

### Kuidas Need Sobivad Kokku?

| ATL Staatus | TBX-Basic Ekvivalent | Sobivus |
|-------------|---------------------|---------|
| `atl_approved` | `preferredTerm-admn-sts` | ✅ Väga hea sobivus |
| `atl_in_use` | `admittedTerm-admn-sts` | ⚠️ Osaliselt - TBX ei eristä "praegu kasutusel" |
| `candidate` | - | ❌ Puudub TBX-is (review workflow) |
| `rejected` | `deprecatedTerm-admn-sts` | ⚠️ Osaliselt - TBX "deprecated" on pigem "aegunud" kui "tagasilükatud" |

---

## Kuidas Neid Kombineerida?

### Variant 1: Topelt-Staatus (ATL + TBX)

```json
{
  "term": "addiktiivne käitumine",
  "partOfSpeech": "noun",
  "administrativeStatus": "preferredTerm-admn-sts",
  "atl_status": "atl_approved",
  "approvedBy": "ATL consensus",
  "approvedDate": "2025-10-16",
  "source": "WSO ACA Glossary"
}
```

**Plussid:**
- ✅ TBX-Basic compliant
- ✅ ATL workflow tracking
- ✅ Eksporditav TBX formaati

**Miinused:**
- ⚠️ Kaks staatuse välja (võib olla segane)

### Variant 2: Laiendatud administrativeStatus

```json
{
  "term": "addiktiivne käitumine",
  "partOfSpeech": "noun",
  "administrativeStatus": "atl_approved",
  "approvedBy": "ATL consensus",
  "approvedDate": "2025-10-16",
  "source": "WSO ACA Glossary",
  "_tbx_mapping": {
    "atl_approved": "preferredTerm-admn-sts",
    "atl_in_use": "admittedTerm-admn-sts",
    "candidate": null,
    "rejected": "deprecatedTerm-admn-sts"
  }
}
```

**Plussid:**
- ✅ ATL-sõbralik (oma staatused)
- ✅ TBX mapping dokumenteeritud
- ✅ Lihtne eksportida (kasuta mappingut)

**Miinused:**
- ⚠️ Mitte täielikult TBX compliant (custom values)

### Variant 3: Hübriid

```json
{
  "term": "addiktiivne käitumine",
  "partOfSpeech": "noun",
  "administrativeStatus": "preferredTerm-admn-sts",
  "workflow": {
    "atl_status": "atl_approved",
    "approvedBy": "ATL consensus",
    "approvedDate": "2025-10-16",
    "reviewStatus": "completed"
  },
  "source": "WSO ACA Glossary"
}
```

**Plussid:**
- ✅ TBX compliant (administrativeStatus standard)
- ✅ ATL workflow eraldi gruppeerituna
- ✅ Selge eraldus: termin staatus vs. workflow staatus

**Miinused:**
- ⚠️ Veidi keerulisem struktuur

---

## Transaction Tracking - Võrdlus

### TBX-Basic: transacGrp

```xml
<transacGrp>
  <transac type="transactionType">origination</transac>
  <transacNote type="responsibility" target="pe324">Tommy</transacNote>
  <date>2025-10-16</date>
</transacGrp>
<transacGrp>
  <transac type="transactionType">modification</transac>
  <transacNote type="responsibility" target="pe456">Anne</transacNote>
  <date>2025-10-17</date>
</transacGrp>
```

**Kontseptsioon:**
- Mitmed `transacGrp` elemendid (ajalugu)
- Igal tehingul tüüp, isik, kuupäev

### Sinu Plaan: Metadata Per Status

```json
{
  "status": "atl_approved",
  "approvedBy": "ATL consensus",
  "approvedDate": "2025-10-16"
}
```

**Kontseptsioon:**
- Metadata otseselt staatuse juures
- Ainult viimane tehing (mitte kogu ajalugu)

### Kombineeritud Variant

```json
{
  "term": "addiktiivne käitumine",
  "administrativeStatus": "preferredTerm-admn-sts",
  "transactions": [
    {
      "type": "origination",
      "responsibility": "Anne",
      "date": "2025-10-15",
      "action": "Added from WSO Glossary"
    },
    {
      "type": "modification",
      "responsibility": "ATL consensus",
      "date": "2025-10-16",
      "action": "Approved as preferred term",
      "atl_status_change": "candidate → atl_approved"
    },
    {
      "type": "modification",
      "responsibility": "Mirko",
      "date": "2025-10-17",
      "action": "Added part of speech"
    }
  ]
}
```

**Plussid:**
- ✅ TBX compliant (transaction tracking)
- ✅ Kogu ajalugu säilitatud
- ✅ ATL workflow decisions dokumenteeritud

**Miinused:**
- ⚠️ Keerulisem struktuur
- ⚠️ Kas kogu ajalugu on vajalik?

---

## Component Terms - TBX-is Puudub!

### Sinu Plaanid:

```json
{
  "addictive": {
    "isGlossaryTerm": false,
    "derivedFrom": ["addictive behavior", "addictive thinking"],
    "termComplexity": "simple"
  },
  "addictive behavior": {
    "isGlossaryTerm": true,
    "termComplexity": "complex",
    "componentTerms": ["addictive", "behavior"]
  }
}
```

### TBX-Basic:

**Puudub otse!** Aga on lahendused:

#### Lahendus 1: crossReference

```xml
<conceptEntry id="c001">
  <term>addictive behavior</term>
  <ref type="crossReference" target="c042">addictive</ref>
  <ref type="crossReference" target="c123">behavior</ref>
</conceptEntry>

<conceptEntry id="c042">
  <term>addictive</term>
  <note>Component term derived from: addictive behavior, addictive thinking</note>
</conceptEntry>
```

**Kasutab:** TBX `crossReference` funktsiooni

#### Lahendus 2: Custom Data Category

```xml
<conceptEntry id="c042">
  <term>addictive</term>
  <admin type="termType">componentTerm</admin>
  <admin type="derivedFrom">addictive behavior; addictive thinking</admin>
</conceptEntry>
```

**Kasutab:** TBX custom `admin` väljad

#### Lahendus 3: JSON Custom Fields (Eksportida hiljem)

```json
{
  "id": "c042",
  "languages": {
    "en": {
      "terms": [
        {
          "term": "addictive",
          "partOfSpeech": "adjective"
        }
      ]
    }
  },
  "_custom": {
    "isGlossaryTerm": false,
    "derivedFrom": ["addictive behavior", "addictive thinking"]
  }
}
```

**Kasutab:** Custom JSON fields, eksport TBX-i käigus convertitakse

---

## Soovitused

### 1. Staatused: Variant 3 (Hübriid)

```json
{
  "term": "addiktiivne käitumine",
  "partOfSpeech": "noun",
  "administrativeStatus": "preferredTerm-admn-sts",
  "workflow": {
    "atl_status": "atl_approved",
    "approvedBy": "ATL consensus",
    "approvedDate": "2025-10-16"
  },
  "source": "WSO ACA Glossary"
}
```

**Põhjused:**
- ✅ TBX compliant
- ✅ ATL workflow selgelt eraldatud
- ✅ Lihtne eksportida TBX-i
- ✅ ATL-sõbralikud staatused säilivad

**Mapping TBX eksporti jaoks:**
- `atl_approved` → `preferredTerm-admn-sts`
- `atl_in_use` → `admittedTerm-admn-sts`
- `candidate` → jätta välja TBX ekspordist (internal workflow)
- `rejected` → `deprecatedTerm-admn-sts` + note with reason

### 2. Component Terms: Lahendus 3 (JSON Custom)

```json
{
  "id": "c042",
  "subjectField": "ACA terminology",
  "languages": {
    "en": {
      "terms": [{"term": "addictive", "partOfSpeech": "adjective"}]
    },
    "et": {
      "terms": [{"term": "sõltuvuslik", "administrativeStatus": "candidate"}]
    }
  },
  "_metadata": {
    "isGlossaryTerm": false,
    "derivedFrom": ["addictive behavior", "addictive thinking"],
    "termComplexity": "simple"
  }
}
```

**Põhjused:**
- ✅ Component terms on tavalised terminid
- ✅ Custom metadata `_metadata` grupis
- ✅ TBX eksport: kasuta `crossReference` või `admin` välju
- ✅ Lihtne struktuur

### 3. Transaction History: Täielik Variant ✅ OTSUSTATUD

**Kogu täielik ajalugu `transactions[]` array-na** (2025-10-16):

```json
{
  "term": "addiktiivne käitumine",
  "administrativeStatus": "preferredTerm-admn-sts",
  "transactions": [
    {
      "type": "origination",
      "responsibility": "Anne",
      "date": "2025-10-15",
      "action": "Added from WSO Glossary"
    },
    {
      "type": "modification",
      "responsibility": "ATL consensus",
      "date": "2025-10-16",
      "action": "Approved as preferred term",
      "status_change": "candidate → atl_approved"
    }
  ]
}
```

**Põhjused:**
- ✅ TBX-Basic compliant (`transacGrp`)
- ✅ Kogu ajalugu säilitatud (kes, millal, miks)
- ✅ Saab jälgida otsuste evolutsiooni
- ✅ Hea dokumentatsioon ja accountability

### 4. Tagasilükkamised: note Field

```json
{
  "term": "sõltuvuslik käitumine",
  "administrativeStatus": "deprecatedTerm-admn-sts",
  "workflow": {
    "atl_status": "rejected",
    "rejectedBy": "ATL review team",
    "rejectedDate": "2025-10-16"
  },
  "note": "Too clinical, not ACA tone"
}
```

**Põhjused:**
- ✅ TBX `note` standard field
- ✅ Põhjus selgelt dokumenteeritud
- ✅ ATL workflow metadata eraldi

---

## Lõppstruktuur: Soovitus

```json
{
  "metadata": {
    "created": "2025-10-16",
    "standard": "TBX-Basic v1.2.1 + ATL Extensions",
    "formatVersion": "2.0"
  },
  "concepts": [
    {
      "id": "c001",
      "subjectField": "ACA terminology",
      "languages": {
        "en": {
          "xml:lang": "en",
          "definition": null,
          "terms": [
            {
              "term": "addictive behavior",
              "partOfSpeech": "noun",
              "administrativeStatus": "preferredTerm-admn-sts",
              "source": "WSO ACA Glossary",
              "note": "Pattern of behavior characterized by addiction"
            }
          ]
        },
        "et": {
          "xml:lang": "et",
          "definition": "Sõltuvust iseloomustav käitumismuster",
          "terms": [
            {
              "term": "addiktiivne käitumine",
              "partOfSpeech": "noun",
              "administrativeStatus": "preferredTerm-admn-sts",
              "source": "WSO ACA Glossary",
              "workflow": {
                "atl_status": "atl_approved",
                "approvedBy": "ATL consensus",
                "approvedDate": "2025-10-16"
              }
            },
            {
              "term": "sõltuvuslik käitumine",
              "partOfSpeech": "noun",
              "administrativeStatus": "deprecatedTerm-admn-sts",
              "source": "Sõnaveeb",
              "workflow": {
                "atl_status": "rejected",
                "rejectedBy": "ATL review team",
                "rejectedDate": "2025-10-16"
              },
              "note": "Too clinical, not ACA tone"
            },
            {
              "term": "sõltlane käitumine",
              "partOfSpeech": "noun",
              "administrativeStatus": "admittedTerm-admn-sts",
              "source": "Sõnaveeb",
              "workflow": {
                "atl_status": "candidate",
                "addedDate": "2025-10-15"
              }
            }
          ]
        }
      },
      "_metadata": {
        "termComplexity": "complex",
        "componentTerms": ["addictive", "behavior"],
        "isGlossaryTerm": true
      }
    },
    {
      "id": "c042",
      "subjectField": "ACA terminology",
      "languages": {
        "en": {
          "xml:lang": "en",
          "terms": [
            {
              "term": "addictive",
              "partOfSpeech": "adjective",
              "administrativeStatus": "preferredTerm-admn-sts"
            }
          ]
        },
        "et": {
          "xml:lang": "et",
          "terms": [
            {
              "term": "sõltuvuslik",
              "partOfSpeech": "adjective",
              "administrativeStatus": "candidate",
              "source": "Sõnaveeb",
              "workflow": {
                "atl_status": "candidate",
                "addedDate": "2025-10-15"
              }
            }
          ]
        }
      },
      "_metadata": {
        "termComplexity": "simple",
        "componentTerms": null,
        "isGlossaryTerm": false,
        "derivedFrom": ["addictive behavior", "addictive thinking"]
      }
    }
  ]
}
```

---

## Kokkuvõte: Sinu Plaanid vs TBX-Basic

### ✅ Hea Sobivus

1. **Mitmed variandid** - TBX toetab täielikult (mitmed termSec elemendid)
2. **Staatuse tracking** - TBX `administrativeStatus` vastab ATL vajadustele
3. **Source tracking** - TBX `admin type="source"` ja `source` field
4. **Notes** - TBX `note` field sobib rejected_reason jaoks
5. **termComplexity** - Hea lisa! ISO 1087 compliant

### ⚠️ Vajab Kohandamist

1. **ATL staatused** - ✅ OTSUSTATUD: Kasuta custom väärtusi (`atl_status`, `usage_status`) + mapping TBX standardile
2. **Workflow metadata** - ✅ OTSUSTATUD: Grupeeri `workflow` objekti (separate from term data)
3. **Transaction history** - ✅ OTSUSTATUD: Täielik history `transactions[]` array (2025-10-16)

### ➕ Sinu Unikaalsed Lisad

1. **is_glossary_term** - Eristab kolme tüüpi termineid:
   - `true` - WSO ametlikud glossaari terminid
   - `false` + `derivedFrom: [...]` - Komponent-terminid (tuletatud glossaarist)
   - `false` + `derivedFrom: []` - Kogukonna lisatud terminid (korduvad tekstis, arutlusobjektid)

   Näide kogukonna terminist:
   ```json
   {
     "_metadata": {
       "isGlossaryTerm": false,
       "derivedFrom": [],
       "termType": "communityAdded",
       "addedReason": "Kordub palju ATL tekstides, tekitab arutelusid"
     }
   }
   ```

2. **derivedFrom** - Jälgib terminite päritolu ja seoseid glossaari terminitega
3. **componentTerms** - ISO 1087 compliant! Liitsõnade komponentide loetelu
4. **componentLookups** (Issue #7) - Komponentide eraldi Sõnaveeb lookupid
5. **usageExamples** - Tõlkeotsuste dokumenteerimine kontekstiga:
   ```json
   {
     "usageExamples": [
       {
         "source": "Daily Meditation 2024-03-15",
         "enContext": "...we feel that we are changing inside.",
         "etTranslation": "...me tunneme, et meis toimub sisemine muutus.",
         "translatorNote": {
           "author": "Külli J",
           "date": "2025-10-16",
           "explanation": "See pole intellektuaalne taipamine, vaid tajutav tunne...",
           "keyInsight": "Sisemine muutus ei sünni pingutades..."
         }
       }
     ]
   }
   ```

### 📖 Grammatilised Vormid ja CAT Toolid

**Eesti keele eripära:** 14 käänet × 2 arvu = 28 vormi + tüvemitus (nt `käsi : käe`)

**CAT tool lähenemine:**

Salvesta AINULT baasvormi (lemma). CAT tool lemmatiseerija leiab grammatilised variandid automaatselt.

**Kuidas see töötab:**

1. Terminipank: `"muutus"` (alus/nominatiiv)
2. Tekstis: `"muutusest"` (alaltüüv)
3. CAT lemmatiseerija: `"muutusest" → "muutus"`
4. Tulemus: CAT leiab termini ✅

**TBX-Basic struktuur:**
```json
{
  "term": "muutus",
  "partOfSpeech": "noun",
  "grammaticalNumber": "singular",
  "grammaticalGender": "common"
}
```

**Erandid - lisa käsitsi vormid kui:**
- CAT tool ei leia vormi ära (testimise järel)
- Tüvemitus on erandlik (`käsi : käe`, `vesi : vee`)
- Vorm on idioomatiline erinevate tähendustega

**Pragmaatiline variant:**
```json
{
  "term": "muutus",
  "partOfSpeech": "noun",
  "etVariants": []  // Tavaliselt tühi
}

// AGA kui CAT ei tunne "muutusest" ära:
{
  "term": "muutus",
  "partOfSpeech": "noun",
  "etVariants": [
    {
      "term": "muutusest",
      "grammaticalCase": "elative"
    }
  ]
}
```

**Soovitus:**
- Alusta ainult baasvormi-ga (95% terminitest)
- Testi CAT tool eesti tekstidega
- Lisa vorme ainult probleemsete termini puhul (5%)

**CAT tool fuzzy matching:**
- Baasterminid + olulised fraasid eraldi terminitena
- CAT tool leiab n-gram matchinguga kõik variandid
- Tõlkijad näevad konteksti + usageExamples

### 🎯 Peamine Soovitus

**Kasuta TBX-Basic struktuuri tuumikuna + lisa custom ATL fields `workflow` ja `_metadata` gruppidesse.**

**Eelised:**
- ✅ TBX compliant (eksporditav)
- ✅ ATL workflow supported
- ✅ Component terms tracked
- ✅ ADHD-friendly (selge struktuur)

---

**Kõik otsused tehtud:** (2025-10-16)

1. ✅ **Transaction history:** Täielik history `transactions[]` array
2. ✅ **atl_in_use vs atl_approved:** Variant C - mõlemad eraldi (`atl_status` + `usage_status`)
3. ✅ **componentLookups:** Hübriid - andmed `_metadata`, viide `has_components: true`

---

**Viimati uuendatud:** 2025-10-16 (kõik otsused finaliseeritud)
