import pytest
import random
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


# --- 3. Test for Logout Button
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


# --- 4. Test for Reset App State button (in a separate test file: 'test_inventory_menu.py')
# Test the "Reset App State" button:
# 1. Verify that items in the cart are removed
# 2. Verify the sort filter is reset to its default option
# 3. Verify the "Remove" button changed back to "Add to Cart"
def test_reset_app_state(setup_driver):
    inventory_page = InventoryPage()
    inventory_page.driver = setup_driver
    inventory_page.wait = WebDriverWait(setup_driver, 10)
    try:
        # Attempt to select the option "Price (High to Low)"
        inventory_page.select_sort_type_text("Price (high to low)")
        # Find all add-to-cart buttons
        add_to_cart_buttons = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")
        random_item = random.choice(add_to_cart_buttons)  # Select a random button from the list and click it
        random_item.click()

        # Verify item is in the cart
        cart_count = inventory_page.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert cart_count == "1", "Failed to add item to cart before reset."

        # Verify that the button text has changed to "Remove"
        updated_random = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")[
            add_to_cart_buttons.index(random_item)]
        assert updated_random.text == "Remove", "Button did not change to 'Remove' after adding item to cart."

        # Now reset app state
        inventory_page.reset_app_state()

        # 1. Check that cart is empty after reset
        cart_icons = inventory_page.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(cart_icons) == 0, "Cart was not reset to empty."

        # 2. Check that the sort dropdown is reset to default <--- WILL FAIL: BUG
        default_sort_text = inventory_page.get_sort_type_text()
        assert default_sort_text == "Name (A to Z)", "Sort order was not reset to default."

        # 3. Verify the "Remove" button changed back to "Add to Cart" <--- WILL FAIL: BUG
        add_to_cart_button = inventory_page.driver.find_element(By.CLASS_NAME, "btn_inventory")
        assert add_to_cart_button.text == "Add to cart", "Button did not revert to 'Add to cart' after reset."

    except NoSuchElementException:
        pytest.fail("Reset app state test failed - required elements not found.")

# NOTE: This test fails when reaching verifications 2 and 3 because there's a bug in the app
# The "Reset App State" button will indeed empty the cart. However, it will not reset the sort dropdown back to default
# nor will it change the "Remove" button back to "Add to Cart"
