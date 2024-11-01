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


class TestInventoryFunctionality:
    # A series of basic functionality tests for the Inventory Page

    # --- 1. Test the "Go To Shopping Cart" Button
    def test_go_to_cart(self, setup_driver):
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

    # --- 2. Test the "Add To Cart" Button with multiple items
    def test_add_items_to_cart(self, setup_driver):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        # Find all "Add to Cart" buttons on the page
        add_to_cart_buttons = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")

        if not add_to_cart_buttons:
            pytest.fail("No 'Add to Cart' buttons found on the page.")

        self.num_items_to_add = random.randint(1, len(add_to_cart_buttons))
        self.selected_buttons = random.sample(add_to_cart_buttons, self.num_items_to_add)

        self.updated_buttons_list = []
        for button in self.selected_buttons:
            button.click()
            updated_button = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")[
                add_to_cart_buttons.index(button)]
            self.updated_buttons_list.append(updated_button)
            assert updated_button.text == "Remove", "Button did not change to 'Remove' after adding item to cart."

        cart_count = inventory_page.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert cart_count == str(
            self.num_items_to_add), f"Expected cart count to be {self.num_items_to_add} but got {cart_count}."

    # --- 3. Test the "Remove" (items from cart) Button with multiple items
    def test_remove_items_from_cart(self, setup_driver):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        # Add items to cart before removing
        self.test_add_items_to_cart(setup_driver)

        num_items_to_remove = random.randint(1, len(self.updated_buttons_list))
        selected_remove_buttons = random.sample(self.updated_buttons_list, num_items_to_remove)

        for remove_button in selected_remove_buttons:
            remove_button.click()
            updated_button_add = inventory_page.driver.find_elements(By.CLASS_NAME, "btn_inventory")[
                self.updated_buttons_list.index(remove_button)]
            assert updated_button_add.text == "Add to cart", "Button did not change to 'Add to cart' after removing " \
                                                             "item from cart."

        # Attempt to retrieve the cart badge; handle if it doesn't exist
        try:
            updated_cart_count = inventory_page.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        except NoSuchElementException:
            updated_cart_count = "0"  # Set to "0" if the cart badge is not present

        remaining_items = self.num_items_to_add - num_items_to_remove
        assert updated_cart_count == str(
            remaining_items), f"Expected cart count to be {remaining_items} but got {updated_cart_count}."
