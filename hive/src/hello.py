#!python

#from bottle import route, run, template
import bottle 
#from bottle import route, run, template

#import agents.log

def source_python_file(internal_name,qualified_filename):
    # Seems 'internal_name' is erroneous for ourpurposes, but required for the spec_from... method.
    # I don't like importing shit in the function. But...meh  I'll move this to dynaload.py in a sec.  
    # After I'm done dicking around with it.  So...half past never.
    import importlib.util
    test_spec = importlib.util.spec_from_file_location(internal_name,qualified_filename)
    loaded_module = importlib.util.module_from_spec(test_spec)
    test_spec.loader.exec_module(loaded_module)
    return loaded_module

def run_test_6():
    loaded = source_python_file('foo','./agents/mod_bar.py')

    thingamabob = loaded.get_object('')
    thingamabob.hello_world()

def add_route(route_name,handler):
    print(">> Adding route [{0}]".format(route_name))
    bottle.route(route_name,callback=handler)




def load_agent(agent_filename):
    """
    Takes the name of the agent python script.
    """
    loaded = source_python_file('log_mod',agent_filename)
    (route_name,handler) = loaded.get_interface('config_goes_here')
    add_route(route_name,handler)



#route('/log/<message>',callback=agents.log.index)

#@route('/hello/<name>')
#def index(name):
#    return template('<b>Hello {{name}}</b>!',name=name)

load_agent('./agents/mod_log.py')

bottle.run(host="0.0.0.0", port=8080,debug=True,reloader=True)

