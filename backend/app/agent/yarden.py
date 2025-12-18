import anthropic
from app.config import get_settings
from app.agent.personality import YARDEN_SYSTEM_PROMPT
from app.agent.tools import TOOLS, execute_tool
from app.services.conversation import ConversationService


class YardenAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.conversation_service = ConversationService()
        self.model = "claude-sonnet-4-20250514"

    async def chat(self, user_id: str, message: str, session_id: str) -> str:
        # Load conversation history
        history = await self.conversation_service.get_history(session_id)

        # Add user message to history
        history.append({"role": "user", "content": message})

        # Build messages for Claude
        messages = self._build_messages(history)

        # Store user_id for tool calls
        self.current_user_id = user_id

        # Agent loop
        response = await self._run_agent_loop(user_id, messages)

        # Save conversation
        history.append({"role": "assistant", "content": response})
        await self.conversation_service.save_history(session_id, history)

        return response

    def _build_messages(self, history: list) -> list:
        """Build message list for Claude API."""
        return history

    async def _run_agent_loop(self, user_id: str, messages: list) -> str:
        """Run the agent loop, handling tool calls."""
        # Build system prompt with user context
        system_prompt = f"""{YARDEN_SYSTEM_PROMPT}

## Current User
You are talking to user_id: {user_id}
When using tools, always use this user_id. Do not ask the user for their ID.
"""
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                tools=TOOLS,
                messages=messages
            )

            # Check if we need to handle tool calls
            if response.stop_reason == "tool_use":
                # Process tool calls
                tool_results = []
                assistant_content = []

                for block in response.content:
                    if block.type == "tool_use":
                        assistant_content.append({
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input
                        })
                        result = await execute_tool(
                            tool_name=block.name,
                            tool_input=block.input,
                            user_id=user_id
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                    elif block.type == "text":
                        assistant_content.append({
                            "type": "text",
                            "text": block.text
                        })

                # Add assistant response and tool results to messages
                messages.append({"role": "assistant", "content": assistant_content})
                messages.append({"role": "user", "content": tool_results})
            else:
                # No more tool calls, extract text response
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text
                return ""
