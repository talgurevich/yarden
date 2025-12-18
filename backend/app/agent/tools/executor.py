import json
from app.services.cycle_app import CycleAppService
from app.services.rag import RAGService

# Lazy initialization
_cycle_app = None
_rag = None


def get_cycle_app():
    global _cycle_app
    if _cycle_app is None:
        _cycle_app = CycleAppService()
    return _cycle_app


def get_rag():
    global _rag
    if _rag is None:
        _rag = RAGService()
    return _rag


async def execute_tool(tool_name: str, tool_input: dict, user_id: str) -> str:
    """Execute a tool and return the result as a string."""

    try:
        cycle_app = get_cycle_app()
        rag = get_rag()

        if tool_name == "get_user_profile":
            result = await cycle_app.get_user_profile(tool_input["user_id"])

        elif tool_name == "search_workout_plan":
            result = await rag.search_workout(
                user_id=tool_input["user_id"],
                query=tool_input["query"]
            )

        elif tool_name == "get_exercise_info":
            result = await rag.get_exercise_info(tool_input["exercise_name"])

        elif tool_name == "log_workout_feedback":
            result = await cycle_app.log_feedback(
                user_id=tool_input["user_id"],
                feedback=tool_input["feedback"],
                workout_date=tool_input.get("workout_date"),
                difficulty_rating=tool_input.get("difficulty_rating")
            )

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})
