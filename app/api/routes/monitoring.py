from fastapi import APIRouter

from app.services.reflection_service import (
    get_ai_reflection_stats,
    get_daily_rate_limits,
)

router = APIRouter()


@router.get("/stats")
def get_stats():
    """
    Get usage statistics for the AI reflection layer.
    Useful for monitoring API usage and ensuring we stay within free tier limits.
    """
    return get_ai_reflection_stats()


@router.get("/api/rate-limits")
def get_rate_limits():
    """
    Get daily API call rate limit information.

    RATE LIMIT POLICY:
    - Max calls per day: 50 (recommended for smooth operation)
    - Reason: Balances free API tier usage with user experience
    - Caching: Reuses responses for 24 hours (doesn't count against limit)
    - Reset: Daily at 00:00 UTC

    Returns:
        {
            "max_calls_per_day": 50,
            "calls_used_today": 3,
            "calls_remaining": 47,
            "percentage_used": 6,
            "reset_time": "2026-03-02T00:00:00Z",
            "status": "OK | WARNING (<=5 left) | EXCEEDED",
            "gemini_available": boolean
        }

    Recommendations:
    - Green (OK): No action needed
    - Yellow (WARNING): Approaching limit, encourage caching/reusing decisions
    - Red (EXCEEDED): Use fallback wisdom until tomorrow's reset
    """
    return get_daily_rate_limits()
