import json
import os
import re
from langchain_core.messages import HumanMessage, AIMessage, messages_from_dict, message_to_dict

MEMORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory")


class Memory:
    def __init__(self, directory=MEMORY_DIR):
        self.directory = os.path.normpath(directory)

    def _path(self, user_name):
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", user_name)
        return os.path.join(self.directory, f"{safe_name}.json")

    def load(self, user_name):
        path = self._path(user_name)
        if not os.path.isfile(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return messages_from_dict(json.load(f))
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            print(f"Could not read saved memory ({exc}). Starting fresh.")
            return []

    def save(self, user_name, history):
        os.makedirs(self.directory, exist_ok=True)
        with open(self._path(user_name), "w", encoding="utf-8") as f:
            json.dump([message_to_dict(m) for m in history], f, ensure_ascii=False, indent=2)