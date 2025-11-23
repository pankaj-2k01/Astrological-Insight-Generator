from datetime import datetime
from typing import Dict


class ZodiacCalculator:
    """
    Calculates the zodiac sign (sun-sign) from a birth datetime.

    This class is designed so that in future we can extend it to also
    use birth_place and birth_time more deeply (e.g., Vedic/Panchang).
    """

    # Western sun-sign ranges. (month, day)
    ZODIAC_RANGES = [
        ("Capricorn", (12, 22), (12, 31)),
        ("Capricorn", (1, 1), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21)),
    ]

    # Simple metadata for each sign
    ZODIAC_METADATA = {
        "Aries": {"element": "Fire", "ruling_planet": "Mars"},
        "Taurus": {"element": "Earth", "ruling_planet": "Venus"},
        "Gemini": {"element": "Air", "ruling_planet": "Mercury"},
        "Cancer": {"element": "Water", "ruling_planet": "Moon"},
        "Leo": {"element": "Fire", "ruling_planet": "Sun"},
        "Virgo": {"element": "Earth", "ruling_planet": "Mercury"},
        "Libra": {"element": "Air", "ruling_planet": "Venus"},
        "Scorpio": {"element": "Water", "ruling_planet": "Mars"},
        "Sagittarius": {"element": "Fire", "ruling_planet": "Jupiter"},
        "Capricorn": {"element": "Earth", "ruling_planet": "Saturn"},
        "Aquarius": {"element": "Air", "ruling_planet": "Saturn"},
        "Pisces": {"element": "Water", "ruling_planet": "Jupiter"},
    }

    @staticmethod
    def _in_range(
        month: int,
        day: int,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> bool:
        sm, sd = start
        em, ed = end

        if sm == em:
            return month == sm and sd <= day <= ed

        if sm < em:
            if sm < month < em:
                return True
            if month == sm and day >= sd:
                return True
            if month == em and day <= ed:
                return True

        return False

    def get_zodiac_sign(self, birth_datetime: datetime) -> Dict[str, str]:
        """
        Returns a dict with sign, element, and ruling planet:

        {
          "sign": "Leo",
          "element": "Fire",
          "ruling_planet": "Sun"
        }
        """
        month = birth_datetime.month
        day = birth_datetime.day

        sign = "Unknown"
        for s, start, end in self.ZODIAC_RANGES:
            if self._in_range(month, day, start, end):
                sign = s
                break

        meta = self.ZODIAC_METADATA.get(sign, {})
        return {
            "sign": sign,
            "element": meta.get("element"),
            "ruling_planet": meta.get("ruling_planet"),
        }
