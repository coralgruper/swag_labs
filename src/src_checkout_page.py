from src.swag_labs_functions import SwagLabsFunctions
from src.src_inventory_page import InventoryPage
from selenium.webdriver.common.by import By


class CheckoutPage(SwagLabsFunctions):
    # Insert Your Information in the Checkout Page
    def set_first_name(self, first_name):
        first_name_bar = self.driver.find_element(By.ID, "first-name")
        return first_name_bar.send_keys(first_name)

    def set_last_name(self, last_name):
        last_name_bar = self.driver.find_element(By.ID, "last-name")
        return last_name_bar.send_keys(last_name)

    def set_postal_code(self, postal_code):
        postal_code_bar = self.driver.find_element(By.ID, "postal-code")
        return postal_code_bar.send_keys(postal_code)

    # Helper function to enter your_information
    def perform_checkout(self, first_name, last_name, postal_code):
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_postal_code(postal_code)

    # Click on the "Cancel" button in the Checkout Page
    def checkout_cancel(self):
        checkout_cancel_button = self.driver.find_element(By.ID, "cancel")
        return checkout_cancel_button.click()

    # Click on the "Continue" button in the Checkout Page
    def checkout_continue(self):
        checkout_continue_button = self.driver.find_element(By.ID, "continue")
        return checkout_continue_button.click()

    # Calculate the total price (before taxes) of the items in the Checkout Page
    def get_total_price(self):
        items_prices = []
        for item_price in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price"):
            only_numbers = item_price.text.replace('$', '')
            items_prices.append(float(only_numbers))
        return sum(items_prices)

    # Click on the "Finish" button in the Checkout Page
    def checkout_finish(self):
        checkout_finish_button = self.driver.find_element(By.ID, "finish")
        return checkout_finish_button.click()


