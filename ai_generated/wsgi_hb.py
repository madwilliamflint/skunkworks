#!/usr/bin/python

import sys
import datetime 
import threading
import requests
import time

import bottle

def log(message):
    print("[{0}]:\t{1}".format(threading.get_ident(),message))

def log_dict(d):
    for k in d:
        log("{0}: {1}".format(k,d[k]))

def log_http_response(response):
    log("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    log("Status: [{0}]".format(response.status_code))
    log_dict(response.headers)
    log("")
    log(response.text)
    log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

def run_trigger(occasion):
    log("run_trigger()")
    result = "This is a heartbeat response.  The occasion variable came in saying [{0}].".format(occasion)
    return result

def make_request(url,delay):
    while True:
        try:
            response = requests.get(url)
            log_http_response(response)
        except requests.exceptions.RequestException as e:
            log(f"Request failed: {e}")
        time.sleep(delay)

def start_thread(url,delay):
    thread = threading.Thread(target=make_request, args=[url,delay])

    thread.daemon = True  # This makes sure the thread will exit when the main program exits
    thread.start()

@bottle.route('/trigger/<occasion>')
@bottle.route('/trigger/')
def route_trigger(occasion='tick'):
    result = run_trigger(occasion)

    # Testing parallelism and blocking by creating an artifical delay in processing time.
    #time.sleep(10)
    
    return "Thanks!  [{0}].".format(result)

# Empty string works as root route?
@bottle.route("/")
def route_root():
    now=datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    #print("Formatted Timestamp:", timestamp_str)    
    return "Simple response off the root url." + timestamp_str

@bottle.error()
def route_generic_error(error):
    # Log the unresolved route attempt
    whups = f"Error {bottle.error.status_code}: {bottle.error.body} at {bottle.request.url} from {bottle.request.remote_addr}"
    log(whups)
    return whups

if __name__ == '__main__':

    ip = "127.0.0.1"
    port_num = 1234
    heartbeat_interval = 1

    url = "http://{0}:{1}/trigger/".format(ip,port_num)

    start_thread(url,heartbeat_interval)

    log("running bottle's run method...")       
    bottle.run(host="0.0.0.0",port=port_num,reloader=True)
