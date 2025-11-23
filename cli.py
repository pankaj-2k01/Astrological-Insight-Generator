import argparse
from datetime import datetime

from modules.zodiac_calculator import ZodiacCalculator
from modules.astro_rules import AstrologicalRules
from modules.llm_generator import LLMGenerator
from modules.cache_manager import CacheManager
from modules.models import BirthDetails, InsightResponse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Astrological Insight Generator (CLI)"
    )
    parser.add_argument("--name", required=True, help="User's name")
    parser.add_argument("--birth_date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--birth_time", required=True, help="HH:MM")
    parser.add_argument("--birth_place", required=True, help="Birth location")
    parser.add_argument(
        "--language",
        default="en",
        choices=["en", "hi"],
        help="Output language (en/hi)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Create BirthDetails model (reusing same schema as API)
    details = BirthDetails(
        name=args.name,
        birth_date=args.birth_date,
        birth_time=args.birth_time,
        birth_place=args.birth_place,
        language=args.language,
    )

    # Initialize modules (separate from API process)
    zodiac_calc = ZodiacCalculator()
    astro_rules = AstrologicalRules()
    llm_gen = LLMGenerator()
    cache_mgr = CacheManager()

    # Validate and parse datetime
    try:
        birth_datetime = datetime.strptime(
            f"{details.birth_date} {details.birth_time}",
            "%Y-%m-%d %H:%M",
        )
    except ValueError:
        raise SystemExit(
            "Invalid date/time format. Use YYYY-MM-DD for date and HH:MM for time"
        )

    language = details.language or "en"
    cache_key = f"{details.name.lower()}_{details.birth_date}_{language}"
    cached_result = cache_mgr.get(cache_key)

    if cached_result:
        resp = InsightResponse(**cached_result)
    else:
        zodiac_info = zodiac_calc.get_zodiac_sign(birth_datetime)
        daily_context = astro_rules.get_daily_context(zodiac_info["sign"])
        insight_text = llm_gen.generate_insight(
            name=details.name,
            zodiac_info=zodiac_info,
            daily_context=daily_context,
            language=language,
        )

        resp = InsightResponse(
            zodiac=zodiac_info["sign"],
            insight=insight_text,
            language=language,
            element=zodiac_info.get("element"),
            ruling_planet=zodiac_info.get("ruling_planet"),
        )

        cache_mgr.set(cache_key, resp.dict(), ttl=86400)

    # Print nicely
    print(f"Zodiac        : {resp.zodiac}")
    if resp.element:
        print(f"Element       : {resp.element}")
    if resp.ruling_planet:
        print(f"Ruling Planet : {resp.ruling_planet}")
    print(f"Language      : {resp.language}")
    print("Insight       :")
    print(resp.insight)


if __name__ == "__main__":
    main()
