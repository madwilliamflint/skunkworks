class MethodDispatcher:
    def __init__(self):
        self.dispatch_table = {}

    def register_method(self, method_name, method):
        """
        Register a method in the dispatch table.
        Args:
            method_name (str): The name of the method.
            method (callable): The method to be registered.
        """
        self.dispatch_table[method_name] = method

    def call_method(self, method_name, *args, **kwargs):
        """
        Call the method looked up in the dispatch table.
        Args:
            method_name (str): The name of the method to call.
            *args: Positional arguments to pass to the method.
            **kwargs: Keyword arguments to pass to the method.
        Returns:
            The result of the method call.
        """
        method = self.dispatch_table.get(method_name)
        if method:
            return method(*args, **kwargs)
        else:
            raise ValueError(f"Method '{method_name}' not found in the dispatch table.")

# Example usage:
def greet(name):
    return f"Hello, {name}!"

dispatcher = MethodDispatcher()
dispatcher.register_method("greet", greet)

result = dispatcher.call_method("greet", "Alice")
print(result)  # Output: "Hello, Alice!"
