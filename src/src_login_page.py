from src.swag_labs_functions import SwagLabsFunctions
from selenium.webdriver.common.by import By


class LoginPage(SwagLabsFunctions):
    def set_username(self, username):
        username_bar = self.driver.find_element(By.ID, "user-name")
        username_bar.send_keys(username)

    def set_password(self, password):
        password_bar = self.driver.find_element(By.ID, "password")
        password_bar.send_keys(password)

    def login_button(self):
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
