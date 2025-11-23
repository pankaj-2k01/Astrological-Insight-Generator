
---

### `DESIGN_WRITEUP.md`

```markdown
# DESIGN WRITEUP – Astrological Insight Generator

This document explains the **architecture**, **data flow**, and **design decisions** behind the Astrological Insight Generator.

The focus is on:

- Clear modularization.
- Extensibility for real LLMs, Panchang data, and RAG.
- Meeting the assignment expectations around ML logic and personalization.

---

## 1. High-Level Flow

### 1.1 Overview

The system supports both **REST API** (via FastAPI) and a **CLI interface**.  
In both cases, the core flow is:

1. Accept **birth details** and **language**.
2. Parse/validate date and time.
3. Infer the **zodiac sign**.
4. Look up **astrological rules** for that sign (traits, daily theme).
5. Check a **cache** to see if an insight is already generated for this user/date/language.
6. Build a **prompt** and (stub) embeddings for an LLM.
7. Generate an **insight** using a pseudo-LLM.
8. Translate to Hindi if requested (stub).
9. Return a structured **InsightResponse**.

---

## 2. Modules & Responsibilities

### 2.1 `ZodiacCalculator` (`modules/zodiac_calculator.py`)

**Responsibility:** Determine the user's zodiac sign and metadata.

- Uses static Western sun-sign date ranges (Aries…Pisces).
- Input: `datetime` (birth_datetime).
- Output: `dict`:

  ```python
  {
      "sign": "Leo",
      "element": "Fire",
      "ruling_planet": "Sun"
  }
