from src.swag_labs_functions import SwagLabsFunctions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class InventoryPage(SwagLabsFunctions):
    def get_inventory_items_names(self):
        items_names = []
        for item_name in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name"):
            items_names.append(item_name.text)
        return items_names

    def get_inventory_items_prices(self):
        items_prices = []
        for item_price in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price"):
            only_numbers = item_price.text.replace('$', '')
            items_prices.append(float(only_numbers))
        return items_prices

    def select_sort_type_text(self, sort_type_option):
        sort_type = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        select = Select(sort_type)
        return select.select_by_visible_text(sort_type_option)

    def get_sort_type_text(self):
        sort_type = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        select = Select(sort_type)
        return select.first_selected_option.text

    def logout(self):
        # Open the menu
        menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()

        # Wait until the logout option is clickable, then click it
        logout_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout_option.click()

    def go_to_cart(self):
        cart_button = self.driver.find_element(By.ID, "shopping_cart_container")
        cart_button.click()

    def reset_app_state(self):
        menu_button = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        reset_option = self.driver.find_element(By.ID, "reset_sidebar_link")
        reset_option.click()
