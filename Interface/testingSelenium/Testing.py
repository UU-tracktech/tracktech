import unittest
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# IMPORTANT all testcases need to start with test_
class FirstTest(unittest.TestCase):

    def test_localHost(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Go to local host
        self.driver.get("http://127.0.0.1:3000/")

        # Confirmation that it went to local host
        time.sleep(3)

        # self.driver.find_element_by_class_name("App-link").click()
        self.driver.find_element_by_link_text("Learn React").click()
        time.sleep(3)

        self.driver.quit()

    def test_GoToDifferentPage(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # Loads the UU informatica education page
        self.driver.get("https://students.uu.nl/beta/informatica")
        time.sleep(2)
        # If you right click on an element and then inspect it, you get the XPath of the element.
        # Make single quotes of the double quotes
        self.driver.find_element_by_xpath("//*[@id='finalist-blocks-finalist-megamenu']/div/div/ul[1]/li[3]/a").click()
        time.sleep(2)
        # So let's suppose that you want to enlist or unenlist and want to click on that option you need to click on
        self.driver.find_element_by_xpath("//*[@id='og-menu-og-single-menu-block']/div/ul/li[2]/ul/li[5]/a").click()
        time.sleep(2)
        self.driver.quit()

    def test_ElementIsDisplayed(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # Loads the UU informatica education page
        self.driver.get("https://students.uu.nl/beta/informatica")
        time.sleep(2)
        # If you right click on an element and then inspect it, you get the XPath of the element.
        # Make single quotes of the double quotes
        element = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/picture/img")
        time.sleep(2)
        # Checking if the image is displayed on the page
        isDisplayed = element.is_displayed()
        print(isDisplayed)
        time.sleep(2)
        self.driver.quit()

    def test_loginsystem(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Go to the outlook email
        self.driver.get("https://outlook.live.com/owa/")
        time.sleep(2)
        # Go to the login page
        self.driver.find_element_by_xpath("/html/body/header/div/aside/div/nav/ul/li[2]/a").click()

        # Enter the email adress (my old spam email)
        self.driver.find_element_by_xpath("//*[@id='i0116']").send_keys("berenddekker@live.nl")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='idSIButton9']").click()

        # Entering the password (fake password)
        self.driver.find_element_by_xpath("//*[@id='i0118']").send_keys("FakeP@ssw0rd")
        time.sleep(2)

        # In this case, we expect a failure when we try to click on this button
        # self.driver.find_element_by_xpath("invalidID").click()

        self.driver.quit()\
