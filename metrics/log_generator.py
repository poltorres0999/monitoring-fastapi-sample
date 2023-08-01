import time
import random
import json
from datetime import datetime, timedelta
METHODS = ["GET", "POST", "PUT", "DELETE"]
LOG_LEVEL = ["ERROR", "WARNING", "DEBUG", "INFO"]
MODULES = ["module_1", "module_2", "module_3"]
FUNCTIONS = ["function_1", "function_2", "function_3"]
STATUS_CODES = [200, 400, 500]
URLS = ["api/vi/foo", "api/vi/bar", "api/vi/buz"]


def generate_fake_function_log():
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    log_level = random.choice(LOG_LEVEL)
    module = random.choice(MODULES)
    function = random.choice(FUNCTIONS)

    log_data = f"{timestamp} | {log_level} | Module: {module} | Function: {function}| Log message level {log_level} from module {module} at function {function}"

    return log_data


def generate_request_log():
    url = random.choice(URLS)
    status_code = random.choice(STATUS_CODES)
    time_ms = random.randint(100, 1500)
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    method = random.choice(METHODS)
    log_level = random.choice(LOG_LEVEL)

    log_data = f"{timestamp} | {log_level} | {method} {url} | Requested by: Undefined Status: {status_code} Duration: {time_ms} ms"

    return log_data


def write_logs_to_file(general_log_path: str, requests_log_path: str, interval: int = 2):
    while True:
        if random.randint(0, 1) == 1:
            with open(general_log_path, "a") as log_file:
                fake_log = generate_request_log()
                log_file.write(fake_log)
                log_file.write("\n")

            with open(requests_log_path, "a") as log_file:
                fake_log = generate_request_log()
                log_file.write(fake_log)
                log_file.write("\n")
        else:
            with open(general_log_path, "a") as log_file:
                fake_log = generate_fake_function_log()
                log_file.write(fake_log)
                log_file.write("\n")

        time.sleep(interval)


if __name__ == "__main__":
    general_log_path = "/var/logs/logs.log"
    requests_log_path = "/var/logs/requests.log"
    iterations = 1
    write_logs_to_file(general_log_path=general_log_path,
                       requests_log_path=requests_log_path, interval=1)
