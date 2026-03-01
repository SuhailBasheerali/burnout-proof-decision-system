"""
AI Reflector Module - Absolem's Wisdom Layer
Provides burnout prevention advice using Google Gemini API with fallback strategies.
"""

import os
import json
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)

# Default Absolem wisdom - used as fallback
ABSOLEM_FALLBACK_WISDOM = {
    "advice": "Patience, young learner. The burden you carry is not the decision itself, but your resistance to choosing. Some options demand the soul's surrender—avoid those. Choose what sustains your spirit, not merely your ambition.",
    "action_plan": [
        "Identify which option allows you to rest without guilt",
        "Build buffer time into your chosen path—urgency breeds burnout",
        "Review your choice weekly; adjust when the path no longer feels sustainable"
    ],
    "comparison_insight": "The most sustainable option is rarely the most prestigious. Trust your energy, not the noise.",
    "source": "Absolem's Default Wisdom"
}

# Cache configuration
CACHE_DIR = Path(__file__).parent.parent.parent / ".ai_cache"
CACHE_EXPIRY_HOURS = 24


class AbsolemReflector:
    """AI Reflective advisory layer with Absolem character theme."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the reflector with optional API key.
        Falls back gracefully if API key not provided.
        """
        self.api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY")
        self.gemini_available = False
        self.usage_stats = {"total_calls": 0, "failed_calls": 0, "cached_calls": 0}
        
        if self.api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                self.gemini_available = True
                logger.info("✨ Gemini API initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️  Gemini API initialization failed: {e}. Using fallback wisdom.")
                self.gemini_available = False
        else:
            logger.info("📖 Using Absolem's Default Wisdom (no API configured)")
    
    def _get_cache_key(self, options_summary: str) -> str:
        """Generate cache key from options."""
        return hashlib.md5(options_summary.encode()).hexdigest()
    
    def _load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load cached response if available and not expired."""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    cache_time = datetime.fromisoformat(cached["timestamp"])
                    if datetime.now() - cache_time < timedelta(hours=CACHE_EXPIRY_HOURS):
                        self.usage_stats["cached_calls"] += 1
                        logger.info(f"📚 Cache hit - reusing Absolem's previous wisdom")
                        return cached["response"]
                    else:
                        cache_file.unlink()
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, response: Dict[str, Any]):
        """Save response to cache."""
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file = CACHE_DIR / f"{cache_key}.json"
            with open(cache_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "response": response
                }, f)
        except Exception as e:
            logger.warning(f"Cache write failed: {e}")
    
    def _create_prompt(self, options: list, best_option: str, analysis_data: dict) -> str:
        """Create Absolem-themed prompt."""
        # Handle both dict and Pydantic model inputs
        options_names = []
        for opt in options:
            if hasattr(opt, 'title'):
                # Pydantic model
                options_names.append(opt.title)
            elif isinstance(opt, dict) and 'title' in opt:
                # Dictionary
                options_names.append(opt['title'])
            elif isinstance(opt, dict) and 'name' in opt:
                # Alternative dict format
                options_names.append(opt['name'])
        
        options_str = ", ".join(options_names) if options_names else "unknown options"
        return f"""You are Absolem, a wise guardian from the Caterpillar Kingdom. Your role is to provide 
brief, cryptic yet helpful advice to prevent burnout in academic decisions.

The student has {len(options)} options: {options_str}
The analysis suggests '{best_option}' is strongest.
Key metrics: Growth score {analysis_data.get('growth_score', '?')}, Sustainability: {analysis_data.get('sustainability_score', '?')}

In 2-3 sentences, advise which option prevents burnout best and why. Be cryptic but insightful. 
Keep it short. Focus on SUSTAINABILITY and BURNOUT PREVENTION."""
    
    def get_reflection(self, options: list, comparison_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get Absolem's wisdom on the decision with full mitigation strategy.
        
        Args:
            options: List of decision options with scores
            comparison_result: Backend analysis result
        
        Returns:
            Dictionary with advice, action plan, and comparison insight
        """
        self.usage_stats["total_calls"] += 1
        
        # Generate cache key based on options
        try:
            # Handle both dict and Pydantic models
            options_for_cache = []
            for opt in options:
                if hasattr(opt, 'title') and hasattr(opt, 'growth_criteria'):
                    # Pydantic model
                    options_for_cache.append({
                        "title": opt.title,
                        "growth": sum(c.weight for c in opt.growth_criteria),
                        "sustainability": sum(c.weight for c in opt.sustainability_criteria)
                    })
                elif isinstance(opt, dict):
                    # Dictionary
                    options_for_cache.append({
                        "title": opt.get("title", "Unknown"),
                        "growth": opt.get("growth", 0),
                        "sustainability": opt.get("sustainability", 0)
                    })
            
            options_summary = json.dumps(options_for_cache, sort_keys=True)
        except Exception as cache_err:
            logger.warning(f"Cache key generation error: {cache_err}. Using fallback.")
            options_summary = json.dumps({"error": "cache_key_gen"})
        
        cache_key = self._get_cache_key(options_summary)
        
        # Check cache first
        cached_response = self._load_from_cache(cache_key)
        if cached_response:
            return cached_response
        
        # Determine best option
        # Handle both dict and Pydantic model for comparison_result
        if hasattr(comparison_result, 'recommended_option'):
            # Pydantic model
            best_option = comparison_result.recommended_option
            analysis_data = {
                "growth_score": None,
                "sustainability_score": None
            }
        elif isinstance(comparison_result, dict):
            # Dictionary
            best_option = comparison_result.get("recommended_option", "Unknown")
            analysis_data = {
                "growth_score": comparison_result.get("analysis", {}).get("growth_score"),
                "sustainability_score": comparison_result.get("analysis", {}).get("sustainability_score")
            }
        else:
            best_option = "Unknown"
            analysis_data = {"growth_score": None, "sustainability_score": None}
        
        # Try Gemini API
        if self.gemini_available:
            try:
                prompt = self._create_prompt(options, best_option, analysis_data)
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=200,
                        temperature=0.7,
                    ),
                    safety_settings=[
                        {
                            "category": genai.types.HarmCategory.HARM_CATEGORY_UNSPECIFIED,
                            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
                        }
                    ]
                )
                
                wisdom_text = response.text.strip()
                result = {
                    "advice": wisdom_text,
                    "action_plan": [
                        "Reflect on this wisdom—does it resonate with your energy?",
                        f"If choosing '{best_option}', ensure you have rest periods built in",
                        "Monitor your burnout signals weekly; adjust course if needed"
                    ],
                    "comparison_insight": f"In Absolem's view, '{best_option}' offers the most sustainable path forward.",
                    "source": "Absolem (via Gemini)"
                }
                
                # Cache successful response
                self._save_to_cache(cache_key, result)
                logger.info("✨ Gemini wisdom generated and cached")
                return result
                
            except Exception as e:
                logger.warning(f"❌ Gemini API call failed: {e}. Falling back to default wisdom.")
                self.usage_stats["failed_calls"] += 1
                return ABSOLEM_FALLBACK_WISDOM
        
        # Fallback to default wisdom
        logger.info("📖 Using default Absolem wisdom (API unavailable)")
        return ABSOLEM_FALLBACK_WISDOM
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Return usage statistics for monitoring."""
        return {
            **self.usage_stats,
            "cache_enabled": True,
            "fallback_available": True,
            "timestamp": datetime.now().isoformat()
        }


# Global instance
_reflector_instance: Optional[AbsolemReflector] = None


def get_reflector() -> AbsolemReflector:
    """Singleton pattern for reflector instance."""
    global _reflector_instance
    if _reflector_instance is None:
        _reflector_instance = AbsolemReflector()
    return _reflector_instance


def get_absolem_wisdom(
    options: list,
    comparison_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convenience function to get Absolem's wisdom.
    
    Args:
        options: List of decision options
        comparison_result: Backend analysis result
    
    Returns:
        Dictionary with advice, action plan, and comparison insight
    """
    reflector = get_reflector()
    return reflector.get_reflection(options, comparison_result)
