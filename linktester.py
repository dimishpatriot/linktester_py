# file: test_linktester.py
# Linktester (version 0.1 beta)
# dimishpatriot@github.com, 2020

# === IMPORTS === #
import pytest
import requests
from functions import *


# === TESTS === #
@pytest.mark.links
def test_links_on_page(page_url, links_on_page, headers, log_file):
    """ """
    write_main_data(url=page_url,
                    len_of_list=len(links_on_page),
                    type_of_data="links",
                    log_file=log_file,
                    output=(print, log_file.write))

    result = True
    test = {"all links": len(links_on_page),
            "normal": 0,
            "redirect": 0,
            "broken": 0,
            "server errors": 0}
    print("\nTesting links:\n")
    counter = 1
    for link in links_on_page:
        try:
            r = requests.get(link, headers=headers)
            status_code = r.status_code
        except requests.exceptions.ConnectionError:
            status_code = 520

        status_str = f"{link} - [{status_code}]\n"
        log_file.write(status_str)
        print(f"({counter} of {test['all links']}) {status_str}")
        counter += 1
        result = validate_status(status_code, test)

    test["normal"] = get_num_normal_links(test)

    write_test_data(result=test,
                    output=(print, log_file.write))

    assert result == 1


@pytest.mark.images
def test_img_on_page(page_url, img_on_page, headers, log_file):
    """ """
    write_main_data(url=page_url,
                    len_of_list=len(img_on_page),
                    type_of_data="images",
                    log_file=log_file,
                    output=(print, log_file.write))

    result = True
    test = {"all links": len(img_on_page),
            "normal": 0,
            "redirect": 0,
            "broken": 0,
            "server errors": 0}
    print("\nTesting images:\n")
    counter = 1
    for link in img_on_page:
        try:
            r = requests.get(link, headers=headers)
            status_code = r.status_code
        except requests.exceptions.ConnectionError:
            status_code = 520

        status_str = f"{link} - [{status_code}]\n"
        log_file.write(status_str)
        print(f"({counter} of {test['all links']}) {status_str}")
        counter += 1
        result = validate_status(status_code, test)

    test["normal"] = get_num_normal_links(test)

    write_test_data(result=test,
                    output=(print, log_file.write))

    assert result == 1
