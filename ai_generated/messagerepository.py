import json
import os

class MessageRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.messages = []
        if os.path.exists(file_path):
            self.load()

    def add_message(self, message):
        self.messages.append(message)
        self.save()

    def retrieve_messages(self, criteria):
        return [msg for msg in self.messages if all(msg.get(k) == v for k, v in criteria.items())]

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.messages, f, indent=4)

    def load(self):
        with open(self.file_path, 'r') as f:
            self.messages = json.load(f)

# Example usage:
repo = MessageRepository('messages.json')
repo.add_message({'id': 1, 'content': 'Hello, world!', 'author': 'Alice'})
repo.add_message({'id': 2, 'content': 'Goodbye, world!', 'author': 'Bob'})

# Retrieve messages by author
criteria = {'author': 'Alice'}
matching_messages = repo.retrieve_messages(criteria)
print(matching_messages)
