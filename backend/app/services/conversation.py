from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
from typing import List, Dict


class ConversationService:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client.yarden
        self.collection = self.db.conversations

    async def get_history(self, session_id: str, limit: int = 20) -> List[Dict]:
        """Get conversation history for a session (sliding window)."""
        doc = await self.collection.find_one({"session_id": session_id})
        if doc and "messages" in doc:
            # Return last N messages (sliding window)
            return doc["messages"][-limit:]
        return []

    async def save_history(self, session_id: str, messages: List[Dict]):
        """Save conversation history, keeping only recent messages."""
        max_messages = 50  # Keep last 50 messages

        await self.collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "messages": messages[-max_messages:],
                    "message_count": len(messages)
                }
            },
            upsert=True
        )

    async def get_summary(self, session_id: str) -> str:
        """Get conversation summary if it exists."""
        doc = await self.collection.find_one({"session_id": session_id})
        return doc.get("summary", "") if doc else ""

    async def save_summary(self, session_id: str, summary: str):
        """Save a conversation summary."""
        await self.collection.update_one(
            {"session_id": session_id},
            {"$set": {"summary": summary}},
            upsert=True
        )
