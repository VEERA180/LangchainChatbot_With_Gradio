import uuid
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from Memory import Memory


class UserSession:
    def __init__(self, user_name, memory=None):
        self.user_name = user_name
        self.memory = memory or Memory()
        self.session_id = str(uuid.uuid4())
        self.started_at = datetime.now()
        self.history = self.memory.load(user_name)

    def add_user_message(self, text):
        self.history.append(HumanMessage(content=text))

    def add_ai_message(self, text):
        self.history.append(AIMessage(content=text))
        self.memory.save(self.user_name, self.history)

    def discard_last_message(self):
        if self.history:
            self.history.pop()

    def recent_history(self, limit=20):
        recent = self.history[-limit:]
        # Start on a user message so the model never sees a reply without its question.
        while recent and not isinstance(recent[0], HumanMessage):
            recent = recent[1:]
        return recent 