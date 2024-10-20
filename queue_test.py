class StringQueueDictionary:
    def __init__(self):
        self.queue_dict = {}

    def push(self, queue_name, item):
        if queue_name not in self.queue_dict:
            self.queue_dict[queue_name] = []
        self.queue_dict[queue_name].append(item)

    def pop(self, queue_name):
        if queue_name in self.queue_dict and self.queue_dict[queue_name]:
            return self.queue_dict[queue_name].pop(0)
        else:
            return None  # Queue is empty or doesn't exist

# Example usage:
queue_manager = StringQueueDictionary()
queue_manager.push("my_queue", 42)
queue_manager.push("my_queue", "hello")
print(queue_manager.pop("my_queue"))  # Output: 42
print(queue_manager.pop("my_queue"))  # Output: "hello"
print(queue_manager.pop("nonexistent_queue"))  # Output: None
