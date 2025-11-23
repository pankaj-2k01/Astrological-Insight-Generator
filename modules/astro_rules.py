from typing import Dict, Any


class AstrologicalRules:
    """
    Provides dummy astrological rules / daily context for each zodiac sign.
    """

    ZODIAC_RULES: Dict[str, Dict[str, Any]] = {
        "Aries": {
            "traits": ["bold", "energetic", "decisive"],
            "today_theme": "taking initiative and starting fresh tasks",
        },
        "Taurus": {
            "traits": ["grounded", "patient", "reliable"],
            "today_theme": "stability, comfort, and steady progress",
        },
        "Gemini": {
            "traits": ["curious", "adaptable", "communicative"],
            "today_theme": "conversations, learning, and quick thinking",
        },
        "Cancer": {
            "traits": ["empathetic", "intuitive", "protective"],
            "today_theme": "emotional connection and home matters",
        },
        "Leo": {
            "traits": ["confident", "warm", "charismatic"],
            "today_theme": "leadership, visibility, and self-expression",
        },
        "Virgo": {
            "traits": ["detail-oriented", "practical", "helpful"],
            "today_theme": "organization, planning, and service",
        },
        "Libra": {
            "traits": ["diplomatic", "graceful", "fair-minded"],
            "today_theme": "balance, relationships, and aesthetics",
        },
        "Scorpio": {
            "traits": ["intense", "focused", "transformative"],
            "today_theme": "deep focus and emotional transformation",
        },
        "Sagittarius": {
            "traits": ["optimistic", "adventurous", "philosophical"],
            "today_theme": "exploration, learning, and big-picture thinking",
        },
        "Capricorn": {
            "traits": ["disciplined", "ambitious", "responsible"],
            "today_theme": "long-term goals and structured effort",
        },
        "Aquarius": {
            "traits": ["innovative", "independent", "humanitarian"],
            "today_theme": "original ideas and community focus",
        },
        "Pisces": {
            "traits": ["compassionate", "imaginative", "sensitive"],
            "today_theme": "intuition, creativity, and emotional depth",
        },
    }

    DEFAULT_RULE = {
        "traits": ["balanced", "thoughtful"],
        "today_theme": "staying present and calm",
    }

    def get_daily_context(self, zodiac_sign: str) -> Dict[str, Any]:
        """
        Returns daily context for a given zodiac sign:
        {
          "traits": [...],
          "today_theme": "..."
        }
        """
        return self.ZODIAC_RULES.get(zodiac_sign, self.DEFAULT_RULE)
