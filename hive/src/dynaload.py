#!python3 


#
# From: 
# 
# https://stackoverflow.com/questions/951124/dynamic-loading-of-python-modules 
#
#    def loadModules():
#        res = {}
#        import os
#        # check subfolders
#        lst = os.listdir("services")
#        dir = []
#        for d in lst:
#            s = os.path.abspath("services") + os.sep + d
#            if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
#                dir.append(d)
#        # load the modules
#        for d in dir:
#            res[d] = __import__("services." + d, fromlist = ["*"])
#        return res
#
#    This other one is to instantiate an object by a class defined in one of the modules loaded by the first function:
#
#    def getClassByName(module, className):
#        if not module:
#            if className.startswith("services."):
#                className = className.split("services.")[1]
#            l = className.split(".")
#            m = __services__[l[0]]
#            return getClassByName(m, ".".join(l[1:]))
#        elif "." in className:
#            l = className.split(".")
#            m = getattr(module, l[0])
#            return getClassByName(m, ".".join(l[1:]))
#        else:
#            return getattr(module, className)
#
#    A simple way to use those functions is this:
#
#    mods = loadModules()
#    cls = getClassByName(mods["MyModule"], "submodule.filepy.Class")
#    obj = cls()



# Dynaload

# Attempts to hot load all classes from the 'agents' module.

#import agents

#################################################################################################
# EXPERIMENT 1: 
#################################################################################################
#
# Iterate across the files in the subdirectory and find the python scripts starting with mod_
# 
# Works fine. 
#
#################################################################################################
#import os
#
#import importlib, inspect

#inspect.getmembers(agents)

#for name, cls in inspect.getmembers(agents, inspect.isclass):

#for f in os.listdir('./agents/'):
#    if f[0:4] == 'mod_' and f[-2:] == 'py':
#        print("Module found: [{0}]".format(f))
#################################################################################################



def loadModules():
    # Attempts to load modules underneath the 'directory' directory.
    # Not QUITE what I'm looking for.

#    directory = 'agents'
    directory = '.'
    res = {}
    import os
    # check subfolders
    lst = os.listdir(directory)
    #print(lst)
    dir = []
    for d in lst:
        s = os.path.abspath(directory) + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            print(">>> " + d)
            dir.append(d)
    # load the modules
    for d in dir:
        res[d] = __import__(directory + d, fromlist = ["*"])
    return res

def run_test_2():
    mods = loadModules()

    for mod in mods:
        print("Loaded module [{0}]".format(mod))

    # Just because I know.
    agents = mods['agents']


    import inspect

    print("-------------------")
    for item in inspect.getmembers(agents):
        if inspect.isclass(item):
            print("CLASS: " + str(item))
    #    print("\t" + str(item))
    #print(inspect.getmembers(agents))

    print(agents.AppLog)

##################################################################################################
#
# Test 3:  Tough to articulate.  Starting at the bottom and working my way back up the chain
#
##################################################################################################

from importlib import import_module
import os 

def list_module_files():

    files = list()
    lst = os.listdir('./agents/')
    for item in lst:
        if '__init__' not in item:
            if item[-3:] == '.py':
#                files.append('./agents/' + item)
                files.append(item)
    return files


#for i in list_module_files():
#    print(">>> " + i)

def run_test_3():
    # Perverted from: 
    # https://stackoverflow.com/questions/30604401/how-to-iterate-through-a-list-of-modules-and-call-their-methods-in-python-3
    import imp

    agents = list()

    for file in list_module_files():
        mod = imp.load_source('./agents/',file)
        print("==================================")
        print(mod)
        print("----------------------------------")

#run_test_3()




######################################################################################################
# Test 4
######################################################################################################

def run_test_4():
    import importlib
    import inspect
    importlib.invalidate_caches()

#    foo = importlib.import_module('agents')
#    foo = importlib.import_module('agents',globals(),locals(),[],0)
    foo = __import__('agents',globals(),locals(),[],0)

    tuples = inspect.getmembers(foo)
    for t in tuples:
        if t[0] != '__builtins__':
            print(t)


    print("--------------------------")
    print(inspect.getmembers(foo, inspect.isclass))
        



#run_test_4()







######################################################################################################
# Test 5
#
#  https://www.dev2qa.com/how-to-import-a-python-module-from-a-python-file-full-path/
#
# THIS WORKS!
#
######################################################################################################




def run_test_5():
    # first import importlib.util module.
    import importlib.util
    # get python module spec from the provided python source file. The spec_from_file_location function takes two parameters, the first parameter is the module name, then second parameter is the module file full path. 
    test_spec = importlib.util.spec_from_file_location("foo", "./agents/mod_foo.py")
    #print("test_spec: [{0}]".format(test_spec))
    # pass above test_spec object to module_from_spec function to get custom python module from above module spec.
    test_module = importlib.util.module_from_spec(test_spec)

    # load the module with the spec.
    test_spec.loader.exec_module(test_module)
    # invoke the module variable.
    bar = test_module.h_world()
    print(bar)
    #'jerry'

    # create an instance of a class in the module.
    #test_hello = test_module.TestHello()

    # call the module class's function.
    #test_hello.print_hello_message()
#hello jerry

#run_test_5()


######################################################################################################
# Test 6
######################################################################################################

def source_python_file(internal_name,qualified_filename):
    # Seems 'internal_name' is erroneous, but required for the spec_from... method.
    import importlib.util
    test_spec = importlib.util.spec_from_file_location(internal_name,qualified_filename)
    loaded_module = importlib.util.module_from_spec(test_spec)
    test_spec.loader.exec_module(loaded_module)
    return loaded_module

def run_test_6():
    loaded = source_python_file('foo','./agents/mod_bar.py')

    thingamabob = loaded.get_object('')
    thingamabob.hello_world()

run_test_6()





#import os
#
#import importlib, inspect

#inspect.getmembers(agents)

#for name, cls in inspect.getmembers(agents, inspect.isclass):

#for f in os.listdir('./agents/'):
#    if f[0:4] == 'mod_' and f[-2:] == 'py':
#        print("Module found: [{0}]".format(f))
