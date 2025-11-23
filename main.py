from datetime import datetime
from fastapi import FastAPI, HTTPException
import uvicorn

from modules.zodiac_calculator import ZodiacCalculator
from modules.astro_rules import AstrologicalRules
from modules.llm_generator import LLMGenerator
from modules.cache_manager import CacheManager
from modules.models import BirthDetails, InsightResponse

app = FastAPI(
    title="Astrological Insight Generator",
    version="1.0.0",
    description="Takes birth details and returns a personalized daily astrological insight.",
)

# Initialize modules (singletons for this process)
zodiac_calc = ZodiacCalculator()
astro_rules = AstrologicalRules()
llm_gen = LLMGenerator()
cache_mgr = CacheManager()


@app.get("/")
async def root():
    return {
        "message": "Astrological Insight Generator API",
        "endpoints": {
            "/predict": "POST - Get personalized astrological insight",
            "/health": "GET - Health check",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/predict", response_model=InsightResponse)
async def get_prediction(details: BirthDetails):
    """
    Generate personalized astrological insight based on birth details.

    Expects:
    {
      "name": "Ritika",
      "birth_date": "1995-08-20",
      "birth_time": "14:30",
      "birth_place": "Jaipur, India",
      "language": "en"
    }
    """
    try:
        # Validate and parse datetime
        try:
            birth_datetime = datetime.strptime(
                f"{details.birth_date} {details.birth_time}",
                "%Y-%m-%d %H:%M",
            )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date/time format. Use YYYY-MM-DD for date and HH:MM for time",
            )

        language = details.language or "en"

        # Build a cache key that is user + date + language aware.
        # (You could also include today's date if you want per-day caching.)
        cache_key = f"{details.name.lower()}_{details.birth_date}_{language}"
        cached_result = cache_mgr.get(cache_key)
        if cached_result:
            return cached_result

        # Calculate zodiac sign + metadata
        zodiac_info = zodiac_calc.get_zodiac_sign(birth_datetime)

        # Get daily astrological context for that sign
        daily_context = astro_rules.get_daily_context(zodiac_info["sign"])

        # Generate personalized insight using LLM stub
        insight_text = llm_gen.generate_insight(
            name=details.name,
            zodiac_info=zodiac_info,
            daily_context=daily_context,
            language=language,
        )

        # Prepare response model
        response = InsightResponse(
            zodiac=zodiac_info["sign"],
            insight=insight_text,
            language=language,
            element=zodiac_info.get("element"),
            ruling_planet=zodiac_info.get("ruling_planet"),
        )

        # Cache for 24 hours (86400 seconds)
        cache_mgr.set(cache_key, response.dict(), ttl=86400)

        return response

    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating insight: {str(e)}",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
