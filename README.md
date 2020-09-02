# Linktester (version 0.2 beta)

The program is designed to test links and images on the page.

To use the program required:

- python version > 3.6 (https://www.python.org/downloads/)
- requests (https://pypi.org/project/requests/)
- pytest (https://docs.pytest.org/en/stable/getting-started.html)
- selenium webdriver (https://selenium-python.readthedocs.io/)

See required modules for my working environment in the file "requirements.txt."

To start testing, just type in console in the tester folder, add "--url" key and page name:

**pytest linktester.py --url pagename**

To start testing in multithreading-mode add key "--th" and num of threads:

**pytest linktester.py --url pagename --th 4**

To see all process in console add pytest-key "-s":

**pytest -s linktester.py --url pagename --th 4**

To see full pytest report in console add pytest-key "-v":

**pytest -v -s linktester.py --url pagename --th 4**

To start test only for links or images add pytest-key "-k" with string "links" or "images"

**pytest -v -s -k "links" linktester.py --url pagename --th 4**

The test result is output to the console and to a log file.
If there is no log folder, it will be created with the first file.
A separate file is created for each run