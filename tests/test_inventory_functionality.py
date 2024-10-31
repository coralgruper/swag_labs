import pytest
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from src.src_login_page import LoginPage
from src.src_inventory_page import InventoryPage


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


# A series of basic functionality tests for the Inventory Page


# 1. Test the "Go To Shopping Cart" Button
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


# 2. Test the "Add To Cart" Button with multiple items
def test_add_items_to_cart(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver
    inventory_page.wait = WebDriverWait(setup_driver, 10)

    try:
        # Find all "Add to Cart" buttons on the page
        add_to_cart_buttons = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")

        if not add_to_cart_buttons:
            pytest.fail("No 'Add to Cart' buttons found on the page.")

        num_items_to_add = random.randint(1, len(add_to_cart_buttons))
        selected_buttons = random.sample(add_to_cart_buttons, num_items_to_add)

        # Track the indices of items added to the cart
        for button in selected_buttons:
            button.click()
            # Re-fetch the button to verify the text has changed
            updated_button = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")[
                add_to_cart_buttons.index(button)]
            assert updated_button.text == "Remove", "Button did not change to 'Remove' after adding item to cart."

        # Verify cart count matches the number of items added
        cart_count = inventory_page.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert cart_count == str(
            num_items_to_add), f"Expected cart count to be {num_items_to_add} but got {cart_count}."

    except NoSuchElementException:
        pytest.fail("Add Multiple Items To Cart failed - Required elements not found.")


# 3. Test for Logout Button
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


def test_remove_items_from_cart(setup_driver):
    pass
# 4. Test for Reset App State button (in a separate test file: 'test_reset_app_state.py')
