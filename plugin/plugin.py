#!python

import os
import glob
import inspect
import importlib
from plugins.mplbase import MaelstromPluginBase

PLUGIN_DIR = 'plugins'

# These three functions knit together into discover_plugins.  I just haven't done the split yet.

def get_plugin_candidates(plugin_dir,module_pattern):
    full_spec = os.path.join(plugin_dir,module_pattern)

    potential_matches = glob.glob(full_spec)

    return potential_matches

def load_file_as_module(filename):
    # Snip the extension off the end.
    module_name = filename[:-3]
            
    module = importlib.import_module(module_name)

    return module

def get_plugins_from_module(module):
    plugins = list()

    for name, obj in inspect.getmembers(module, inspect.isclass):

        # For each gut, if it's a class descended off of MaelstromPluginBase and isn't that class itself...
        if inspect.isclass(obj) and issubclass(obj, MaelstromPluginBase) and obj is not MaelstromPluginBase:
            # Append the module, class name,obj tuple
            plugins.append((module,name,obj))

    return plugins



def discover_plugins(plugin_dir):
    """ This should really be 3 separate functions.  But for the sake of the ./skunkworks/ tech demo it's all in one.
    But the proper breakout should be something like this:
    
    - Given the plugin_dir search for all files matching a filespec. [pass this in as well]
    - given a file... Load it dynamically as a module
    - given a module:  Return a list of all classes it contains that are descended off of a specific class [ pass that in as well ]

    That way it'd all be quite reasonably abstracted and decoupled with 3 required parameters in the envelope:
    - Directory
    - Filespec
    - base class

    Alternatively I could be sold on a single method being required within a plugin that did all the reporting or registration
    of what it provided.

    """
    plugins = []

    # List all the potential files
    for filename in os.listdir(plugin_dir):
        # Filter them out by filename convention
        if filename.endswith('.py') and filename.startswith('mpl_'):
            # Pull the base name off
            module_name = filename[:-3]
            # Just try to load the thing.

            module = importlib.import_module(f'{PLUGIN_DIR}.{module_name}')

            # Given a loaded module, use inspect to iterate through it's guts
            for name, obj in inspect.getmembers(module, inspect.isclass):

                # For each gut, if it's a class descended off of MaelstromPluginBase and isn't that class itself...
                if inspect.isclass(obj) and issubclass(obj, MaelstromPluginBase) and obj is not MaelstromPluginBase:
                    # Append the module, class name,obj tuple
                    plugins.append((module,name,obj))
            #plugins.append(module)
    return plugins

# Returns a list of tuples each containing:

# - Module
# - Class name
# - Class declaration

# Just some goofy sample code to prove that it works.  Those methods would never be called like that and just print or 
# return  strings.  But it proves the point.


plugin_table = dict()
plugin_list = discover_plugins(PLUGIN_DIR)
for a in plugin_list:
    name = a[1]
    print("Building plugin object [{0}]".format(name))
    o = a[2]()
    print(o.plugin_info())
    o.initialize_install(None)
    o.register_hooks(None)
    o.initialize_run()
    o.run_me()

    plugin_table[name] = o

for x in plugin_table:
    print(x)



    