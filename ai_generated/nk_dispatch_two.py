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

    def call_method(self, method_name, arg1, arg2):
        """
        Call the method looked up in the dispatch table.
        Args:
            method_name (str): The name of the method to call.
            arg1: First positional argument to pass to the method.
            arg2: Second positional argument to pass to the method.
        Returns:
            The result of the method call.
        """
        method = self.dispatch_table.get(method_name)
        if method:
            return method(arg1, arg2)
        else:
            raise ValueError(f"Method '{method_name}' not found in the dispatch table.")

# Example usage:
class MathOperations:
    def add_numbers(self, a, b):
        return a + b

    def multiply_numbers(self, a, b):
        return a * b

math_ops = MathOperations()
dispatcher = MethodDispatcher()
dispatcher.register_method("add", math_ops.add_numbers)
dispatcher.register_method("multiply", math_ops.multiply_numbers)

result_add = dispatcher.call_method("add", 3, 4)
result_multiply = dispatcher.call_method("multiply", 3, 4)

print(f"Addition result: {result_add}")  # Output: Addition result: 7
print(f"Multiplication result: {result_multiply}")  # Output: Multiplication result: 12
