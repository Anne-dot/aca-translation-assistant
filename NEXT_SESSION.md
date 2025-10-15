# Next Session - 2025-10-16

## ⚠️ FIRST: Read These Before Starting

**CRITICAL - Read every time before continuing work:**
1. `~/.claude/instructions.md` - Global non-negotiable requirements (always follow this as primary source)
2. `AI_COLLABORATION_GUIDE.md` - Project collaboration rules (if exists)
3. **If this is after compacting:** Read compacting summary to get back to speed

**Important:** All work must follow `~/.claude/instructions.md` principles - 29 line limit, show TEXT first, ask open questions, NO SILENT FAILURES, ADHD-friendly code.

## Where We Left Off (2025-10-15)

**Issue #4 completed and closed:**
- ✅ Implemented matching algorithm for Glossary + EKI
- ✅ Aggressive normalization (handle `(n.)`, `(v.)`, newlines)
- ✅ Match rate: 10/845 (1.2%) - expected (EKI specialized, Glossary general)
- ✅ Created CSV files for manual review
- ✅ Output: `data/aca-glossary-eki.json`, `data/glossary-review.csv`, `data/eki-terms.csv`

**Issue #5 completed and closed:**
- ✅ Refactored shared code to `src/utils.py` (DRY principle)
- ✅ 5 utility functions created
- ✅ 3 scripts refactored and tested
- ✅ Updated `~/.claude/instructions.md` with utils rule

**Documentation updated:**
- ✅ PROJECT_OVERVIEW_DRAFT.md - status and date updated
- ✅ NEXT_SESSION.md - updated for next session
- ✅ Created `docs/MANUAL_REVIEW_GUIDE.md` - guide for manual JSON editing

**Key decision:** Low match rate expected - EKI = specialized therapy terms, Glossary = general ACA vocabulary

## Next Concrete Step

**Manuaalne ülevaatus: matched terminid ja CSV failid**

### Mida teha

**1. Ava failid**
```bash
code data/aca-glossary-eki.json
# Ava CSV failid Excelis/Google Sheetsis
```

**2. Kontrolli 10 automaatselt matchitud terminit**
- Ava `data/glossary-review.csv` Excelis
- Sorteeri Match_Status järgi (matched enne)
- Kontrolli üle kas tõlked sobivad
- Valideeri domain ja definitsioonid

**3. Otsi käsitsi lisamatche**
- Võrdle Glossary EN termineid EKI EN terminitega
- Kasuta `data/eki-terms.csv` abimaterjalina (564 EN→ET paari)
- Märgi leitud matchid JSON-i (vt juhend)
- Lisa `match_confidence: "manual"`

**4. Märgi homonüümid**
- Terminid, millel mitu tähendust (nt "abuse" - noun vs verb)
- Notes veerg sisaldab `(n.)`, `(v.)`, `(to)` markereid - need on kandidaadid
- Lisa JSON-i teine sense (vt juhend)
- Lisa `part_of_speech` väli (ISO 704 standard)

**5. Checkpoint iga 25 termini järel**
- Salvesta `data/aca-glossary-eki.json`
- Valideeri: `python3 -m json.tool data/aca-glossary-eki.json > /dev/null`
- Tee märkmeid, mida leidsid

**Detailne juhend:** Vaata `docs/MANUAL_REVIEW_GUIDE.md`

### Failid
- **Muudetav:** `data/aca-glossary-eki.json` - terminibaas
- **Vaatamiseks:** `data/glossary-review.csv` (826 terminit)
- **Vaatamiseks:** `data/eki-terms.csv` (564 EN→ET paari)
- **Juhend:** `docs/MANUAL_REVIEW_GUIDE.md`

### Success criteria
✅ 10 matched terminit valideeritud
✅ Käsitsi lisamatchid leitud ja märgitud
✅ Homonüümid identifitseeritud ja märgitud
✅ JSON korrektne ja valideeritud
✅ Valmis järgmiseks enrichment sammuks

## After This
1. **Review closed issues and update documentation**
   - **Thoroughly review all closed issue comments** (Issues #4, #5, #6)
   - Extract important decisions, findings, and changes
   - **Update PROJECT_OVERVIEW_DRAFT.md** based on issue details:
     - Step 1B-4 with correct additional sources
     - Manual review process (checkpoints, workflow)
     - Any other decisions made in issue comments
   - **Update DECISIONS.md** with strategic decisions from issues
   - Follow workflow: GitHub Issues (active work) → Documentation (after closing)

2. **Review remaining .md files** - clean up or archive:
   - `EXISTING_TOOLS_ANALYSIS.md` - review if still needed or archive
   - `PERSONAL_THOUGHTS.md` - personal file, keep as is
   - `eki_analüüs/README.md` - old analysis, consider archiving

3. Create issue for structured manual review workflow (if needed)
4. Manual review of Estonian-only terms (262 total from EKI)
5. 1B-Step4: Enrich with additional sources (IATE, Eurotermbank, Aare, Sonaveeb)
6. 1C: Extract from ATL existing translations

## Important Context
- See Issue #4 for matching decisions: https://github.com/Anne-dot/aca-translation-assistant/issues/4
- See Issue #5 for refactoring: https://github.com/Anne-dot/aca-translation-assistant/issues/5
- Manual review is hands-on work with JSON + CSV files
- `part_of_speech` field added following ISO 704 lexicography standards
