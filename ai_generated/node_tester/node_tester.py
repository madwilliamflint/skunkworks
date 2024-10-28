import requests
import logging
import json
import datetime
from requests.exceptions import RequestException, Timeout, ConnectionError
import telnetlib
import smtplib

# Initialize logging
logging.basicConfig(filename='server_responses.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load servers from JSON file
with open('servers.json', 'r') as f:
    servers = json.load(f)

def log_message(timestamp, name, host, port, status, response_code, response_time, url):
    message = f"{timestamp:<30}{name:<15}{host:<20}{port:<7}{status:<16}{response_code:<14}{response_time:<10}{url}"
    logging.info(message)
    print(message)

def poll_http(name, host, port, endpoint):
    url = f"http://{host}:{port}{endpoint}"
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    response_time = "N/A"
    try:
        response = requests.get(url, timeout=10)
        response_time = datetime.datetime.now() - start_time
        response.raise_for_status()
        log_message(timestamp, name, host, port, "Success", response.status_code, f"{response_time.total_seconds()}s", url)
    except Timeout:
        response_time = datetime.datetime.now() - start_time
        log_message(timestamp, name, host, port, "Timeout", "N/A", f"{response_time.total_seconds()}s", url)
    except ConnectionError as e:
        response_time = datetime.datetime.now() - start_time
        if "Connection refused" in str(e):
            log_message(timestamp, name, host, port, "Port Not Listening", "N/A", f"{response_time.total_seconds()}s", url)
        else:
            log_message(timestamp, name, host, port, "Unreachable", "N/A", f"{response_time.total_seconds()}s", url)
    except RequestException as e:
        response_time = datetime.datetime.now() - start_time
        response_code = e.response.status_code if e.response else "N/A"
        log_message(timestamp, name, host, port, "Error", response_code, f"{response_time.total_seconds()}s", url)

def poll_telnet(name, host, port):
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    try:
        tn = telnetlib.Telnet(host, port, timeout=10)
        response_time = datetime.datetime.now() - start_time
        tn.close()
        log_message(timestamp, name, host, port, "Success", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    except TimeoutError:
        response_time = datetime.datetime.now() - start_time
        log_message(timestamp, name, host, port, "Timeout", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    except ConnectionRefusedError:
        response_time = datetime.datetime.now() - start_time
        log_message(timestamp, name, host, port, "Port Not Listening", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")
    except Exception as e:
        response_time = datetime.datetime.now() - start_time
        log_message(timestamp, name, host, port, "Unreachable", "N/A", f"{response_time.total_seconds()}s", f"telnet://{host}:{port}")

def poll_smtp(name, host, port):
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    try:
        server = smtplib.SMTP(host, port, timeout=10)
