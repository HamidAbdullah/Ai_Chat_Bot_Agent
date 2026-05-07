"""
AI orchestration layer with tool-calling and Groq compatibility.
"""

import json
from typing import Any, Dict, List

import httpx
from openai import OpenAI

from config import settings
from tools import calculate, get_current_time


class AssistantBrain:
    """Main assistant engine with OpenAI-compatible tool usage."""

    def __init__(self) -> None:
        if not settings.groq_api_key:
            raise ValueError("Missing GROQ_API_KEY. Please set it in .env")
        if not settings.groq_api_key.startswith("gsk_"):
            raise ValueError(
                "Invalid GROQ_API_KEY format. Expected a Groq key starting with 'gsk_'."
            )

        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
        )
        self.client_no_proxy = OpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
            http_client=httpx.Client(trust_env=False, timeout=30.0),
        )

        self.tools_schema: List[Dict[str, Any]] = [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Perform arithmetic calculations from expressions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Math expression, e.g. '10*5+2'",
                            }
                        },
                        "required": ["expression"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "current_time",
                    "description": "Get current local date and time.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
        ]

        self.system_prompt = (
            "You are Kivyx AI Agent, a smart and friendly AI assistant.\n"
            "Rules:\n"
            "- Be concise but helpful.\n"
            "- Use tools when needed for exact calculations or time.\n"
            "- If user asks normal questions, answer naturally.\n"
            "- Remember recent conversation context.\n"
        )

    def _run_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute the requested tool safely."""
        try:
            if tool_name == "calculator":
                return calculate(arguments.get("expression", ""))
            if tool_name == "current_time":
                return get_current_time()
            return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Tool execution error: {e}"

    def respond(self, conversation_context: List[Dict[str, str]], user_input: str) -> str:
        """Generate final assistant response with optional tool calls."""
        messages: List[Dict[str, Any]] = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_context)
        messages.append({"role": "user", "content": user_input})

        try:
            return self._respond_with_client(self.client, messages)
        except Exception as first_error:
            # Always retry once without proxy env settings.
            try:
                return self._respond_with_client(self.client_no_proxy, messages)
            except Exception as second_error:
                first_text = str(first_error) or first_error.__class__.__name__
                second_text = str(second_error) or second_error.__class__.__name__
                return (
                    "AI service error: Connection failed in both network paths. "
                    f"Default path -> {first_text}. "
                    f"No-proxy path -> {second_text}."
                )

    def _respond_with_client(self, client: OpenAI, messages: List[Dict[str, Any]]) -> str:
        """Run one full model pass with optional tool-calling."""
        first = client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            tools=self.tools_schema,
            tool_choice="auto",
            temperature=settings.temperature,
        )

        msg = first.choices[0].message

        if msg.tool_calls:
            messages.append(msg.model_dump(exclude_none=True))

            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments or "{}")
                tool_result = self._run_tool(tool_name, tool_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": tool_result,
                    }
                )

            second = client.chat.completions.create(
                model=settings.model_name,
                messages=messages,
                temperature=settings.temperature,
            )
            return second.choices[0].message.content or "I could not generate a response."

        return msg.content or "I could not generate a response."
