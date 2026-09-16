# Coding Standards

**Project:** ACA Translation Assistant
**Status:** Draft - under discussion
**Last updated:** 2026-09-16

---

## How to Use This Document

This is the **Single Source of Truth** for coding standards in this project.

- **Don't duplicate** these rules elsewhere
- **Reference this file** when needed
- **Status markers:** Each rule shows who proposed it and its status:
  - `[Henri]` - proposed by Henri
  - `[Anne]` - proposed by Anne
  - `[Agreed]` - confirmed by both
  - `[Discuss]` - needs discussion

---

## References (avatud soovitustele)

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/) (official Python style guide)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [The Hitchhiker's Guide to Python - Code Style](https://docs.python-guide.org/writing/style/)

---

## 1. Naming Conventions

| Type | Convention | Example | Status |
|------|------------|---------|--------|
| Variables, functions | `snake_case` | `term_count`, `load_glossary()` | `[Henri]` `[Anne]` |
| Constants | `ALL_CAPS` | `MAX_RETRIES`, `DEFAULT_PATH` | `[Henri]` |
| Classes | `UpperCamelCase` | `GlossaryTerm`, `ReviewSession` | `[Henri]` |

**Rules:**
- `[Henri]` Variable names are either single letter (small scope only, max ~50 lines) or completely unabbreviated. Single letter for iteration (indexes, ...) and i.e generic function to remove padding for string - factory - step by step; formulas. 
- `[Anne]` No abbreviations except widely-known acronyms (api, json, etc.). Abbreviation widely used already outside of coding (ACA abbreviation in upper case since it is written so in normal writing)
- `[Anne]` Names must be self-explanatory.

- sobib

---

## 2. Formatting `[Agreed]`

Formatting is handled by [Black](https://black.readthedocs.io/). Decided
2026-09-16. Black supersedes the earlier layout rules (line length,
indentation, line breaks, blank lines, spaces around `=` in keyword
arguments, quote style). Configuration lives in `pyproject.toml`.

Open: line length (Black default 88, earlier target 80).

---

## 3. Comments `[Henri]`

Comments are **only** for:

1. **File headers / docstrings** - purpose of the file
2. **Section dividers** - visual separation of major sections:
```python
#==============================================================================#
# STATISTICS                                                                   #
#==============================================================================#
```
3. **Why, not what** - explain *why* code exists, never *what* it does
4. **Pseudocode** töö ajal
5. **Todo notes** töö ajal

**Never** write comments that describe what code does. If code needs explanation, refactor it or rename variables.

- sobib

---

## 4. Console Output `[Henri]` `[Discuss]`

- **No emojis or non-ASCII characters** in code output
- Use instead:
  - ASCII art for visual elements
  - ANSI escape codes for colors (via module if needed) - Anne ütleb: "Super!"
  - "Irregular" punctuation for emphasis: `!!Save failed:`

**Rationale:** Emojis are hard to write/change, unreliable to render on CLI, and complicate testing.

**Note:** Anne currently uses emojis in some scripts for visual feedback. Needs discussion. Nõus. 
**Note:** Anne annab AI-le juhendi, et emoji on ok dokumentatsioonis ja ei ole okei cli programmides.

- sobib. Ülioluline! Emojod saavad bänni!!!!

---

## 5. Architecture Principles `[Anne]`

### ADHD-friendly Code
- One file = one purpose
- One function = one purpose
- Visual separators in code
- Immediate feedback (progress indicators, status messages)

### Core Principles
- **DRY** (Don't Repeat Yourself) - Ära kirjuta sama asja mitmesse kohta. 
- **KISS** (Keep It Simple)
- **MVP-first** (working > perfect) = **Progressive Enhancement** (make it work → make it right → make it fast)
- **Modular** (small, focused functions)
- **Single Source of Truth**
- **Defensive Programming**

### Code Reuse
When a function/pattern repeats 2+ times across files:
- Extract to `src/utils.py`
- Import where needed

### When to Split Modules
Split when file grows and natural grouping emerges. Don't force splitting - keep code in one file as long as it's logical and understandable. When it grows and natural groupings appear, then split. ([Issue #31](https://github.com/Anne-dot/aca-translation-assistant/issues/31))

### Minimum Python version `[Agreed]`
The project minimum is **Python 3.12** (agreed 2026-08-26; supersedes the
earlier 3.10+ proposal). Reasons: `match/case` needs 3.10+ anyway; Python
3.10 reaches end-of-life in October 2026; and PEP 701 (3.12) removes the
f-string quote restriction, so the double-quote convention applies uniformly
with no exceptions. The minimum is also documented in README's technology
stack.

---

## 6. Error Handling `[Anne]`

- **NO SILENT FAILURES**
- Errors must always be visible
- Use clear error messages that help debugging

```python
# BAD - silent failure
def load_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return None  # Caller has no idea what went wrong

# GOOD - visible failure
def load_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"!!Error: File not found: {path}")
        raise
    except PermissionError:
        print(f"!!Error: Permission denied: {path}")
        raise
```

- sobib. Mõlemad nõus, et see on oluline.

---

## 7. What to Avoid `[Anne]` `[Henri]`

### Callback Hell
```python
# BAD
- koodimatrjoska, rekusrsive, loopime. väldid stack overflowd, mingi väljumise strateegia, safety check.

# GOOD
data = get_data()
processed = process_data(data)
save_data(processed)
notify()
```

TODO: Anne - lisa parem näide (Henri näide Discordis)

### Premature Optimization
```python
# BAD - optimizing for 10 items
cache = WeakValueDictionary()
def get_term(id):
    if id not in cache:
        cache[id] = load_from_db(id)
    return cache[id]

# GOOD - simple, works, optimize later if needed
def get_term(id):
    return load_from_db(id)
```

### Over-abstraction
```python
# BAD
class AbstractTermLoaderFactoryInterface:
    def create_loader(self):
        return TermLoaderFactory().create()

# GOOD
def load_terms(path):
    with open(path) as f:
        return json.load(f)
```

---

## 8. OOP vs Functions `[Agreed]`

Use classes only when needed (e.g., creating new data types). Otherwise prefer functions.

```python
# Use CLASS for real-world entity with state
class GlossaryTerm:
    def __init__(self, english, estonian):
        self.english = english
        self.estonian = estonian
        self.reviewed = False

# Use FUNCTION for simple transformation
def format_term_for_display(term):
    return f"{term.english} → {term.estonian}"
```

- sobib 

---

## 9. Tooling

Formatter: Black (see section 2). Linter and editor setup: see
[Issue #30](https://github.com/Anne-dot/aca-translation-assistant/issues/30).

---


## 10. Commit Requirements `[Agreed]`

- Every commit must at minimum pass `python3 -m py_compile` on all touched
  Python files.
- Scripts should be run end-to-end before committing whenever the branch has
  the data to do so; if not possible, say so in the commit message.

Proposed by Anne, agreed by Henri in [Issue #29](https://github.com/Anne-dot/aca-translation-assistant/issues/29).

---

## Discussion Log

See [Issue #29](https://github.com/Anne-dot/aca-translation-assistant/issues/29) for full discussion.
