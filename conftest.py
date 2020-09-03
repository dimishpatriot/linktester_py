# file: conftest.py
# Linktester (version 0.3 beta)
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
    parser.addoption("--th",
                     default=1,
                     help="input num threads")
    parser.addoption("--levels-in-deep",
                     default=0,
                     help="input deep levels")


# === FIXTURES === #
@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def num_threads(pytestconfig):
    return int(pytestconfig.getoption("--th"))


@pytest.fixture(scope="session")
def deep_levels(pytestconfig):
    return int(pytestconfig.getoption("--levels-in-deep"))


@pytest.fixture(scope="session")
def log_file(page_url):
    log_folder = os.path.join(os.getcwd(), "log")
    filename = ''.join(page_url.split("//")[1:])  # remove protocol

    filename = filename.replace('.', '_')
    filename = filename.replace('/', '_')
    if filename[-1] != '_':
        filename += "_"
    filename += str(int(time.time())) + ".txt"  # add time stamp and extension

    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    filename = os.path.join(log_folder, filename)  # add folder name

    with open(filename, "w", encoding="utf-8") as f:
        f.write("----------------------------------------------------------\n")
        f.write("|                   * Linktester v.0.2 *                 |\n")
        f.write("|         github.com/dimishpatriot/linktester_py         |\n")
        f.write("|                       TEST LOG                         |\n")
        f.write("----------------------------------------------------------\n\n")
        yield f


@pytest.fixture(scope="session")
def sitemap_file(page_url):
    log_folder = os.path.join(os.getcwd(), "log")
    filename = ''.join(page_url.split("//")[1:])  # remove protocol

    filename = filename.replace('.', '_')
    filename = filename.replace('/', '_')
    if filename[-1] != '_':
        filename += "_"
    filename += str(int(time.time())) + "_sitemap.txt"  # add time stamp and extension

    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    filename = os.path.join(log_folder, filename)  # add folder name

    with open(filename, "w", encoding="utf-8") as f:
        f.write("----------------------------------------------------------\n")
        f.write("|                   * Linktester v.0.2 *                 |\n")
        f.write("|         github.com/dimishpatriot/linktester_py         |\n")
        f.write("|                       SITEMAP LOG                      |\n")
        f.write("----------------------------------------------------------\n\n")
        f.write(f"...for page {page_url}\n")
        yield f


@pytest.fixture(scope="session")
def headers():
    return {"user-agent": "chrome"}


@pytest.fixture(scope="session")
def page_url(pytestconfig):
    url = "https://{}".format(pytestconfig.getoption("--url").split("//")[-1])
    return url
