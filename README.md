# d2l-downloader

This script uses Selenium to automatically download various files from the desired courses on D2L. Follow the steps below before running the Python script.

* download the appropriate chromedriver from here: https://sites.google.com/a/chromium.org/chromedriver/downloads (I used ChromeDriver 2.27)
* extract the chromedriver to the directory of the script
* run this command in the terminal ```pip install selenium```
* open ```config.ini``` with any text editor
* enter the courses of interest to download files from  below the *[Courses]* header (ie. CS 135)
* run the Python script in the terminal with ```python main.py```
* enter login credentials into the console
