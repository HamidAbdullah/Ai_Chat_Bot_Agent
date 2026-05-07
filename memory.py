"""
Memory and chat history manager.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List


class ConversationMemory:
    """Stores and retrieves chat sessions and message history."""

    def __init__(self, history_file: str, max_memory_messages: int = 12) -> None:
        self.history_file = history_file
        self.max_memory_messages = max_memory_messages
        self.sessions: Dict[str, Dict[str, Any]] = self._load_history()

    def _load_history(self) -> Dict[str, Dict[str, Any]]:
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return {}

    def _save_history(self) -> None:
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.sessions, f, indent=2, ensure_ascii=False)

    def create_new_chat(self, title: str = "New Chat") -> str:
        chat_id = str(uuid.uuid4())
        self.sessions[chat_id] = {
            "title": title,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
        }
        self._save_history()
        return chat_id

    def get_sessions(self) -> Dict[str, Dict[str, Any]]:
        return self.sessions

    def get_messages(self, chat_id: str) -> List[Dict[str, str]]:
        return self.sessions.get(chat_id, {}).get("messages", [])

    def add_message(self, chat_id: str, role: str, content: str) -> None:
        if chat_id not in self.sessions:
            self.create_new_chat()

        self.sessions[chat_id]["messages"].append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
            }
        )

        if self.sessions[chat_id]["title"] == "New Chat" and role == "user":
            short_title = content.strip()[:40]
            self.sessions[chat_id]["title"] = short_title if short_title else "New Chat"

        self.sessions[chat_id]["updated_at"] = datetime.now().isoformat()
        self._save_history()

    def get_recent_context(self, chat_id: str) -> List[Dict[str, str]]:
        all_msgs = self.get_messages(chat_id)
        recent = all_msgs[-self.max_memory_messages :]
        return [{"role": m["role"], "content": m["content"]} for m in recent]

    def clear_chat(self, chat_id: str) -> None:
        if chat_id in self.sessions:
            self.sessions[chat_id]["messages"] = []
            self.sessions[chat_id]["updated_at"] = datetime.now().isoformat()
            self._save_history()
