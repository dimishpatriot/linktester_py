# file: test_linktester.py
# Linktester (version 0.1 beta)
# dimishpatriot@github.com, 2020

# === IMPORTS === #
import pytest
import requests
import time


# === FUNCTIONS === #
def write_main_data(url, len_of_list, type_of_data,
                    log_file, output, start_time):
    """ """
    for out in output:
        out(f"\n=== Test {type_of_data} on the page: {url} ===\n")
        out(f"Start time: {time.ctime(start_time)}\n")
        out(f"Unique {type_of_data} collected: {len_of_list}\n")
        out(f"Logfile: {log_file.name} ({log_file.encoding})\n")


def write_test_data(result, output,
                    start_time, finish_time):
    """ """
    for out in output:
        out("\nResults:\n")
        for k, v in result.items():
            out(f"- {k}: {v}\n")

        out(f"Finish time: {time.ctime(finish_time)}\n")
        complete_time = int(finish_time - start_time)
        out(f"Time to complete: {complete_time} sec.\n")


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


def get_status_code(link, headers):
    try:
        r = requests.get(link, headers=headers)
        status_code = r.status_code
    except requests.exceptions.ConnectionError:
        status_code = 520

    return status_code


def get_status_str(link, status_code):
    return "{} - [{}]\n".format(link, status_code)


# === TESTS === #
@pytest.mark.links
def test_links_on_page(page_url, links_on_page, headers, log_file):
    """ """
    start_time = time.time()
    write_main_data(url=page_url,
                    len_of_list=len(links_on_page),
                    type_of_data="links",
                    log_file=log_file,
                    output=(print, log_file.write),
                    start_time=start_time)

    result = True
    test = {"all links": len(links_on_page),
            "normal": 0,
            "redirect": 0,
            "broken": 0,
            "server errors": 0}

    print("\nTesting links:\n")
    log_file.write("\nTesting links:\n")

    for link in links_on_page:
        status_code = get_status_code(link, headers)
        status_str = get_status_str(link, status_code)

        print(f"{status_str}")
        log_file.write(status_str)

        result = validate_status(status_code, test)

    finish_time = time.time()
    test["normal"] = get_num_normal_links(test)

    write_test_data(result=test,
                    output=(print, log_file.write),
                    start_time=start_time,
                    finish_time=finish_time)

    assert result == 1


@pytest.mark.images
def test_img_on_page(page_url, img_on_page, headers, log_file):
    """ """
    start_time = time.time()
    write_main_data(url=page_url,
                    len_of_list=len(img_on_page),
                    type_of_data="images",
                    log_file=log_file,
                    output=(print, log_file.write),
                    start_time=start_time)

    result = True
    test = {"all links": len(img_on_page),
            "normal": 0,
            "redirect": 0,
            "broken": 0,
            "server errors": 0}

    print("\nTesting images:\n")
    log_file.write("\nTesting images:\n")

    for link in img_on_page:
        status_code = get_status_code(link, headers)
        status_str = get_status_str(link, status_code)
        log_file.write(status_str)

        print(f"{status_str}")
        result = validate_status(status_code, test)

    finish_time = time.time()
    test["normal"] = get_num_normal_links(test)

    write_test_data(result=test,
                    output=(print, log_file.write),
                    start_time=start_time,
                    finish_time=finish_time)

    assert result == 1
