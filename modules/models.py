from pydantic import BaseModel, Field
from typing import Optional


class BirthDetails(BaseModel):
    """
    Input model for birth details and language preference.

    Kept as strings for date/time to allow custom validation/formatting
    and to keep API/CLI behavior consistent.
    """
    name: str = Field(..., description="User's name")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    birth_time: str = Field(..., description="Birth time in HH:MM format")
    birth_place: str = Field(..., description="Birth location")
    language: Optional[str] = Field(
        "en",
        description="Output language code (e.g., 'en' for English, 'hi' for Hindi)"
    )


class InsightResponse(BaseModel):
    """
    Output model for the astrological insight.
    """
    zodiac: str
    insight: str
    language: str
    element: Optional[str] = None
    ruling_planet: Optional[str] = None
