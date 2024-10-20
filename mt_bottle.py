from bottle import Bottle, run, route
import threading
import code

app = Bottle()

# This is an edit that exists for absolutely no reason at all other than
# to test git -> github.  Have fun.


@route('/hello/<name>')
def hello(name):
    return f"Hello {name}!"

def start_server():
    run(app, host='localhost', port=8080)

def interactive_shell():
    # Start an interactive shell
    code.interact(local=locals())

if __name__ == "__main__":
    # Start the Bottle server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    print("Bottle server running on http://localhost:8080")
    print("Type 'exit()' to quit the interactive shell.")

    # Start the interactive shell
    interactive_shell()
