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

def log_result(result):
    """
    Log and print result. This function can be replaced to redirect output as needed.
    """
    logging.info(result)
    print(result)

def format_message(timestamp, name, host, port, status, response_code, response_time, url):
    """
    Format message for logging and printing.
    """
    return f"{timestamp:<30}{name:<15}{host:<20}{port:<7}{status:<16}{response_code:<14}{response_time:<10}{url}"

def poll_http(name, host, port, endpoint):
    url = f"http://{host}:{port}{endpoint}"
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    response_time = "N/A"
    try:
        response = requests.get(url, timeout=10)
        response_time = datetime.datetime.now() - start_time
        response.raise_for_status()
        result = format_message(timestamp, name, host, port, "Success", response.status_code, f"{response_time.total_seconds()}s", url)
    except Timeout:
        response_time = datetime.datetime.now() - start_time
        result = format_message(timestamp, name, host, port, "Timeout", "N/A", f"{response_time.total_seconds()}s", url)
    except ConnectionError as e:
        response_time = datetime.datetime.now() - start_time
        status = "Port Not Listening" if "Connection refused" in str(e) else "Unreachable"
        result = format_message(timestamp, name, host, port, status, "N/A", f"{response_time.total_seconds()}s", url)
    except RequestException as e:
        response_time = datetime.datetime.now() - start_time
        response_code = e.response.status_code if e.response else "N/A"
        result = format_message(timestamp, name, host, port, "Error", response_code, f"{response_time.total_seconds()}s", url)
    log_result(result)

def poll_telnet(name, host, port):
    timestamp = datetime.datetime.now().isoformat()
    start_time = datetime.datetime.now()
    try:
        tn = telnetlib.Telnet(host, port, timeout=10)
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
        server = smtplib.SMTP(host, port, timeout=10)
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
    header = format_message("Timestamp", "Name", "Host", "Port", "Status", "Response Code", "Response Time", "URL")
    log_result(header)
    for name, server in servers.items():
        host = server["host"]
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
