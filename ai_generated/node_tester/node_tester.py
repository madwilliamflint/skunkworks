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

def poll_server(name, host, port):
    url = f"http://{host}:{port}/custom-endpoint"
    start_time = datetime.datetime.now()
    try:
        response = requests.get(url, timeout=10)
        response_time = datetime.datetime.now() - start_time
        response.raise_for_status()
        message = f"{name}\t{host}:{port}\tSuccess\t{response.status_code}\t{response_time.total_seconds()}s"
        logging.info(message)
        print(message)
    except Timeout:
        message = f"{name}\t{host}:{port}\tTimeout\tN/A\tN/A"
        logging.error(message)
        print(message)
    except ConnectionError:
        message = f"{name}\t{host}:{port}\tConnection Error\tN/A\tN/A"
        logging.error(message)
        print(message)
    except RequestException as e:
        message = f"{name}\t{host}:{port}\tError\t{str(e)}\tN/A"
        logging.error(message)
        print(message)

def main():
    header = "Name\tHost:Port\tStatus\tResponse Code\tResponse Time"
    logging.info(header)
    print(header)
    for name, server in servers.items():
        poll_server(name, server['host'], server['port'])

if __name__ == "__main__":
    main()
