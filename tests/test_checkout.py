import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from src.src_login_page import LoginPage
from src.src_inventory_page import InventoryPage
from src.src_checkout_page import CheckoutPage
from src.src_cart_page import ShoppingCartPage
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


# Test the Checkout process functionality
class TestCheckout:

    # --- 1. Test for a successful checkout information
    @pytest.mark.parametrize(
        "first_name, last_name, postal_code",
        [
            ('Mickey', 'Mouse', '123456'),
        ]
    )
    # Validate Your Information in the Checkout Page
    def test_successful_checkout(self, setup_driver, first_name, last_name, postal_code):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        cart_page = ShoppingCartPage()
        cart_page.driver = setup_driver
        cart_page.wait = WebDriverWait(setup_driver, 10)

        checkout_page = CheckoutPage()
        checkout_page.driver = setup_driver
        checkout_page.wait = WebDriverWait(setup_driver, 10)

        try:
            # Take necessary steps to reach the Checkout Page
            inventory_page.add_random_items_to_cart()
            inventory_page.go_to_cart()
            cart_page.cart_checkout()

            # Verify the user is redirected to the 'Checkout: Your Information' page
            checkout_your_information_page = checkout_page.driver.find_element(By.ID, "checkout_info_container")
            assert checkout_your_information_page.is_displayed(), "Checkout failed - Checkout: Your Information page " \
                                                                  "not found. "

            # Insert relevant data
            checkout_page.perform_checkout(first_name, last_name, postal_code)
            checkout_page.checkout_continue()

            # Verify the user is redirected to the 'Checkout: Overview' page
            checkout_overview_page = checkout_page.driver.find_element(By.ID, "checkout_summary_container")
            assert checkout_overview_page.is_displayed(), "Checkout failed - Checkout: Overview page not found."

            # Verify the price before taxes is as appears on the screen
            total_price_displayed = checkout_page.driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
            assert float(total_price_displayed.text.replace('Item total: $', '')) == checkout_page.get_total_price(), \
                "Checkout failed - Total Price miscalculated. "

            checkout_page.checkout_finish()
            checkout_complete_page = checkout_page.driver.find_element(By.ID, "checkout_complete_container")
            assert checkout_complete_page.is_displayed(), "Checkout failed - Checkout: Complete page not found."

        except NoSuchElementException:
            pytest.fail("Checkout failed - required elements not found.")

    # --- 2. Test for a non-successful checkout information
    @pytest.mark.parametrize(
        "first_name, last_name, postal_code, expected_error_message",
        [
            ('', '', '', 'Error: First Name is required'),
            ('Mickey', '', '12345', 'Error: Last Name is required'),
            ('Mickey', 'Mouse', '', 'Error: Postal Code is required'),
        ]
    )
    def test_failed_checkout(self, setup_driver, first_name, last_name, postal_code, expected_error_message):
        inventory_page = InventoryPage()
        inventory_page.driver = setup_driver
        inventory_page.wait = WebDriverWait(setup_driver, 10)

        cart_page = ShoppingCartPage()
        cart_page.driver = setup_driver
        cart_page.wait = WebDriverWait(setup_driver, 10)

        checkout_page = CheckoutPage()
        checkout_page.driver = setup_driver
        checkout_page.wait = WebDriverWait(setup_driver, 10)

        # Verify that an error message appears, and that it matches the expected error message
        try:
            # Take necessary steps to reach the Checkout: Your Information Page
            inventory_page.add_random_items_to_cart()
            inventory_page.go_to_cart()
            cart_page.cart_checkout()

            # Insert relevant data and Continue to get the error
            checkout_page.perform_checkout(first_name, last_name, postal_code)
            checkout_page.checkout_continue()
            actual_error_message = checkout_page.driver.find_element(By.XPATH,
                                                                     '//*[@id="checkout_info_container"]/div/form'
                                                                     '/div[1]/div[4]')
            assert actual_error_message.is_displayed(), "Error message not displayed."
            assert actual_error_message.text == expected_error_message, "Unexpected error message text."
        except NoSuchElementException:
            pytest.fail("Error message not found.")
