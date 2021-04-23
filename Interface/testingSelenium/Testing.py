"""

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

 """

import timegit
import unittest
from selenium import webdriver


# IMPORTANT all testcases need to start with test_
class FirstTest(unittest.TestCase):
    """A series of unit tests for a Selenium application

    """

    def test_localhost(self):
        """Tests that starting a localhost works by finding an element in the webpage

        """
        driver = webdriver.Chrome()
        driver.maximize_window()

        # Go to local host
        driver.get("http://127.0.0.1:3000/")

        # Confirmation that it went to local host
        time.sleep(3)

        # self.driver.find_element_by_class_name("App-link").click()
        driver.find_element_by_link_text("Learn React").click()
        time.sleep(3)

        driver.quit()

    def test_go_to_different_page(self):
        """Tests if you can go to a different page with Selenium by going to uu website

        """
        driver = webdriver.Chrome()
        driver.maximize_window()
        # Loads the UU informatica education page
        driver.get("https://students.uu.nl/beta/informatica")
        time.sleep(2)
        # If you right click on an element and then inspect it, you get the XPath of the element.
        # Make single quotes of the double quotes
        driver.find_element_by_xpath("//*[@id='finalist-blocks-finalist-megamenu']/div/div/ul[1]/li[3]/a").click()
        time.sleep(2)
        # So let's suppose that you want to enlist or unenlist and want to click on that option you need to click on
        driver.find_element_by_xpath("//*[@id='og-menu-og-single-menu-block']/div/ul/li[2]/ul/li[5]/a").click()
        time.sleep(2)
        driver.quit()

    def test_element_is_displayed(self):
        """Tests if an element is displayed by finding an element on the uu website

        """
        driver = webdriver.Chrome()
        driver.maximize_window()
        # Loads the UU informatica education page
        driver.get("https://students.uu.nl/beta/informatica")
        time.sleep(2)
        # If you right click on an element and then inspect it, you get the XPath of the element.
        # Make single quotes of the double quotes
        element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/picture/img")
        time.sleep(2)
        # Checking if the image is displayed on the page
        is_displayed = element.is_displayed()
        print(is_displayed)
        time.sleep(2)
        driver.quit()

    def test_login_system(self):
        """Tests logging in by logging into outlook with a fake password

        """
        driver = webdriver.Chrome()
        driver.maximize_window()

        # Go to the outlook email
        driver.get("https://outlook.live.com/owa/")
        time.sleep(2)
        # Go to the login page
        driver.find_element_by_xpath("/html/body/header/div/aside/div/nav/ul/li[2]/a").click()

        # Enter the email adress (my old spam email)
        driver.find_element_by_xpath("//*[@id='i0116']").send_keys("berenddekker@live.nl")
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='idSIButton9']").click()

        # Entering the password (fake password)
        driver.find_element_by_xpath("//*[@id='i0118']").send_keys("FakeP@ssw0rd")
        time.sleep(2)

        # In this case, we expect a failure when we try to click on this button
        # self.driver.find_element_by_xpath("invalidID").click()

        driver.quit()
