from src.swag_labs_functions import SwagLabsFunctions
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
