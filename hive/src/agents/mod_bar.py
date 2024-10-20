#!python


class SomeClass():
    def __init__(self,config):
        self.config =  config

    def hello_world(self):
        print("Hello World!")

def get_object(config):
    obj = SomeClass(config)
    return obj