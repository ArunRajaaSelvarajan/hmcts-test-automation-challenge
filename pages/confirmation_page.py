import time

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

class ConfirmationPage(BasePage):

    logger = get_logger(__name__)
    CONFIRMATION_MESSAGE = (By.ID, "confirmation-message")

    def get_confirmation_message(self):
        return self.get_text(self.CONFIRMATION_MESSAGE)

