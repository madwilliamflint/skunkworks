#!python

class AppLog():
    def __init__(self,configuration):
        self.config = configuration

    def preferred_route(self):
        # This is a little more bottle specific than I'd like.  But something has to know.
        # To abstract this much farther I'd be looking for "virtual void main() = 0;" type crap.

        return '/log/<message>'

    def __call__(self, **messages):
        #TODO: POST/GET processing.
        #TODO:  Fold in the real logging class.
        
        print(messages['message'])
        return(messages['message'])
    
def get_interface(configuration):
    obj = AppLog(configuration)
    return(obj.preferred_route(),obj)


