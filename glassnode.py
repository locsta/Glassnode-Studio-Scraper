from selenium_scraper import SeleniumClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from datetime import datetime
import os
import pandas as pd
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pprint import pprint
from itertools import cycle
import pyautogui
import threading

def scrape_glassnode_studio():
    login_email = input("Please enter your email address:")
    login_password = input("Please enter your password:")
    url = "https://studio.glassnode.com/metrics?a=BTC&m=addresses.ActiveCount"
    browser = SeleniumClass(headless=False).open_browser()
    browser.get(url)
    time.sleep(5)
    browser.find_element_by_class_name("ant-btn-link").click()
    browser.find_element_by_id("loginForm_email").send_keys(login_email)
    browser.find_element_by_id("loginForm_password").send_keys(login_password)
    time.sleep(1)
    browser.find_element_by_class_name("ant-btn-primary").click()
    list_sections = {}
    time.sleep(8)
    couldn_scrape = []
    for i in range(3, 21, 1):
        time.sleep(5)
        # Click on each category
        category = browser.find_element_by_xpath(f"/html/body/div[1]/section/main/div/div[1]/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div[{i}]")
        category_name = category.text.split("\n")[0]
        print("category_name: " + category_name)
        list_sections[category_name] = {}
        category.click()
        # Select sections
        sections = browser.find_elements_by_class_name("ant-collapse-content-box")
        len_sections = len(sections)
        for j in range(len_sections):
            section_name = sections[j].find_element_by_xpath('..').text.split("\n")[1]
            list_sections[category_name][section_name] = []
            print("section_name: " + section_name)
            csv_pages = sections[j].find_elements_by_tag_name("a")
            for page in csv_pages:
                page_name = page.text.replace("\n", " - ")
                list_sections[category_name][section_name].append(page_name)
                print("page_name: " + page_name)
                page.click()
                time.sleep(5)
                # Download CSV file
                try:
                    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div[2]/div/div[1]/div[4]/div[2]/div/button[2]/span[1]')))
                    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/div/div[1]/div[4]/div[2]/div/button[2]/span[1]").click()
                    time.sleep(1)
                    pyautogui.click((3645, 811))
                    time.sleep(1)
                    pyautogui.click((4031, 882))
                    time.sleep(1)
                except:
                    couldn_scrape.append(f"Couldnt scrape CSV: {category_name} -- {section_name} -- {page_name}")
                # Download JSON file
                try:
                    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/div/div[1]/div[4]/div[2]/div/button[1]/span[2]").click()
                    time.sleep(1)
                    pyautogui.click((3645, 811))
                    time.sleep(1)
                    pyautogui.click((4031, 882))
                except:
                    couldn_scrape.append(f"Couldnt scrape JSON: {category_name} -- {section_name} -- {page_name}")
            sections = browser.find_elements_by_class_name("ant-collapse-content-box")

        # Click on return to categories
        browser.find_element_by_xpath(f"/html/body/div[1]/section/main/div/div[1]/div/div[3]/div[2]/div[2]/div/div/div[1]/div").click()
    
    # Dump json files tree for later use (to organise files into folders)
    with open("files_tree.json", "w") as outfile:
        json.dump(list_sections, outfile)

    # Dump json files tree of non-scraped files (files not available for download on glassnode studio)
    with open("not_scraped.json", "w") as outfile:
        json.dump(couldn_scrape, outfile)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    scrape_glassnode_studio()