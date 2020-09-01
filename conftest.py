# file: conftest.py
# Linktester (version 0.1 beta)
# dimishpatriot@github.com, 2020


# === IMPORTS === #
import pytest
import time
import os
from selenium import webdriver


# === TEST SETTINGS === #
def pytest_addoption(parser):
    parser.addoption("--url",
                     default="https://test.com",
                     help="input URL for testing")


# === FIXTURES === #
@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def log_file(page_url):
    log_folder = os.path.join(os.getcwd(), "log")
    filename = ''.join(page_url.split("//")[1:])  # remove protocol

    filename = filename.replace('.', '_')
    filename = filename.replace('/', '_')
    if filename[-1] != '_':
        filename += "_"

    filename += str(int(time.time())) + ".txt"  # add time stamp

    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    filename = os.path.join(log_folder, filename)  # add folder name

    with open(filename, "w", encoding="utf-8") as f:
        f.write("-----------------------\n")
        f.write("|  Linktester report  |\n")
        f.write("-----------------------\n")
        yield f


@pytest.fixture(scope="session")
def headers():
    return {"user-agent": "chrome"}


@pytest.fixture(scope="session")
def page_url(pytestconfig):
    url = "https://{}".format(pytestconfig.getoption("--url").split("//")[-1])
    return url


@pytest.fixture()
def links_on_page(page_url, driver):
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


@pytest.fixture()
def img_on_page(page_url, driver):
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
