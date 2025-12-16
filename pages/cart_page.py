from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

class CartPage(BasePage):
    logger = get_logger(__name__)

    SIDE_CART_BUTTON = (By.CSS_SELECTOR, ".bag--float-cart-closed")
    CHECKOUT_BUTTON = (By.XPATH, "//div[text()='Checkout']")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//div[text()='Continue Shopping']")
    SIDE_CART_CLOSE_BUTTON = (By.CSS_SELECTOR, "div[class='float-cart__close-btn']")
    SIDE_CART_SUBTOTAL = (By.CSS_SELECTOR, ".float-cart__footer .sub-price__val")

    def validate_side_cart(self, product_name, product_price):
        self.element_visible(self.SIDE_CART_CLOSE_BUTTON)
        actual_product_name = self.get_text((By.XPATH, f"//div[@class='float-cart__shelf-container']//p[text()='{product_name}']"))
        assert actual_product_name == product_name, f"Expected product name '{product_name}' but got '{actual_product_name}'"
        actual_product_price = self.get_text((By.XPATH, f"//div[@class='float-cart__shelf-container']//p[text()='{product_name}']/../following-sibling::div[@class='shelf-item__price']/p"))
        assert actual_product_price == product_price, f"Expected product price '{product_price}' but got '{actual_product_price}'"

    def validate_subtotal(self):
        price_elements = self.find_elements((By.XPATH,
                                             "//div[@class='float-cart__shelf-container']//p/../following-sibling::div[@class='shelf-item__price']/p"))

        calculated_total = 0.0
        for element in price_elements:
            price_text = element.text
            price_value = float(price_text.replace('$ ', '').strip())
            calculated_total += price_value

        # Get displayed subtotal and compare
        displayed_subtotal = self.get_text(self.SIDE_CART_SUBTOTAL)
        displayed_value = float(displayed_subtotal.replace('$ ', '').strip())

        assert calculated_total == displayed_value, f"Calculated total ${calculated_total} doesn't match displayed ${displayed_value}"
        self.logger.info(f"Subtotal validation passed: ${calculated_total}")

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.logger.info("Proceeding to checkout")

    def navigate_to_side_cart_without_adding_items(self):
        self.click(self.SIDE_CART_BUTTON)
        self.logger.info("Navigated to side cart without adding items")

    def check_presence_of_continue_shopping_button(self):
        self.element_visible(self.CONTINUE_SHOPPING_BUTTON)

    def check_absence_of_side_cart_close_btn(self):
        if not self.element_visible(self.SIDE_CART_CLOSE_BUTTON):
            return True
        else:
            return False

    def close_side_cart(self):
        self.click(self.SIDE_CART_CLOSE_BUTTON)
        self.logger.info("Side cart closed")