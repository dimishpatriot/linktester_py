# Linktester (version 0.1 beta)

The program is designed to test links and images on the page.

To use the program required:

- python version > 3.6 (https://www.python.org/downloads/)
- requests (https://pypi.org/project/requests/)
- pytest (https://docs.pytest.org/en/stable/getting-started.html)
- selenium webdriver (https://selenium-python.readthedocs.io/)

See modules for my working environment in the file "requirements.txt."

To start testing, just type in console in the tester folder.

**pytest linktester.py --url sitename**

Adding other pytest options is available, for example adding -k "images" or -k "links" will only test images or links.

The test result is output to the console and to a log file. If there is no log folder, it will be created with the first file.
