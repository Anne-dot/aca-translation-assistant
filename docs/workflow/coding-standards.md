# Coding Standards

**Project:** ACA Translation Assistant
**Status:** Draft - under discussion
**Last updated:** 2025-12-10

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

## References

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
- `[Henri]` Variable names are either single letter (small scope only, max ~50 lines) or completely unabbreviated
- `[Anne]` No abbreviations except widely-known acronyms (API, JSON, etc.)
- `[Anne]` Names must be self-explanatory

---

## 2. Code Layout

### Line Length `[Henri]`
- **Target:** 80 characters
- **Maximum:** 100 characters (strings/comments only, in extreme cases)
- Never start a word past column 80

### Indentation `[Henri]`
- Use **tabs** for indentation
- Use **spaces** for alignment within lines
- Keep indentation on "empty lines" for clarity in diffs

### Line Breaks `[Henri]`
Prefer indentation-based alignment over spacing alignment:

```python
# Preferred
foo = long_function_name(
	var_one, var_two,
	var_three, var_four
)

# Avoid
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

### Blank Lines `[Henri]`
- 1 blank line between logical sections within a function
- 3 blank lines between top-level functions
- 3 blank lines before section dividers

---

## 3. Strings and Characters `[Henri]`

- **Double quotes** (`"`) for strings (default)
- **Single quotes** (`'`) only for:
  - Character literals
  - Strings containing double quotes

---

## 4. Comments `[Henri]`

Comments are **only** for:

1. **File headers** - purpose of the file
2. **Section dividers** - visual separation of major sections:
```python
#==============================================================================#
# STATISTICS                                                                   #
#==============================================================================#
```
3. **Why, not what** - explain *why* code exists, never *what* it does

**Never** write comments that describe what code does. If code needs explanation, refactor it or rename variables.

---

## 5. Console Output `[Henri]` `[Discuss]`

- **No emojis or non-ASCII characters** in code output
- Use instead:
  - ASCII art for visual elements
  - ANSI escape codes for colors (via module if needed)
  - "Irregular" punctuation for emphasis: `!!Save failed:`

**Rationale:** Emojis are hard to write/change, unreliable to render on CLI, and complicate testing.

**Note:** Anne currently uses emojis in some scripts for visual feedback. Needs discussion.

---

## 6. Architecture Principles `[Anne]`

### ADHD-friendly Code
- One file = one purpose
- One function = one purpose
- Visual separators in code
- Immediate feedback (progress indicators, status messages)

### Core Principles
- **DRY** (Don't Repeat Yourself)
- **KISS** (Keep It Simple)
- **MVP-first** (working > perfect)
- **Modular** (small, focused functions)
- **Single Source of Truth**
- **Progressive Enhancement** (make it work → make it right → make it fast)

### Code Reuse
When a function/pattern repeats 2+ times across files:
- Extract to `src/utils.py`
- Import where needed

---

## 7. Error Handling `[Anne]`

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

---

## 8. What to Avoid `[Anne]` `[Henri]`

### Callback Hell
```python
# BAD
get_data(lambda a:
    process_data(a, lambda b:
        save_data(b, lambda c:
            notify(c))))

# GOOD
data = get_data()
processed = process_data(data)
save_data(processed)
notify()
```

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

## 9. OOP vs Functions `[Anne]` `[Discuss]`

**Anne's approach:** Pragmatic OOP - use classes for entities, functions for transformations.

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

**Question for Henri:** What is your stance on OOP? When to use classes vs functions?

---

## 10. Tooling (Future) `[Discuss]`

Consider adopting:
- `black` - auto-formatter (with custom line length)
- `flake8` - linter
- `mypy` - type checking
- Pre-commit hooks

**Note:** Tabs vs spaces - `black` uses spaces by default. Need to decide if we adapt or configure.

---

## Discussion Log

See [Issue #29](https://github.com/Anne-dot/aca-translation-assistant/issues/29) for full discussion.
