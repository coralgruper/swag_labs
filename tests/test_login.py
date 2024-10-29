# Importing relevant libraries
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from src.src_login_page import LoginPage


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
    yield login
    driver.quit()


# Helper function to perform login
def perform_login(login, username, password):
    login.set_username(username)
    login.set_password(password)
    login.login_button()


# Test for a successful login with multiple accepted users
@pytest.mark.parametrize(
    "username, password",
    [
        ('standard_user', 'secret_sauce'),
        ('problem_user', 'secret_sauce'),
        ('error_user', 'secret_sauce'),
    ]
)
def test_standard_user_login(setup_driver, username, password):
    login = setup_driver
    perform_login(login, username, password)  # Use helper function

    # Verify the user is redirected to the inventory page (the main page)
    try:
        inventory = login.driver.find_element(By.ID, "inventory_container")
        assert inventory.is_displayed(), "Standard user login failed - Inventory container not found."
    except NoSuchElementException:
        pytest.fail("Standard user login failed - Inventory container not found.")


# Test for a failed login with various user scenarios
@pytest.mark.parametrize(
    "username, password, expected_error_message",
    [
        ('locked_out_user', 'secret_sauce', 'Epic sadface: Sorry, this user has been locked out.'),
        ('non_existing_user', '12345', 'Epic sadface: Username and password do not match any user in this service'),
        ('', '', 'Epic sadface: Username is required'),
        ('standard_user', '', 'Epic sadface: Password is required'),
    ]
)
def test_failed_login(setup_driver, username, password, expected_error_message):
    login = setup_driver
    perform_login(login, username, password)  # Use helper function

    # Verify that an error message appears, and that it matches the expected error message
    try:
        actual_error_message = login.driver.find_element(By.XPATH,
                                                         '//*[@id="login_button_container"]/div/form/div[3]/h3')
        assert actual_error_message.is_displayed(), "Error message not displayed."
        assert actual_error_message.text == expected_error_message, "Unexpected error message text."
    except NoSuchElementException:
        pytest.fail("Error message not found.")
