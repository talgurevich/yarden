TOOLS = [
    {
        "name": "get_user_profile",
        "description": "Get the user's profile including their fitness goals, stats, preferences, and history summary.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID"
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "search_workout_plan",
        "description": "Search the user's workout plan for specific information. Use this to find exercises, schedules, or any workout-related details.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID"
                },
                "query": {
                    "type": "string",
                    "description": "What to search for (e.g., 'today's workout', 'chest exercises', 'week 2 plan')"
                }
            },
            "required": ["user_id", "query"]
        }
    },
    {
        "name": "get_exercise_info",
        "description": "Get detailed information about a specific exercise including form tips, common mistakes, and alternatives.",
        "input_schema": {
            "type": "object",
            "properties": {
                "exercise_name": {
                    "type": "string",
                    "description": "Name of the exercise"
                }
            },
            "required": ["exercise_name"]
        }
    },
    {
        "name": "log_workout_feedback",
        "description": "Log feedback about a completed workout including how it went, difficulty level, and any notes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID"
                },
                "workout_date": {
                    "type": "string",
                    "description": "Date of the workout (YYYY-MM-DD)"
                },
                "feedback": {
                    "type": "string",
                    "description": "User's feedback about the workout"
                },
                "difficulty_rating": {
                    "type": "integer",
                    "description": "Difficulty rating 1-10"
                }
            },
            "required": ["user_id", "feedback"]
        }
    }
]
