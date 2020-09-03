# Linktester (version 0.3 beta)

The program is designed to test links and images on the page. ALso program may construct and test site tree.

To use the program required:

- python version > 3.6 (https://www.python.org/downloads/)
- requests (https://pypi.org/project/requests/)
- pytest (https://docs.pytest.org/en/stable/getting-started.html)
- selenium webdriver (https://selenium-python.readthedocs.io/)

See required modules for my working environment in the file "requirements.txt."

To start testing, just type in console in the tester folder, add "--url" key and page name:

**pytest linktester.py --url pagename**

To start testing in multithreading-mode add key "--th" and num of threads (by default --th=1):

**pytest linktester.py --url pagename --th 4**

To see all process in console use pytest-key "-s":

**pytest -s linktester.py --url pagename**

To see full pytest report in console use pytest-key "-v":

**pytest -v linktester.py --url pagename**

To start test only for links or images add pytest-key "-k" with string "links" or "images"

**pytest -k "links" linktester.py --url pagename**

To start test only for site in deep use pytest-key "-k" with string "deep". You can set how many levels to test in depth of the domain with key "--levels-in-deep" (by default --levels=0).

**pytest "deep" linktester.py --url pagename --levels-in-deep 2**

Full command may looks like this:

**pytest linktester.py -s -v -k "deep" --url pagename --levels-in-deep 2 --th 8**

The test result is output to the console and to a log file.
Sitemap is output to the console and a sitemap file.
If there is no log folder, it will be created with the first file.
A separate file is created for each run

**Note:** Does not work with http-sites as start page yet.