import pytest
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from src.src_login_page import LoginPage
from src.src_inventory_page import InventoryPage
from src.src_cart_page import ShoppingCartPage


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


class TestCartFunctionality:
    # A series of basic functionality tests for the Shopping Cart page

    # --- 1. Verify click-ability of the "Continue Shopping" button in the Shopping Cart page
    def test_cart_continue_shopping(self, setup_driver):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        cart_page = ShoppingCartPage()
        cart_page.driver = setup_driver
        cart_page.wait = WebDriverWait(setup_driver, 10)

        try:
            inventory_page.go_to_cart()
            cart_page.cart_continue_shopping()
            inventory = inventory_page.driver.find_element(By.ID, "inventory_container")
            assert inventory.is_displayed(), "Continue Shopping button failed - didn't go back to Inventory page."
        except NoSuchElementException:
            pytest.fail("Continue Shopping button not found.")

    # --- 2. Verify click-ability of the "Checkout" button in the Shopping Cart page
    def test_cart_checkout(self, setup_driver):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        cart_page = ShoppingCartPage()
        cart_page.driver = setup_driver
        cart_page.wait = WebDriverWait(setup_driver, 10)

        try:
            inventory_page.go_to_cart()
            cart_page.cart_checkout()
            checkout = inventory_page.driver.find_element(By.ID, "checkout_info_container")
            assert checkout.is_displayed(), "Checkout button failed - didn't proceed to the Checkout page."
        except NoSuchElementException:
            pytest.fail("Checkout button not found.")

    # --- 3. Verify that the items chosen in the Inventory page also appear in the Shopping Cart page
    def test_items_in_cart(self, setup_driver):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        cart_page = ShoppingCartPage()
        cart_page.driver = setup_driver
        cart_page.wait = WebDriverWait(setup_driver, 10)

        # Step 1: Retrieve all item names and prices on the Inventory Page
        all_item_names = inventory_page.get_inventory_items_names()
        all_item_prices = inventory_page.get_inventory_items_prices()

        # Step 2: Randomly select a number of items to add to the cart
        add_to_cart_buttons = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")
        num_items_to_add = random.randint(1, len(add_to_cart_buttons))
        selected_indexes = random.sample(range(len(add_to_cart_buttons)), num_items_to_add)

        # Store selected item details for comparison
        selected_item_details = []
        for idx in selected_indexes:
            item_name = all_item_names[idx]
            item_price = all_item_prices[idx]
            selected_item_details.append((item_name, item_price))

            # Add the selected item to the cart
            add_to_cart_buttons[idx].click()

        # Step 3: Navigate to the Cart Page
        inventory_page.go_to_cart()

        # Step 4: Retrieve Items in the Cart and Compare
        cart_items = cart_page.items_in_cart()

        assert len(cart_items) == len(selected_item_details), \
            f"Expected {len(selected_item_details)} items in cart, but found {len(cart_items)}."

        for idx, cart_item in enumerate(cart_items):
            cart_item_name = cart_item.find_element(By.CLASS_NAME, "inventory_item_name").text
            cart_item_price = cart_item.find_element(By.CLASS_NAME, "inventory_item_price").text
            expected_name, expected_price = selected_item_details[idx]

            assert cart_item_name == expected_name, f"Expected item name '{expected_name}' but got '{cart_item_name}'."
            assert float(cart_item_price.replace('$', '')) == expected_price, \
                f"Expected item price '{expected_price}' but got '{cart_item_price}'."