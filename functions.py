# file: functions.py
# Linktester (version 0.1 beta)
# dimishpatriot@github.com, 2020

# === IMPORTS === #
import time
import requests
import os


# === FUNCTIONS === #
def write_main_data(url, len_of_list, type_of_data, log_file, output):
    """ """
    for out in output:
        out(f"\n=== Test {type_of_data} on the page: {url} ===\n")
        out(f"Start time: {time.ctime()}\n")
        out(f"Unique {type_of_data} collected: {len_of_list}\n")
        out(f"Logfile: {log_file.name} ({log_file.encoding})\n")


def write_test_data(result, output):
    """ """
    for out in output:
        out("\nResults:\n")
        for k, v in result.items():
            out(f"- {k}: {v}\n")
        out(f"Finish time: {time.ctime()}\n")


def validate_status(status_code, test):
    result = True
    if status_code != requests.codes.ok:
        if 400 <= status_code < 500:
            result = False
            test["broken"] += 1
        elif 500 <= status_code < 600:
            test["server errors"] += 1
        elif 300 <= status_code < 400:
            test["redirect pages"] += 1
    return result


def get_num_normal_links(test):
    return test["all links"] - \
        test["broken"] - test["server errors"] - test["redirect"]


def get_filename(page_url, data_type):
    log_folder = os.path.join(os.getcwd(), "log")
    filename = ''.join(page_url.split("//")[1:])  # remove protocol

    filename = filename.replace('.', '_')
    filename = filename.replace('/', '_')
    if filename[-1] != '_':
        filename += "_"

    filename += str(int(time.time()))  # add time stamp
    filename += ".txt"
    filename = "data_type" + "_" + filename

    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    filename = os.path.join(log_folder, filename)  # add folder name

    return filename
