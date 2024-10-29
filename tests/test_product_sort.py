import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from src.src_login_page import LoginPage
from src.src_inventory_page import InventoryPage
from selenium.webdriver.support.ui import Select


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
    yield driver  # Yield driver instead of login for broader use
    driver.quit()


# Test to check if the default sort option is set to Name (A to Z)
def test_default_sort(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver  # Use the setup driver for the inventory page
    inventory_page.wait = WebDriverWait(setup_driver, 10)  # Reuse the wait from setup

    # Fetch inventory items and check if they are sorted by name
    items_names = inventory_page.get_inventory_items_names()
    sorted_items_names = sorted(items_names)  # Sort items list for comparison

    try:
        # Verify default sort type
        default_inventory_sort_text = inventory_page.get_sort_type_text()
        expected_inventory_sort_text = "Name (A to Z)"
        assert default_inventory_sort_text == expected_inventory_sort_text, "Default order is not correct."
        assert items_names == sorted_items_names, "Items are not correctly ordered."
    except NoSuchElementException:
        pytest.fail("Could not verify the default sort option or item order.")


# Test to sort by Name (Z to A)
def test_sort_name_Z_A(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver  # Use the setup driver for the inventory page

    # Fetch inventory items and check if they are sorted by descending names
    inventory_page.select_sort_type_text("Name (Z to A)")
    items_names = inventory_page.get_inventory_items_names()
    sorted_items_names_desc = sorted(items_names, reverse=True)  # Sort items list in descending order for comparison

    try:
        # Verify descending name sort (Z to A)
        selected_inventory_sort_text = inventory_page.get_sort_type_text()
        expected_inventory_sort_text = "Name (Z to A)"
        assert selected_inventory_sort_text == expected_inventory_sort_text, "Sort type text does not match."
        assert items_names == sorted_items_names_desc, "Items are not correctly ordered by Name (Z to A)."
    except NoSuchElementException:
        pytest.fail("Could not verify the sort option or item order.")


"""

# Sort by price from low to high
def test_sort_price_low_high(self):

# Sort by Price high to low
def test_sort_price_high_low(self):

"""
