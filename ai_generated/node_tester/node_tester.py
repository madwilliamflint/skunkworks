import requests
import logging
import json
import datetime
import socket
from requests.exceptions import RequestException, Timeout, ConnectionError
import telnetlib
import smtplib


global_timeout=5

# Initialize logging
logging.basicConfig(filename='server_responses.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load servers from JSON file
with open('servers.json', 'r') as f:
    servers = json.load(f)


def ip_reachable(host,port,timeout=global_timeout):
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host,port))
        sock.close()
        return True
    except ConnectionRefusedError:
        return True
    except TimeoutError:
        return False
        
    return False

def log_result(result):
    """
    Log and print result. This function can be replaced to redirect output as needed.
    """
    logging.info(result)
    print(result)

def format_message(timestamp, name, host, port, reachable, responding, response_code, response_time, url):
    """
    Format message for logging and printing.
    """
    return f"{timestamp:<30}{name:<15}{host:<20}{port:<7}{reachable:<10}{responding:<16}{response_code:<14}{response_time:<10}{url}"

def poll_http(name, host, port, endpoint):

    url= f"http://{host}:{port}{endpoint}"
    start_time    = datetime.datetime.now()

    results = dict.fromkeys(['timestamp','name','host','port','reachable','responding','response_code','response_time, url'])

    results['url']           = url
    results['timestamp']     = start_time.isoformat()
    results['name']          = name
    results['response_time'] = "N/A"
    results['reachable']     = 'No'
    results['responding']    = 'No'
    results['response_code'] = 'N/A'
    results['response_time'] = 'N/A'

    response = None

        
    try:
        response = requests.get(results[''], timeout=global_timeout)
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
        results['response_time'] = datetime.datetime.now() - start_time

    return results 

def poll_telnet(name, host, port):
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    try:
        tn = telnetlib.Telnet(host, port, timeout=global_timeout)
        response_time = datetime.datetime.now() - start_time
        tn.close()
        result = format_message(timestamp, name, host, port, "Success", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    except TimeoutError:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Timeout", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    except ConnectionRefusedError:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Port Not Listening", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    except Exception as e:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Unreachable", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    log_result(result)

def poll_smtp(name, host, port):
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    try:
        server = smtplib.SMTP(host, port, timeout=global_timeout)
        server.noop()
        response_time = datetime.datetime.now() - start_time
        server.quit()
        result = format_message(timestamp, name, host, port, "Success", "N/A", f"{response_time.total_seconds()}s", f"smtp://{host}:{port}")
    except Timeout:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Timeout", "N/A", f"{response_time.total_seconds()}s", f"smtp://{host}:{port}")
    except ConnectionRefusedError:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Port Not Listening", "N/A", f"{response_time.total_seconds()}s", f"smtp://{host}:{port}")
    except Exception as e:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Unreachable", "N/A", f"{response_time.total_seconds()}s", f"smtp://{host}:{port}")
    log_result(result)

def main():
    
    header = format_message("Timestamp", "Name", "Host", "Port", "Reachable", "Responding","Response Code", "Response Time", "URL")
    log_result(header)
    for name, server in servers.items():
        host = server["host"]

        reachable = False
        if ip_reachable(host,port):
            reachable = True

            for test_id, profile in server["test_profiles"].items():
                protocol = profile.get("protocol", "http")
                port = profile["port"]
                if protocol == "http":
                    endpoint = profile.get("url", "/custom-endpoint")
                    poll_http(name, host, port, endpoint)
                elif protocol == "telnet":
                    poll_telnet(name, host, port)
                elif protocol == "smtp":
                    poll_smtp(name, host, port)

if __name__ == "__main__":
    main()
