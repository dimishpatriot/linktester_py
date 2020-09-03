# file: test_linktester.py
# Linktester (version 0.3 beta)
# dimishpatriot@github.com, 2020

# === IMPORTS === #
import pytest
import requests
import time
from queue import Queue
from threading import Thread


# === FUNCTIONS === #
def write_main_data(url, len_of_list, type_of_data, start_time, log_file, output) -> None:
    for out in output:
        out(f"\n=== Test {type_of_data} on the page: {url} ===\n")
        out(f"Start time: {time.ctime(start_time)}\n")
        out(f"Unique {type_of_data} collected: {len_of_list}\n")
        out(f"Logfile: {log_file.name} ({log_file.encoding})\n")


def write_test_data(result, start_time, finish_time, output) -> None:
    for out in output:
        out("\nResults:\n")

        for k, v in result.items():
            out(f"- {k}: {v}\n")

        out(f"Finish time: {time.ctime(finish_time)}\n")
        out(f"Time to complete: {round(finish_time - start_time, 2)} sec.\n")


def write_out(string, output) -> None:
    for out in output:
        out(string + '\n')


def validate_status(status_code, test) -> None:
    if 200 <= status_code < 300:
        test["normal"] += 1
    elif 300 <= status_code < 400:
        test["redirect pages"] += 1
    elif 400 <= status_code < 500:
        test["broken"] += 1
    elif 500 <= status_code < 600:
        test["server errors"] += 1


def get_status_code(link, headers) -> int:
    try:
        r = requests.get(link, headers=headers)
        status_code = r.status_code
    except requests.exceptions.ConnectionError:
        status_code = 520
    return status_code


def get_status_str(link, status_code) -> str:
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
        th.append(Thread(target=check_link,
                         args=(q, result, headers, log_file)))
        th[i].start()
    for link in link_list:
        q.put(link)
    for i in range(num_threads):
        q.put(None)
    for i in range(num_threads):
        th[i].join()
    return result


def get_links_from_page(page_url, driver):
    links = set()  # change to set?
    driver.get(page_url)
    urls = driver.find_elements_by_tag_name("a")

    for url in urls:
        url_text = url.get_attribute("href")
        if url_text:
            separated_link = url_text.split('/')
            if separated_link[-1] != '#' and separated_link[0] in ("http:",
                                                                   "https:"):
                links.add(url_text)
        else:
            continue
    return links


def get_img_from_page(page_url, driver):
    images = set()  # change to set?
    driver.get(page_url)
    urls = driver.find_elements_by_tag_name("img")

    for url in urls:
        url_text = url.get_attribute("src")
        if url_text:
            if url_text.split(':')[0] != "data":
                images.add(url_text)
        else:
            continue

    return images


def get_subpages(page_url, driver):
    links_on_page = get_links_from_page(page_url, driver)
    domain = page_url.split("//")[1].split('/')[0]
    sub_pages = set(
        filter(lambda link: domain in link.split('/')[2], links_on_page))
    sub_pages = set(map(lambda link: link.split('?')[0], sub_pages))
    sub_pages = set(map(lambda link: link.rstrip('/'), sub_pages))
    return sub_pages


# === TESTS === #
@ pytest.mark.links
def test_links_on_page(page_url, driver, headers, log_file, num_threads):
    links_on_page = get_links_from_page(page_url, driver)
    start_time = time.time()
    write_main_data(url=page_url,
                    len_of_list=len(links_on_page),
                    type_of_data="links",
                    log_file=log_file,
                    output=(print, log_file.write),
                    start_time=start_time)

    result = check_links_in_multithreading(link_list=links_on_page,
                                           headers=headers,
                                           log_file=log_file,
                                           num_threads=num_threads)
    finish_time = time.time()

    write_test_data(result=result,
                    output=(print, log_file.write),
                    start_time=start_time,
                    finish_time=finish_time)

    assert result["normal"] + result["redirect"] == len(links_on_page)


@ pytest.mark.images
def test_img_on_page(page_url, driver, headers, log_file, num_threads):
    img_on_page = get_img_from_page(page_url, driver)
    start_time = time.time()
    write_main_data(url=page_url,
                    len_of_list=len(img_on_page),
                    type_of_data="images",
                    log_file=log_file,
                    output=(print, log_file.write),
                    start_time=start_time)

    result = check_links_in_multithreading(link_list=img_on_page,
                                           headers=headers,
                                           log_file=log_file,
                                           num_threads=num_threads)
    finish_time = time.time()

    write_test_data(result=result,
                    output=(print, log_file.write),
                    start_time=start_time,
                    finish_time=finish_time)

    assert result["normal"] + result["redirect"] == len(img_on_page)


@pytest.mark.deep
def test_deep_of_site(page_url, driver, headers, log_file, sitemap_file, num_threads, deep_levels):
    sitemap = set((page_url,))
    checked = set()
    write_out(f"=== Deep links test for {page_url} ===\n", (print, log_file.write))

    for level in range(deep_levels):
        write_out(f"=== LEVEL {level} ===", (print, log_file.write))
        for node in sitemap:
            if node not in checked:
                checked.add(node)
                print(f"check node = {node}")
                subpages = get_subpages(page_url=node,
                                        driver=driver)
                sitemap = sitemap.union(subpages)
            else:
                continue

    write_out(f"Sitemap complete with {len(sitemap)} page(s).\n", (print, log_file.write))

    for page in sitemap:
        write_out(page, (print, sitemap_file.write))
    write_out(f"Sitemap saved to {sitemap_file.name}\n", (print, log_file.write))

    for page in sitemap:
        try:
            test_links_on_page(page_url=page,
                               driver=driver,
                               headers=headers,
                               log_file=log_file,
                               num_threads=num_threads)
            write_out(f"Test for page {page} PASSED\n", (print, log_file.write))
        except AssertionError:
            write_out(f"Test for page {page} FAILED\n", (print, log_file.write))
            assert False

    assert True
