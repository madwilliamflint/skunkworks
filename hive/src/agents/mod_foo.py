#!python

from bottle import route, template


class AppLog():
    instance = None
    def __init__(self,configuration):
        self.config = configuration
        instance = self


instance = None
def index(message):
    print(message)
    return(message)



def get_interface(configuration):
    if instance is None:
        instance = AppLog(configuration)

    return ('/app_log/<message>',instance)


def h_world():
    print("Hello!")
    return "World!"