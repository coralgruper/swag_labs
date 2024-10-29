# The following automation code is designed to test the website of Swag Labs
# -------------------------------------------------------------------------------------------------------------------

# Importing relevant libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# The 'SwagLabsFunctions' class is used to initialize a chrome WebDriver and a WebDriverWait with a 10-second timeout
class SwagLabsFunctions:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def open_main_webpage(self):
        # Open the swag labs homepage, maximizes the window
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()