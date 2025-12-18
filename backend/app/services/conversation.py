from typing import List, Dict

# In-memory storage for POC (replace with MongoDB later)
_conversations: Dict[str, List[Dict]] = {}
_summaries: Dict[str, str] = {}


class ConversationService:
    def __init__(self):
        pass

    async def get_history(self, session_id: str, limit: int = 20) -> List[Dict]:
        """Get conversation history for a session (sliding window)."""
        messages = _conversations.get(session_id, [])
        return messages[-limit:]

    async def save_history(self, session_id: str, messages: List[Dict]):
        """Save conversation history, keeping only recent messages."""
        max_messages = 50
        _conversations[session_id] = messages[-max_messages:]

    async def get_summary(self, session_id: str) -> str:
        """Get conversation summary if it exists."""
        return _summaries.get(session_id, "")

    async def save_summary(self, session_id: str, summary: str):
        """Save a conversation summary."""
        _summaries[session_id] = summary
