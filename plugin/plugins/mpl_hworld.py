#!python


from plugins.mplbase import MaelstromPluginBase


class MPHelloWorld(MaelstromPluginBase):
    def __init__(self):
        super().__init__()

    def run_me(self):
        print("Hello World!")

    def plugin_info(self):
        return "Info about the plugin which will eventually be in a dictionary."

    def register_hooks(self,whatever_you_register_hooks_into):
        print("Registering hooks for plugin [MPHelloWorld] (NOP)")

    def initialize_install(self,config):
        print("Installing plugin [MPHelloWorld] (NOP).")

