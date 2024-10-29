import requests
import logging
import json
import datetime
import socket
from requests.exceptions import RequestException, Timeout, ConnectionError

global_timeout=5
global_default_port = 80

# Initialize logging
logging.basicConfig(filename='server_responses.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load servers from JSON file
with open('servers.json', 'r') as f:
    servers = json.load(f)

def ip_reachable(host,timeout=global_timeout):
    try:
        port = global_default_port
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host,port))
        sock.close()
        return True
    except ConnectionRefusedError:
        print("Connection Refused to [{0}]:{1}".format(host,port))
        return True
    except TimeoutError:
        print("Timeout to [{0}]:{1}".format(host,port))
        return False
        
    return False


def format_message(result):
    """
    Format message for logging and printing.
    """

    #timestamp, name, host, port, reachable,test_id, responding, response_code, response_time, url)
    output = ''
    try:
        output =  "{timestamp:<30}{name:<15}{host:<20}{port:<7}{reachable:<10}{test_id:<15}{responding:<16}{response_code:<14}{response_time:<10}{url}".format(**result)
    except Exception as e:
    #except KeyError as e:
        print("Whups. [{0}]".format(str(e)))
        print(result)
    return output

def emit_header():
    keys = ['timestamp','name','host','port','reachable','test_id','responding','response_code','response_time','url']
    labels = ["Timestamp", "Name", "Host", "Port", "Reachable", "Test Id","Responding","Response Code", "Response Time", "URL"]
    results = {keys[i]: labels[i] for i in range(len(keys))}
    log_result(results)

def log_result(result):
    """
    Log and print result. This function can be replaced to redirect output as needed.
    """
    output = format_message(result)
    logging.info(output)
    print(output)


def poll_http(name, host, port, endpoint):

    url= f"http://{host}:{port}{endpoint}"
    start_time    = datetime.datetime.now()

    results = dict.fromkeys(['timestamp','name','host','port','reachable','test_id','responding','response_code','response_time','url'])

    results['url']           = url
    results['timestamp']     = start_time.isoformat()
    results['name']          = name
    results['host']          = host
    results['port']          = port
    results['response_time'] = "N/A"
    results['reachable']     = 'No'
    results['responding']    = 'No'
    results['response_code'] = 'N/A'

    response = None

        
    try:
        response = requests.get(results['url'], timeout=global_timeout)
        response.raise_for_status()
        results['status'] = 'Success'
        results['response_code'] = response.status_code

    except Timeout:
        results['responding'] = "Timeout"
    except ConnectionError as e:
        results['status'] = "Port Not Listening" if "Connection refused" in str(e) else "Unreachable"
    except RequestException as e:
        results['response_code'] = e.response.status_code if e.response else "N/A"
        results['status'] = 'Error'
    finally:
        results['response_time'] = ((datetime.datetime.now() - start_time).microseconds) / 1000000

    return results 

def main():

    emit_header()

    for name, server in servers.items():
        host = server["host"]
        start_time    = datetime.datetime.now()

        keys = ['timestamp','name','host','port','reachable','test_id','responding','response_code','response_time','url']
        defaults = [start_time.isoformat(), name, host, 0, "No", "0","No","N/A", "N/A", "N/A"]
        results = {keys[i]: defaults[i] for i in range(len(keys))}

        if ip_reachable(host):
            for test_id, profile in server["test_profiles"].items():
                protocol = profile.get("protocol", "http")
                port = profile["port"]
                if protocol == "http":
                    endpoint = profile.get("url", "/custom-endpoint")
                    results = poll_http(name, host, port, endpoint)
                results['test_id']   = test_id
                results['reachable'] = 'Yes'
                log_result(results)
        else:
            results['reachable'] = 'No'
            log_result(results)

if __name__ == "__main__":
    main()
