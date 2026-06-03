import logging
from typing import Any, Dict

from app.schemas import ReflectionRequest, ReflectionResponse

logger = logging.getLogger(__name__)


def create_reflection(request: ReflectionRequest) -> ReflectionResponse:
    try:
        from app.engine.ai_reflector import get_absolem_wisdom

        # Get Absolem's wisdom using reflection engine
        wisdom = get_absolem_wisdom(
            options=request.options,
            comparison_result=request.comparison_result
        )

        return ReflectionResponse(
            action_plan=wisdom.get("action_plan", []),
            philosophical_advice=wisdom.get("philosophical_advice", "Choose what sustains your spirit."),
            source=wisdom.get("source", "Unknown")
        )

    except Exception as e:
        from app.engine.ai_reflector import ABSOLEM_FALLBACK_WISDOM

        # Fallback to default wisdom on any error
        logger.error(f"Reflection error: {e}. Using fallback wisdom.")

        fallback = ABSOLEM_FALLBACK_WISDOM
        return ReflectionResponse(
            action_plan=fallback.get("action_plan", []),
            philosophical_advice=fallback.get("philosophical_advice", "Choose what sustains your spirit."),
            source=fallback.get("source", "Unknown")
        )


def get_ai_reflection_stats() -> Dict[str, Any]:
    from app.engine.ai_reflector import get_reflector

    reflector = get_reflector()

    return {
        "ai_reflection_stats": reflector.get_usage_stats(),
        "message": "Monitor these stats to ensure you stay within Gemini's free tier (1500 requests/day)"
    }


def get_daily_rate_limits() -> Dict[str, Any]:
    from app.engine.ai_reflector import get_reflector

    reflector = get_reflector()
    return reflector.get_daily_limits_info()
