from collections import deque

class ContextManager:
    def __init__(self, max_messages=10):
        self.contexts = {}
        self.max_messages = max_messages

    def get(self, user_id):
        return self.contexts.get(user_id, deque())

    def add(self, user_id, role, content):
        ctx = self.contexts.setdefault(user_id, deque(maxlen=self.max_messages))
        ctx.append({"role": role, "content": content})

    def get_messages(self, user_id):
        return list(self.contexts.get(user_id, deque()))
