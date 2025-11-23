# Astrological Insight Generator

The **Astrological Insight Generator** is a small but extensible service that takes a user's birth details and returns a **personalized daily astrological insight**.

It’s designed to demonstrate:

- Clean, modular architecture (class-based).
- Zodiac inference from birth date.
- A simplified astrological rule base per zodiac.
- A **pseudo-LLM layer** with prompt + embedding stubs.
- Optional Hindi output via a translation stub.
- Simple per-user caching to simulate personalization.
- Both **REST API** (FastAPI) and **CLI** interface.

---

##  Project Structure

```text
astrological-insight-generator/
├── main.py                # FastAPI REST API entrypoint
├── cli.py                 # CLI interface for local use
├── requirements.txt
├── README.md
├── DESIGN_WRITEUP.md
└── modules/
    ├── __init__.py
    ├── models.py          # Pydantic models for request/response
    ├── zodiac_calculator.py  # ZodiacCalculator class
    ├── astro_rules.py        # AstrologicalRules class (dummy rule base)
    ├── llm_generator.py      # LLMGenerator class (prompt + pseudo-LLM)
    └── cache_manager.py      # CacheManager class (in-memory TTL cache)
