from pytest_bdd import scenarios, then, parsers
from pages.login_page import LoginPage

scenarios("../features/login.feature")

@then("I should see an error message indicating login failed")
def verify_login_failure(driver):
    page = LoginPage(driver)
    error_message = page.get_login_error_message()
    assert error_message == "Invalid Username", f"Expected: Invalid Username, Actual: {error_message}"
    page.logger.info(f"Login error message validated successfully")

@then(parsers.parse('I should see "{expected_header}" in the username header'))
def verify_username(driver, expected_header):
    page = LoginPage(driver)
    username = page.get_logged_in_username()
    assert expected_header==username, f"Expected: {expected_header}, Actual: {username}"
    page.logger.info(f"Username header validated successfully")

@then("I should remain on the login page without being logged in")
def verify_login_page(driver):
    page = LoginPage(driver)
    if page.verify_login_page():
        page.logger.info(f"User is on login page")
    else:
        assert False, "User is not on login page"
