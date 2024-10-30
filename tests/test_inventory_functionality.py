import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from src.src_login_page import LoginPage
from src.src_inventory_page import InventoryPage
from selenium.webdriver.common.by import By


# Fixture to set up and tear down the Selenium WebDriver
@pytest.fixture
def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    login = LoginPage()
    login.driver = driver
    login.wait = wait
    login.open_main_webpage()
    login.set_username("standard_user")
    login.set_password("secret_sauce")
    login.login_button()
    yield driver
    driver.quit()


"""
# How do I check if the webpage has been reset?
def test_reset_app_state(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver  # Use the setup driver for the inventory page
    inventory_page.wait = WebDriverWait(setup_driver, 10)  # Reuse the wait from setup

    try:
        inventory_page.reset_app_state()
        assert 
"""


# Check the go to shopping cart page functionality
def test_go_to_cart(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver
    inventory_page.wait = WebDriverWait(setup_driver, 10)

    try:
        inventory_page.go_to_cart()
        shopping_cart_page = inventory_page.driver.find_element(By.ID, "cart_contents_container")
        inventory_page.driver.save_screenshot("shopping_cart_page.png")
        assert shopping_cart_page.is_displayed(), "Go to cart failed - Shopping cart page not found."
    except NoSuchElementException:
        pytest.fail("Go to cart failed - Shopping cart page not found.")


def test_logout(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver
    inventory_page.wait = WebDriverWait(setup_driver, 10)

    try:
        inventory_page.logout()
        login_page = inventory_page.driver.find_element(By.ID, "root")
        inventory_page.driver.save_screenshot("login_page.png")
        assert login_page.is_displayed(), "Logout failed - Login page not found."
    except NoSuchElementException:
        pytest.fail("Logout failed - Login page not found.")