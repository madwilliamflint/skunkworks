import requests
import logging
import json
import datetime
from requests.exceptions import RequestException, Timeout, ConnectionError

# Initialize logging
logging.basicConfig(filename='server_responses.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load servers from JSON file
with open('servers.json', 'r') as f:
    servers = json.load(f)

def log_message(timestamp, name, host, port, status, response_code, response_time):
    message = f"{timestamp:<30}{name:<15}{host:<20}{port:<7}{status:<16}{response_code:<14}{response_time:<10}"
    logging.info(message)
    print(message)

def poll_server(name, host, port):
    url = f"http://{host}:{port}/custom-endpoint"
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    response_time = "N/A"
    try:
        response = requests.get(url, timeout=10)
        response_time = datetime.datetime.now() - start_time
        response.raise_for_status()
        log_message(timestamp, name, host, port, "Success", response.status_code, f"{response_time.total_seconds()}s")
    except Timeout:
        response_time = datetime.datetime.now() - start_time
        log_message(timestamp, name, host, port, "Timeout", "N/A", f"{response_time.total_seconds()}s")
    except ConnectionError as e:
        response_time = datetime.datetime.now() - start_time
        if "Connection refused" in str(e):
            log_message(timestamp, name, host, port, "Port Not Listening", "N/A", f"{response_time.total_seconds()}s")
        else:
            log_message(timestamp, name, host, port, "Unreachable", "N/A", f"{response_time.total_seconds()}s")
    except RequestException:
        response_time = datetime.datetime.now() - start_time
        log_message(timestamp, name, host, port, "Error", "N/A", f"{response_time.total_seconds()}s")

def main():
    header = f"{'Timestamp':<30}{'Name':<15}{'Host':<20}{'Port':<7}{'Status':<16}{'Response Code':<14}{'Response Time'}"
    logging.info(header)
    print(header)
    for name, server in servers.items():
        poll_server(name, server['host'], server['port'])

if __name__ == "__main__":
    main()
