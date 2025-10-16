# ISO Standards for Terminology Work

This document summarizes the ISO standards used in this project for terminology database design and term classification.

---

## ISO 704:2022 - Terminology work: Principles and methods

**Official page:** https://www.iso.org/standard/79077.html
**Edition:** 4th edition (July 2022), replaces 2009 version
**Price:** CHF 199 (paid standard)

### Scope

Establishes the basic principles and methods for preparing and compiling terminologies both inside and outside the framework of standardization.

Applicable to terminology work in scientific, technological, industrial, legal, administrative and other fields of knowledge.

### Core Principles

**Objects → Concepts → Designations & Definitions**

Objects are perceived or conceived and abstracted into concepts which, in special languages, are represented by designations and/or definitions.

**Key Elements:**

1. **Concept Systems**
   - How concepts relate to each other
   - Hierarchical and associative relationships
   - Systematic organization of knowledge domains

2. **Characteristics**
   - Used for analyzing concepts
   - Used for developing concept systems
   - Used for writing definitions
   - Should guide selection and formation of designations

3. **Designation Formation**
   - General principles for forming terms and proper names
   - Rules for creating consistent terminology

4. **Definition Writing**
   - Principles for formulating definitions
   - Clarity and precision requirements
   - Relationship to concept characteristics

### Application in This Project

- **Structured data fields:** `part_of_speech`, `definition`, `notes`
- **Concept relationships:** Links between terms, source tracking
- **Definition requirements:** Clear, precise definitions from authoritative sources
- **Issue #6:** Added `part_of_speech` field following ISO 704 compliance

---

## ISO 1087:2019 - Terminology work and terminology science: Vocabulary

**Official page:** https://www.iso.org/standard/62330.html
**Edition:** Published September 2019, replaces ISO 1087-1:2000
**Pages:** Approximately 46 pages
**Price:** CHF 43 (paid standard)

### Scope

Establishes basic terms and definitions for terminology work and terminology science.

Target audience: standardizers, terminologists, individuals involved in terminology work, terminology users, researchers and professionals dealing with terminology science and/or natural language processing.

### Term Classification

ISO 1087 defines three types of terms based on their structure:

#### 1. Simple Term (clauses 3.4.6, 3.4.7)

**Definition:** A term that consists of a single word or lexical unit.

**Examples:**
- sound
- light
- barrier
- virus
- viral
- accessory
- accessorize

**Characteristics:**
- One word only
- No spaces or hyphens
- May have inflections (e.g., virus → viral)

---

#### 2. Compound Term (clause 3.4.8)

**Definition:** A simple term that can be split morphologically into separate components.

**Examples:**
- steamship (steam + ship)
- blackbird (black + bird)
- afterbirth (after + birth)

**Characteristics:**
- Written as one word (no spaces)
- Can be analyzed into meaningful components
- Components combine to create new meaning

---

#### 3. Complex Term (clauses 3.4.9, 3.4.10)

**Definition:** A term that consists of more than one word or lexical unit.

**Examples:**
- computer mouse
- fault recognition circuit
- adult child
- addictive behavior
- inner child

**Characteristics:**
- Multiple words separated by spaces
- Each word retains independent meaning
- Combined meaning may be literal or specialized

### Application in This Project

**Issue #7:** Added `term_complexity` field to classify all 826 ACA Glossary terms

**Statistics from classification:**
- **Simple terms:** 613 (74.2%)
- **Complex terms:** 187 (22.6%) - multi-word phrases
- **Compound terms:** 26 (3.1%) - hyphenated terms

**Impact:**
- Complex and compound terms (213 total) require component extraction
- Components need separate lookup in terminology databases
- Helps interpret Sonaveeb results (complex ACA terms unlikely in standard databases)

**See:** `src/add_term_complexity.py` for implementation

---

## References

### Official ISO Pages

- **ISO 704:2022:** https://www.iso.org/standard/79077.html
- **ISO 1087:2019:** https://www.iso.org/standard/62330.html

### Additional Resources

- **Wikipedia - ISO 704:** https://en.wikipedia.org/wiki/ISO_704
- **ISO/TC 37** (Terminology and language resources): https://en.wikipedia.org/wiki/ISO/TC_37

### Sample Documents

Note: Full ISO standards are paid documents. Sample excerpts may be available:
- ISO 704:2022 sample: https://cdn.standards.iteh.ai/samples/79077/
- ISO 1087:2019 sample: https://cdn.standards.iteh.ai/samples/62330/

---

## Usage Notes

**Why these standards matter:**

1. **International compatibility** - Following established standards ensures our terminology work is compatible with professional terminology databases and translation workflows worldwide

2. **Structured approach** - ISO standards provide systematic methodology for complex terminology work, preventing ad-hoc decisions

3. **Quality assurance** - Professional terminology management ensures consistency and accuracy in translations

4. **Future scalability** - Standards-compliant structure enables integration with other terminology tools and databases

**Project compliance:**
- All data structures follow ISO 704 principles
- Term classification uses ISO 1087 definitions
- Field naming and organization align with standard terminology practices

---

**Last Updated:** 2025-10-16
