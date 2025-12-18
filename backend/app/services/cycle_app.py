import httpx
from app.config import get_settings
from typing import Optional


class CycleAppService:
    """Service to interact with the Cycle-App external system."""

    def __init__(self):
        settings = get_settings()
        self.base_url = settings.cycle_app_api_url
        self.api_key = settings.cycle_app_api_key

    async def get_user_profile(self, user_id: str) -> dict:
        """Fetch user profile from Cycle-App."""
        # TODO: Implement actual Cycle-App API call
        # For now, return mock data for testing

        return {
            "user_id": user_id,
            "name": "Test User",
            "goals": ["Build muscle", "Improve endurance"],
            "fitness_level": "intermediate",
            "current_week": 3,
            "workouts_completed": 12,
            "preferences": {
                "workout_days": ["Monday", "Wednesday", "Friday", "Saturday"],
                "preferred_time": "morning"
            },
            "notes": "Mentioned left knee sensitivity - avoid deep squats"
        }

    async def log_feedback(
        self,
        user_id: str,
        feedback: str,
        workout_date: Optional[str] = None,
        difficulty_rating: Optional[int] = None
    ) -> dict:
        """Log workout feedback to Cycle-App."""
        # TODO: Implement actual Cycle-App API call

        return {
            "status": "logged",
            "user_id": user_id,
            "feedback": feedback,
            "workout_date": workout_date,
            "difficulty_rating": difficulty_rating
        }
