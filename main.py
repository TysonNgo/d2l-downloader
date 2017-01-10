from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import ConfigParser
import json
import os
import re
import sys

class D2L_Downloader():
    def __init__(self,driver):
        self.driver = driver

    def navigate_to_course(self,course_code):
        course_elements = config.get("Elements","courses")
        # click select a course dropdown menu
        self.driver.find_element_by_id(config.get("Elements","select-course")).click()
        
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME,course_elements)))
        
        courses = self.driver.find_elements_by_class_name(course_elements)

        for course in courses:
            if re.search(course_code,course.text,re.IGNORECASE):
                return course.click()

    def navigate_to_content(self):
        menus = self.driver.find_elements_by_class_name(config.get("Elements","menus"))
        for menu in menus:
            if "Course Materials" in menu.text:
                menu.click()
                break
        
        inner_menu = config.get("Elements","inner-menu")
        
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME,inner_menu)))
        
        inner_menus = self.driver.find_elements_by_class_name(inner_menu)
        
        for element in inner_menus:
            if "Content" in element.text:
                links = element.find_elements_by_tag_name("a")
                for link in links:
                    if "Content" in link.text:
                        return link.click()

    def download_content(self):
        self.navigate_to_content()
        
        with open("downloaded.json") as f:
            downloaded = json.load(f)
        
        textblocks = self.driver.find_elements_by_class_name(config.get("Elements","content-textblock"))
        for textblock in textblocks:
            try:
                if textblock.is_displayed() and not textblock.text.isdigit() and \
                textblock.text not in ["Table of Contents","Bookmarks","Course Schedule"]:
                    textblock.click()
                
                    sleep(1)
                    text = self.driver.find_elements_by_class_name(config.get("Elements","content-text"))
                    caret = self.driver.find_elements_by_class_name(config.get("Elements","content-caret"))[1:]
                
                    for i in range(len(text)):
                        if text[i].text not in downloaded:
                            downloaded[text[i].text] = 0
                            with open("downloaded.json","w") as f:
                                json.dump(downloaded,f,indent=4)
                            caret[i].click()
                        
                            sleep(2)
                            options = self.driver.find_elements_by_class_name(config.get("Elements","content-dropdown"))
                        
                            for option in options:
                                if option.text == "Download":
                                    option.click()
                                    sleep(3)
            except Exception as ex:
                print (ex)
                
        sleep(1)

config = ConfigParser.ConfigParser(allow_no_value=True)
config.readfp(open("config.ini"))

# d2l login credentials
username = raw_input("Enter your username: ")
password = getpass("Enter your password: ")

# courses to download from
courses = config.options("Courses")

for course in courses:
    # allow files to be automatically downloaded and saved to
    # download folder where this script is running 
    chrome_options = Options()
    prefs = {
        "download.default_directory":os.getcwd()+os.sep+"Downloads"+os.sep+course,
        "download.prompt_for_download": False
    }
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(driver,10)

    driver.get("https://learn.uwaterloo.ca/")

    form = {
        "username": driver.find_element_by_name("username"),
        "password": driver.find_element_by_name("password")
    }

    form["username"].send_keys(username)
    form["password"].send_keys(password)
    form["password"].submit()

    d2ld = D2L_Downloader(driver)
    d2ld.navigate_to_course(course)
    d2ld.navigate_to_content
    d2ld.download_content()

    # close manually when downloads are finished
