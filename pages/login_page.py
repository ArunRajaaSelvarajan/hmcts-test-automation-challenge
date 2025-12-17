"""
Page object for handling login behaviour on bstackdemo.

Although the demo site uses dropdowns for username and password, this page
object hides those details behind simple methods so that tests read clearly.
"""

from selenium.webdriver.common.by import By
from utils.logger import get_logger
from .base_page import BasePage


class LoginPage(BasePage):
    """
    Page object representing the login area on the bstackdemo homepage.
    """
    logger = get_logger(__name__)

    SIGN_IN_BUTTON = (By.ID, "signin")
    LOGOUT_LINK = (By.XPATH, "//span[contains(text(), 'Logout')]")
    HEADER_LOGO = (By.XPATH, "//div[contains(@class,'justify-center')]")
    USERNAME_DROPDOWN = (By.XPATH, "//div[contains(text(),'Select Username')]")
    PASSWORD_DROPDOWN = (By.XPATH, "//div[contains(text(),'Select Password')]")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".api-error")
    USER_GREETING = (By.CSS_SELECTOR, ".username")

    def open_home(self, base_url: str):
        """Open the bstackdemo homepage."""
        self.open(base_url)

    def open_login_panel(self):
        """Open the login panel from the homepage."""
        self.click(self.SIGN_IN_BUTTON)

    def select_logout(self):
        """Selects Log out link"""
        self.click(self.LOGOUT_LINK)

    def select_username(self, username: str):
        """Select a username from the dropdown based on visible text."""
        option = (
            By.XPATH,
            f"//div[@id='username']//div[contains(text(),'{username}')]",
        )
        self.click(self.USERNAME_DROPDOWN)
        self.click(option)

    def select_password(self, password: str):
        """Select a password from the dropdown based on visible text."""
        option = (
            By.XPATH,
            f"//div[@id='password']//div[contains(text(),'{password}')]",
        )
        self.click(self.PASSWORD_DROPDOWN)
        self.click(option)

    def login_with_valid_credentials(self, username: str, password: str):
        """
        Perform login with the given username and password values.

        Args:
            username: Username label shown in the dropdown.
            password: Password label shown in the dropdown.
        """
        self.select_username(username)
        self.select_password(password)
        self.click(self.LOGIN_BUTTON)
        self.logger.info(f"Logged in with {username}")

    def get_logged_in_username(self) -> str:
        """Return the username shown in the header once logged in."""
        return self.get_text(self.USER_GREETING)

    def login_without_credentials(self):
        """Perform login without providing any credentials."""
        self.click(self.LOGIN_BUTTON)

    def get_login_error_message(self):
        """Return the error message shown when login fails."""
        return self.get_text(self.ERROR_MESSAGE)

    def verify_login_page(self):
        """Verify that the login page is open."""
        return self.element_visible(self.LOGIN_BUTTON)

    def login_controls_present(self) -> bool:
        """
        Smoke check that the modal renders the BrowserStack logo, credential selectors, and CTA.

        Returns:
            True if all required controls are visible; otherwise False.
        """
        locators = [
            self.HEADER_LOGO,
            self.USERNAME_DROPDOWN,
            self.PASSWORD_DROPDOWN,
            self.LOGIN_BUTTON,
        ]
        results = [self.element_visible(locator) for locator in locators]
        self.logger.info("Login UI controls visibility: %s", results)
        return all(results)
