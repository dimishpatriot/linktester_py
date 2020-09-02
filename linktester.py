# file: test_linktester.py
# Linktester (version 0.2 beta)
# dimishpatriot@github.com, 2020

# === IMPORTS === #
import pytest
import requests
import time
from queue import Queue
from threading import Thread


# === FUNCTIONS === #
def write_main_data(url: str, len_of_list: int, type_of_data: str, start_time: float, log_file, output) -> None:
    for out in output:
        out(f"\n=== Test {type_of_data} on the page: {url} ===\n")
        out(f"Start time: {time.ctime(start_time)}\n")
        out(f"Unique {type_of_data} collected: {len_of_list}\n")
        out(f"Logfile: {log_file.name} ({log_file.encoding})\n")


def write_test_data(result: dict, start_time: float, finish_time: float, output) -> None:
    for out in output:
        out("\nResults:\n")

        for k, v in result.items():
            out(f"- {k}: {v}\n")

        out(f"Finish time: {time.ctime(finish_time)}\n")
        out(f"Time to complete: {round(finish_time - start_time, 2)} sec.\n")


def validate_status(status_code: int, test: dict) -> None:
    if 200 <= status_code < 300:
        test["normal"] += 1
    elif 300 <= status_code < 400:
        test["redirect pages"] += 1
    elif 400 <= status_code < 500:
        test["broken"] += 1
    elif 500 <= status_code < 600:
        test["server errors"] += 1


def get_status_code(link: str, headers: dict) -> int:
    try:
        r = requests.get(link, headers=headers)
        status_code = r.status_code
    except requests.exceptions.ConnectionError:
        status_code = 520
    return status_code


def get_status_str(link: str, status_code: int) -> str:
    return "{} - [{}]\n".format(link, status_code)


def check_link(q, test, headers, log_file):
    while True:
        link = q.get()
        if link is None:
            break
        else:
            status_code = get_status_code(link=link,
                                          headers=headers)
            status_str = get_status_str(link=link,
                                        status_code=status_code)
            print(f"{status_str}")
            log_file.write(status_str)

            validate_status(status_code=status_code,
                            test=test)


def check_links_in_multithreading(link_list, headers, log_file, num_threads):
    result = {"normal": 0,
              "redirect": 0,
              "broken": 0,
              "server errors": 0}

    print(f"Working threads = {num_threads}")
    log_file.write(f"\nWorking threads = {num_threads}\n")
    q = Queue(num_threads * num_threads)
    th = list()
    for i in range(num_threads):
        th.append(Thread(target=check_link, args=(
            q, result, headers, log_file)))
        th[i].start()
    for link in link_list:
        q.put(link)
    for i in range(num_threads):
        q.put(None)
    for i in range(num_threads):
        th[i].join()
    return result


# === TESTS === #
@ pytest.mark.links
def test_links_on_page(page_url, links_on_page, headers, log_file, num_threads):
    start_time = time.time()

    write_main_data(url=page_url,
                    len_of_list=len(links_on_page),
                    type_of_data="links",
                    log_file=log_file,
                    output=(print, log_file.write),
                    start_time=start_time)

    result = check_links_in_multithreading(
        links_on_page, headers, log_file, num_threads)
    finish_time = time.time()

    write_test_data(result=result,
                    output=(print, log_file.write),
                    start_time=start_time,
                    finish_time=finish_time)

    assert result["normal"] + result["redirect"] == len(links_on_page)


@ pytest.mark.images
def test_img_on_page(page_url, img_on_page, headers, log_file, num_threads):
    start_time = time.time()
    write_main_data(url=page_url,
                    len_of_list=len(img_on_page),
                    type_of_data="images",
                    log_file=log_file,
                    output=(print, log_file.write),
                    start_time=start_time)

    result = check_links_in_multithreading(img_on_page, headers, log_file, num_threads)
    finish_time = time.time()

    write_test_data(result=result,
                    output=(print, log_file.write),
                    start_time=start_time,
                    finish_time=finish_time)

    assert result["normal"] + result["redirect"] == len(img_on_page)
