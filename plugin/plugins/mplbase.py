#!python

# Uhm... I wasn't fucking ready to get this far.

# This is a sample plug-in for the ../discover_plugins.py script.

# Seeing as how I'm just using this as a tech prototype I just want it to do a couple things:

# First, all plugins should correspond to an interface, meaning...
#   the parent script shouldn't just nakedly import every .py in this directory. (Indeed, some 
#       plugins might have their own sub-modules, etc.)
#   Filename convention and guaranteed interface testing should be prerequisites for a plugin to be
#       accepted.  If the filename convention is followed but the interface is not, report an error.
#
# So let's come up with an interface that does the basic version of what I'm looking for:
#
# - Describe yourself and your contained hooks
# - Given a dispatch table, register yourself (that's dangerous.  But for now I'll deal with it.)
#
# So that's two methods (for now):
#
# - plugin_info
#
# - register_hooks 
#
#  And maybe...
#  
# - initialize_install:  Given a root directory, create any directories or baseline stuff you might need for "install"
#
# - initialize_run: Is the plug-in going to need to run some initialization on load?
#

# Yeah, that's an ABC class interface in a "plugin_template" class that will exist in this self-same plugins directory.
# When the "parent" script detects the plugin it really needs the class name and nothing else.  It can perform an "isa"
# test for safety.  Then just put it in the damned hopper with the other plug-ins.
#
# Yep.  Like it.

# Actually....I'll make that THIS file. :-)

class MaelstromPluginBase:
    def __init__(self):
        pass

    def plugin_info(self):
        raise NotImplementedError

    def register_hooks(self,whatever_you_register_hooks_into):
        raise NotImplementedError

    def initialize_install(self,config):
        raise NotImplementedError

    def initialize_run(self):
      # Not sure I need this at all.  I know I know, YAGNI.  But.... "I feel like I should put it here"
        raise NotImplementedError


