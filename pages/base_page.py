"""
Base page object used by all concrete page classes.

This module provides simple helper methods for interacting with the browser
in a safe and consistent way. It keeps low-level WebDriver calls in one place.
"""

from selenium.common import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger


class ElementInteractionError(Exception):
    """Raised when Selenium fails to interact with an element."""


class BasePage:
    """
    Common functionality shared by all page objects.

    Each page object holds a reference to the WebDriver instance and a
    WebDriverWait helper to perform synchronised actions on the UI.
    """
    logger = get_logger(__name__)

    def __init__(self, driver, timeout: int = 5, poll_frequency: float = 0.2):
        """
        Initialise the page object.

        Args:
            driver: Selenium WebDriver instance controlling the browser.
            timeout: Default timeout (in seconds) for explicit waits.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout, poll_frequency)

    def open(self, url: str):
        """
        Navigate the browser to the given URL.

        Args:
            url: Absolute URL to open in the browser.
        """
        self.driver.get(url)

    def _format_locator(self, locator):
        if isinstance(locator, (list, tuple)) and len(locator) == 2:
            by, value = locator
            return f"{by}={value}"
        return str(locator)

    def click(self, locator, retries: int = 3):
        """
        Click an element once it becomes clickable.

        Args:
            locator: Tuple of (By, locator_string) describing the element.

        Returns:
            The WebElement that was clicked.
        """
        attempt = 0
        while True:
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return element
            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
                ElementNotInteractableException,
            ) as exc:
                attempt += 1
                if attempt > retries:
                    message = f"Failed to click element {self._format_locator(locator)} after {retries} retries: {exc.__class__.__name__}"
                    self.logger.error(message)
                    raise ElementInteractionError(message) from exc
                self.logger.warning("Retrying click for %s (%s)", self._format_locator(
                    locator), exc.__class__.__name__)
            except TimeoutException as exc:
                message = f"Failed to click element {self._format_locator(locator)}: {exc.__class__.__name__}"
                self.logger.error(message)
                raise ElementInteractionError(message) from exc

    def type(self, locator, text: str):
        """
        Clear an input field and type the given text into it.

        Args:
            locator: Tuple of (By, locator_string) describing the element.
            text: Text to send to the element.
        """
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except (StaleElementReferenceException, TimeoutException) as exc:
            message = f"Failed to type into element {self._format_locator(locator)}: {exc.__class__.__name__}"
            self.logger.error(message)
            raise ElementInteractionError(message) from exc

    def get_text(self, locator) -> str:
        """
        Return the visible text for the given element.

        Args:
            locator: Tuple of (By, locator_string) describing the element.

        Returns:
            The text content of the element.
        """
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator))
            return element.text
        except (StaleElementReferenceException, TimeoutException) as exc:
            message = f"Failed to read text from element {self._format_locator(locator)}: {exc.__class__.__name__}"
            self.logger.error(message)
            raise ElementInteractionError(message) from exc

    def get_attribute(self, locator, attribute: str) -> str:
        """
        Return the value of the given attribute for the given element.

        Args:
            locator: Tuple of (By, locator_string) describing the element.
            attribute: Name of the attribute to retrieve.

        Returns:
            The value of the attribute.
        """
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator))
            return element.get_attribute(attribute)
        except (StaleElementReferenceException, TimeoutException) as exc:
            message = (
                f"Failed to read attribute '{attribute}' from element "
                f"{self._format_locator(locator)}: {exc.__class__.__name__}"
            )
            self.logger.error(message)
            raise ElementInteractionError(message) from exc

    def element_visible(self, locator) -> bool:
        """
        Return True if the element exists on the page.

        Args:
            locator: Tuple of (By, locator_string) describing the element.

        Returns:
            True if the element exists, otherwise False.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def find_elements(self, locator):
        """
        Return a list of elements matching the given locator.

        Args:
            locator: Tuple of (By, locator_string) describing the elements.

        Returns:
            List of WebElement objects.
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def get_current_url(self) -> str:
        """
        Return the current URL of the browser.

        Returns:
            The current URL.
        """
        return self.driver.current_url

    def element_present(self, locator):
        """
        Return True if the element is present on the page.

        Args:
            locator: Tuple of (By, locator_string) describing the element.

        Returns:
            True if the element is present, otherwise False.
        """
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
