from src.swag_labs_functions import SwagLabsFunctions
from src.src_inventory_page import InventoryPage
from selenium.webdriver.common.by import By


class ShoppingCartPage(SwagLabsFunctions):
    # Make a list of items appearing in the Shopping Cart Page
    def items_in_cart(self):
        cart_items = []
        for item in self.driver.find_elements(By.CLASS_NAME, "cart_item"):
            cart_items.append(item)
        return cart_items

    # Click on the "Continue Shopping" button in the Shopping Cart Page
    def cart_continue_shopping(self):
        continue_shopping_button = self.driver.find_element(By.ID, "continue-shopping")
        return continue_shopping_button.click()

    # Click on the "Checkout" button in the Shopping Cart Page
    def cart_checkout(self):
        checkout_button = self.driver.find_element(By.ID, "checkout")
        return checkout_button.click()
