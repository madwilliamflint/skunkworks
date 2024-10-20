
#  I took the generated example ocde in nk_dispatch_two.py and fiddled with it 
# here so that the called methods are in the object that contains the dispatcher
# It's shit code. But it's the interim architecture of the dispatcher in the
# Maelstrom server, so I wanted a Hello World model so I could figure out what 
# the cinnamon toast fuck was wrong with my implementation.

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
        
    def add_numbers(self, a, b):
        return a + b

    def multiply_numbers(self, a, b):
        return a * b

    def setup(self):
        self.register_method("add",      self.add_numbers)
        self.register_method("multiply", self.multiply_numbers)

    def run(self):

        result_add =      self.call_method("add", 3, 4)
        result_multiply = self.call_method("multiply", 3, 4)

        print(f"Addition result: {result_add}")  # Output: Addition result: 7
        print(f"Multiplication result: {result_multiply}")  # Output: Multiplication result: 12



if __name__ == '__main__':
    app = MethodDispatcher()
    app.setup()
    app.run()