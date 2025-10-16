# Existing Tools Analysis for ACA Translation Project

**Date:** 2025-10-14
**Context:** Analysis of existing translation tools vs building custom solution
**Project:** ATL (ACA Estonia) Translation Assistant

---

## Executive Summary

**Key Finding:** Don't build everything from scratch. Use existing open source tools and integrate your unique value (ACA-specific terminology database).

**Recommended Approach:**
- ✅ **BUILD:** ACA terminology database (EKI + Glossary + ATL translations) - YOUR UNIQUE VALUE
- ❌ **DON'T BUILD:** Translation memory system, web platform, machine translation engine
- ✅ **INTEGRATE:** Existing professional tools with your terminology database

**Total Cost:** €10-20/month

---

## Critical Questions Answered

### Q1: Can we just use AI for translation?

**Answer:** Yes, but with terminology control.

**Best AI for Estonian:**
1. **DeepL API** - Best quality (€5-10/month)
2. **Claude API** - Good with terminology prompts (~$5/month with caching)
3. **LibreTranslate** - Free but lower quality

**Why you still need your terminology database:**
- AI doesn't know ACA-specific Estonian terminology
- Consistency across documents requires terminology enforcement
- Your EKI + Glossary + ATL combinations are unique

---

### Q2: Is the project public or private?

**Your Situation:** PRIVATE (ACA copyright, community-based review but not freely usable after)

**Impact:**
- ❌ **Weblate Libre (free)** requires public project - NOT suitable
- ✅ Must use private solutions: POEditor ($15/month) or self-hosted Tolgee (free + €5 VPS)

---

## Milestone-by-Milestone Analysis

### Milestone 1: Terminology Database ✅ KEEP YOUR CURRENT WORK

**What you're building:**
- Collecting EKI terms (1,265 terms from 4 databases)
- Matching with Glossary (845 terms)
- Adding ATL existing translations
- Output: JSON/CSV format

**Why this is VALUABLE:**
- ✅ ACA-specific Estonian terminology database DOESN'T EXIST elsewhere
- ✅ Estonian psychotherapy terminology + ACA context is UNIQUE
- ✅ Foundation for everything else
- ✅ Can export to any format (OmegaT TSV, DeepL CSV, JSON API)

**RECOMMENDATION:** ✅ **CONTINUE THIS WORK!**

**What to add:**
- Git version control (backup + history)
- Export scripts to multiple formats

**Cost:** FREE

---

### Milestone 2: Personal CLI Translation Assistant

**Your Original Plan:** Build CLI tool from scratch

**Better Alternative:** **OmegaT + DeepL API + Your Terminology Database**

#### Option A: OmegaT + DeepL API ⭐ RECOMMENDED

**Stack:**
- **OmegaT:** Free open source CAT tool (GPL license)
- **DeepL API:** Best Estonian translation quality
- **Your terminology:** Export to OmegaT glossary format (TSV)

**How it works:**
1. Your terminology database → export to `glossary.tsv`
2. OmegaT loads glossary automatically
3. DeepL API provides machine translation suggestions
4. OmegaT shows BOTH: your terminology + DeepL suggestion
5. Translator sees terminology highlighted in text

**What you DON'T need to build:**
- ❌ Translation memory system (OmegaT does this)
- ❌ Glossary management UI (OmegaT shows automatically)
- ❌ File format support (OmegaT supports .docx, .txt, .pdf, etc.)
- ❌ TMX/XLIFF format handling (OmegaT standard)

**What you SHOULD build:**
- ✅ Small script: `terminibaas.json` → `omegat_glossary.tsv`
- ✅ (Optional) Python wrapper for DeepL API with terminology validation

**Cost:** €5-10/month (DeepL API after 500k free chars)

---

#### Option B: OmegaT + LibreTranslate (Fully Free)

**Stack:**
- **OmegaT:** Free CAT tool
- **LibreTranslate:** Free open source MT (self-hosted)
- **Your terminology:** Same glossary approach

**Pros:**
- ✅ Completely free
- ✅ Full privacy (self-hosted)
- ✅ No usage limits

**Cons:**
- ⚠️ Translation quality lower than DeepL
- ⚠️ Requires server setup (~€5/month VPS)

**Cost:** €5/month (VPS hosting)

---

#### Option C: Build Custom CLI (Original Plan)

**What you'd need to build:**
- Translation memory system
- Glossary matching engine
- File format parsers (.docx, .txt, .pdf)
- Machine translation API integration
- Progress tracking
- Export/import functionality
- CLI interface

**Cost:** FREE (your time)
**Result:** Reinventing the wheel (OmegaT already does all this)

---

#### RECOMMENDATION for Milestone 2:

**Start with Option A (OmegaT + DeepL)**
- Best translation quality
- Professional-grade tool
- Can always build custom later if needed

---

### Milestone 3: Estonian Community Web Tool

**Your Original Plan:** Build web-based collaboration platform

**Better Alternatives:** Use existing translation platforms

#### Option A: POEditor Start Plan - $14.99/month ⭐ SIMPLEST

**Features:**
- ✅ 3,000 strings limit
- ✅ Unlimited projects
- ✅ Unlimited collaborators (!!!)
- ✅ Private project
- ✅ Review workflow (translation → proofreading)
- ✅ Comments and suggestions
- ✅ Machine translation integration
- ✅ API access
- ✅ No technical setup required

**Pros:**
- Simple, user-friendly interface
- No server management
- All features included (no tiered features)
- Affordable for small community

**Cons:**
- Not open source (cloud SaaS)
- String limit (3,000 might be limiting for large projects)

**Cost:** $14.99/month (~€14/month)
**ATL 7th Tradition:** ✅ Affordable for community

---

#### Option B: Tolgee (Self-Hosted) - FREE ⭐ BEST OPEN SOURCE

**Features:**
- ✅ UNLIMITED strings/projects/users
- ✅ Completely free (open source, Apache 2.0 license)
- ✅ Private project
- ✅ Modern, developer-friendly UI
- ✅ In-context translation (ALT+click)
- ✅ Translation memory
- ✅ Machine translation (DeepL, Google)
- ✅ Activity log
- ✅ Can modify source code if needed

**Pros:**
- Free forever
- Modern interface
- Full control over data
- Open source (can customize)
- No artificial limits

**Cons:**
- Requires server (~€5-10/month VPS)
- Technical setup required
- Smaller community than Weblate

**Cost:** €5-10/month (VPS hosting only)

**Tech Requirements:**
- Docker knowledge
- VPS server (DigitalOcean, Hetzner, etc.)
- Basic Linux admin skills

---

#### Option C: Weblate (Self-Hosted) - FREE

**Features:**
- ✅ Free open source (GPL)
- ✅ Most mature translation platform
- ✅ Full-featured (no limitations)
- ✅ Git integration (automatic commits)
- ✅ Translation memory
- ✅ Quality checks
- ✅ Multiple MT integrations

**Pros:**
- Most feature-rich
- Strong Git integration
- Very mature and stable
- Large community

**Cons:**
- More complex setup than Tolgee
- Less modern UI
- Requires more server resources

**Cost:** €5-10/month (VPS hosting)

---

#### Option D: Build Custom Platform (Original Plan)

**What you'd need to build:**
- User authentication and roles
- Project management
- Translation interface
- Review workflow
- Comment system
- Translation memory
- Terminology management UI
- Progress tracking
- Export/import
- API
- Database design
- Security

**Cost:** Your time
**Maintenance:** Ongoing (security updates, bug fixes)

---

#### RECOMMENDATION for Milestone 3:

**For quick start with no technical skills:**
→ **POEditor** ($14.99/month) - Works immediately

**For technical team wanting open source:**
→ **Tolgee self-hosted** (€5-10/month VPS) - Modern UI, easier setup

**For maximum features and maturity:**
→ **Weblate self-hosted** (€5-10/month VPS) - Industry standard

---

### Milestone 4: Multi-Language Platform

**Your Original Plan:** Build universal platform for global ACA communities

**Reality Check:** This already exists!

#### Existing Solution: Weblate

**Weblate already IS a multi-language platform:**
- ✅ Supports unlimited languages
- ✅ Used by 2,500+ libre projects worldwide
- ✅ Scales to millions of strings
- ✅ Multiple organizations can use it
- ✅ Self-hosted = complete control
- ✅ Free forever if self-hosted

**What you'd add:**
- ✅ ACA-specific terminology databases for each language
- ✅ ACA translation guidelines documentation
- ✅ Onboarding materials for new language teams

**Cost (self-hosted):** €20-50/month (larger VPS for multiple communities)

---

## AI Translation Quality Comparison

**For 10,000 word document translation to Estonian:**

| AI Service | Cost | Quality | Edits Required | Best For |
|------------|------|---------|----------------|----------|
| **DeepL API** | €0.25 | ⭐⭐⭐⭐⭐ | 100 edits | Best quality |
| **Claude Sonnet 4.5** | $0.27 | ⭐⭐⭐⭐ | 150 edits | Context-aware |
| **GPT-4o** | $0.20 | ⭐⭐⭐ | 300 edits | General purpose |
| **LibreTranslate** | FREE | ⭐⭐ | 500+ edits | Privacy/free |

**Source:** Blind tests comparing MT outputs for Estonian

**Recommendation:** DeepL API for best Estonian quality

---

## Cost Comparison: Build vs Integrate

### Scenario A: Build Everything From Scratch

**Ongoing costs:**
- Server hosting: €20-50/month
- Maintenance: Ongoing (security updates, bug fixes)

**Monetary cost:** €20-50/month

---

### Scenario B: Integrate Existing Tools (Recommended)

**Ongoing costs:**
- Option A (managed): POEditor $15/month + DeepL €5/month = €20/month
- Option B (self-hosted): VPS €10/month + DeepL €5/month = €15/month

**Monetary cost:** €15-20/month

---

## Recommended Technology Stack

### RECOMMENDED STACK (€15-20/month total)

**Milestone 1: Terminology Database**
- Format: JSON + CSV exports
- Storage: Git repository (GitHub/GitLab)
- Tools: Python scripts for data processing
- **Cost:** FREE

**Milestone 2: Personal CLI Assistant**
- **OmegaT** (desktop CAT tool) - FREE
- **DeepL API** (machine translation) - €5-10/month
- **Your terminology** → OmegaT glossary format (TSV)
- **Cost:** €5-10/month

**Milestone 3: Estonian Community Tool**
- **Option A:** POEditor Start Plan - $14.99/month
- **Option B:** Tolgee self-hosted - €5-10/month (VPS)
- **Cost:** €5-15/month

**Milestone 4: Global Platform**
- **Weblate** self-hosted - €10-20/month (larger VPS)
- Multiple terminology databases (one per language)
- **Cost:** €10-20/month

**TOTAL:** €15-20/month (or €20-25 if using POEditor)

---

### ALTERNATIVE: Fully Free Stack (€5/month)

**If budget is absolutely zero:**

**Milestone 1:** JSON/CSV in Git - FREE
**Milestone 2:** OmegaT + LibreTranslate - FREE (self-hosted)
**Milestone 3:** Tolgee self-hosted - €5/month (VPS)
**Milestone 4:** Weblate self-hosted - €10/month (VPS)

**TOTAL:** €5-10/month

**Trade-off:** Lower MT quality, more technical setup required

---

## What You Should Build (Your Unique Value)

### 1. ACA Terminology Database ✅ CONTINUE

**This is YOUR unique contribution:**
- EKI terms (1,265 from 4 databases)
- Glossary matches (845 terms)
- ATL existing translation pairs
- Estonian psychotherapy + ACA terminology

**Format:**
- Primary: JSON (flexible, API-ready)
- Exports: TSV (OmegaT), CSV (DeepL), TMX (universal)

**Nobody else has this!**

---

### 2. Export Scripts ✅ BUILD

**What you need:**
```python
# terminibaas_to_omegat.py
# Converts terminibaas.json → omegat_glossary.tsv

# terminibaas_to_deepl.py
# Converts terminibaas.json → deepl_glossary.csv

# terminibaas_to_weblate.py
# Converts terminibaas.json → weblate import format
```

**Value:** Bridges your unique data to all tools

---

### 3. ACA Translation Guidelines Documentation ✅ BUILD

**What you need:**
- How to use ACA terminology consistently
- Translation style guide (formal/informal, terminology choices)
- Review process documentation
- Quality criteria

**Format:** Markdown documentation
**Value:** Ensures consistent translation across translators

---

## What You Should NOT Build

### ❌ Don't Build: Translation Memory System
**Why:** OmegaT, Weblate, Tolgee all have this

### ❌ Don't Build: Web-based Translation Interface
**Why:** POEditor, Tolgee, Weblate already exist

### ❌ Don't Build: User Authentication & Roles
**Why:** All platforms have this built-in

### ❌ Don't Build: Machine Translation Engine
**Why:** DeepL API, Claude API already excellent (impossible to match quality)

### ❌ Don't Build: File Format Parsers
**Why:** OmegaT supports 40+ formats

---

## Implementation Roadmap

### Week 1-2: Complete Milestone 1

1. ✅ Finish terminology database (EKI + Glossary + ATL)
2. ✅ Add Git version control
3. ✅ Create export scripts (JSON → TSV/CSV)
4. ✅ Test exports with sample data

**Deliverable:** Complete ACA Estonian terminology database

---

### Week 3-4: Implement Milestone 2

1. Download and install OmegaT
2. Create first OmegaT project
3. Import your terminology (TSV format)
4. Sign up for DeepL API free tier (500k chars/month)
5. Configure OmegaT to use DeepL plugin
6. Translate 2-3 sample documents
7. Evaluate workflow

**Deliverable:** Working personal translation workflow

---

### Week 5-6: Setup Milestone 3

**Option A (Simple):**
1. Sign up for POEditor Start plan ($14.99/month)
2. Import terminology
3. Upload 5 sample documents
4. Invite 3 beta testers
5. Test review workflow

**Option B (Technical):**
1. Rent VPS server (€5-10/month)
2. Install Docker
3. Deploy Tolgee
4. Configure users and projects
5. Import terminology
6. Test with beta team

**Deliverable:** Community translation platform ready

---

### Month 2: Beta Testing

1. Translate 10-15 documents with team
2. Refine terminology based on feedback
3. Document workflow and guidelines
4. Train new translators
5. Establish quality review process

**Deliverable:** Proven translation workflow

---

### Month 3-4: Launch to Estonian Community

1. Finalize terminology
2. Create user documentation (Estonian)
3. Launch to broader ATL community
4. Gather feedback
5. Iterate on process

**Deliverable:** Production-ready Estonian translation system

---

### Month 5-12: Expand to Other Languages (Milestone 4)

1. Document the process for new languages
2. Set up Weblate for multi-language support
3. Create templates for new terminology databases
4. Reach out to other ACA language communities
5. Onboard first additional language (Lithuanian? Latvian? Finnish?)

**Deliverable:** Multi-language platform

---

## Decision Matrix

### Should I build custom or use existing tool?

**Build custom IF:**
- ✅ Functionality doesn't exist anywhere
- ✅ Existing tools don't meet specific need
- ✅ Integration cost > build cost
- ✅ You have 6+ months development time
- ✅ You have ongoing maintenance capacity

**Use existing tool IF:**
- ✅ 80% of features already exist
- ✅ Mature, stable, well-supported
- ✅ Free or affordable
- ✅ Can integrate with your unique data
- ✅ Saves months of development time

---

## Questions to Answer Before Deciding

### 1. Privacy & Copyright
- ✅ **Answered:** Project must be PRIVATE (ACA copyright)
- Impact: Can't use Weblate Libre free tier

### 2. Budget Reality
- ❓ **Question:** Can ATL sustain €15-20/month?
- ATL 7th Tradition: Groups are self-supporting
- €15-20/month is very affordable

### 3. Technical Capacity
- ❓ **Question:** Can you self-host (Docker, Linux)?
- If YES → Tolgee/Weblate self-hosted (free + VPS)
- If NO → POEditor managed ($15/month)

### 4. Team Size
- ❓ **Question:** How many active translators?
- 1-3 people: OmegaT + Google Docs is enough
- 5-10 people: Need proper platform (POEditor/Tolgee)
- 10+ people: Need Weblate-level features

### 5. Translation Volume
- ❓ **Question:** How many words need translation?
- Affects: Platform choice, API costs
- ACA Big Red Book: ~150,000 words
- Daily meditations: ~130,000 words (365 × ~350 words)

### 6. ACA Official Authorization
- ❓ **Question:** Has ACA Translation Subcommittee been contacted?
- **IMPORTANT:** You must work with ACA WSO Translation Sub-Committee
- They provide guidelines and must approve translations
- Contact: https://acawso.org/translations/

### 7. Timeline
- ❓ **Question:** When do you need this ready?
- Build from scratch vs integrate existing tools affects timeline significantly

---

## Final Recommendation

### DO THIS:

**✅ Phase 1 (Now - 2 weeks):**
1. Finish Milestone 1 (terminology database) - YOUR UNIQUE VALUE
2. Create export scripts (JSON → TSV/CSV/TMX)
3. Set up Git version control

**✅ Phase 2 (Weeks 3-4):**
1. Download OmegaT
2. Create first project with your terminology
3. Test DeepL API free tier (500k chars)
4. Translate 2-3 documents to validate workflow

**✅ Phase 3 (Weeks 5-6):**
1. Decide: POEditor (simple) or Tolgee (technical)
2. Set up platform
3. Import terminology
4. Invite 3-5 beta testers

**✅ Phase 4 (Month 2-3):**
1. Beta testing with real documents
2. Refine process
3. Launch to Estonian community

---

### DON'T DO THIS:

**❌ Don't build custom CLI from scratch**
→ Use OmegaT

**❌ Don't build web platform from scratch**
→ Use Tolgee/POEditor/Weblate

**❌ Don't build machine translation engine**
→ Use DeepL API (impossible to match quality)

**❌ Don't reinvent translation memory**
→ Use standard TMX format with existing tools

---

## Cost Summary

### Recommended Stack Total Cost:

**Monthly:**
- DeepL API: €5-10/month
- Tolgee VPS: €5-10/month (or POEditor $15/month)
- **TOTAL: €10-20/month**

**One-time:**
- Domain name (optional): €10/year
- SSL certificate: FREE (Let's Encrypt)

**Maintenance:**
- Estimated: 2-5 hours/month (significantly less than custom-built solution)

---

## Conclusion

**Your original project vision was correct:** ACA needs better translation tools.

**Your unique contribution:** ACA-specific Estonian terminology database (EKI + Glossary + ATL).

**Where to optimize:** Don't build infrastructure that already exists. Use professional open source tools and integrate your unique terminology data.

**Result:**
- Professional quality tools (battle-tested by thousands of projects)
- Lower maintenance burden
- More time for your unique value (terminology curation and ACA-specific guidelines)

**This is not "giving up" on your vision** - it's being smart about where to invest your limited time and resources.

---

**Next Step:** Review this analysis and decide which path forward makes sense for ATL community.

**Questions to discuss:**
1. Can ATL afford €15-20/month? (7th Tradition self-supporting)
2. Do you have technical skills for self-hosting? (affects platform choice)
3. What's the priority: speed to launch or full control?
4. Have you contacted ACA Translation Subcommittee yet?

---

**Document Version:** 1.0
**Created:** 2025-10-14
**Author:** Claude AI (based on extensive research and analysis)
**Project:** ATL (ACA Estonia) Translation Assistant
