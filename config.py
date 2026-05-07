"""
Central configuration for the AI assistant.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str = "Kivyx AI Agent"
    model_name: str = "llama-3.3-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    max_memory_messages: int = 12
    history_file: str = "chat_history.json"
    temperature: float = 0.3


settings = Settings()
