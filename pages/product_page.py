# pages/product_page.py

from selenium.webdriver.common.by import By
from utils.logger import get_logger
from .base_page import BasePage
from .cart_page import CartPage


class ProductPage(BasePage):

    logger = get_logger(__name__)

    def validate_product_listing_page(self):
        """
        Verify that the product listing page is open.
        """
        # Verify that the product listing page is open
        assert self.element_visible(
            (By.XPATH, "//div[@class='shelf-item']")), "Product listing page is not open"

    def add_product_to_cart(self, product_name: str):
        """
        Add a product with the given name to the cart.

        Args:
            product_name: Visible name of the product (e.g. "iPhone 12").
        """
        product_tile = (
            By.XPATH,
            f"//div[@class='shelf-item'][./p[text()='{product_name}']]"
        )
        # The add-to-cart button relative to that tile
        add_button = (
            By.XPATH,
            f"//div[@class='shelf-item']/p[text()='{product_name}']//following-sibling::div[text()='Add to cart']"
        )
        cartPage = CartPage(self.driver)

        if cartPage.check_absence_of_side_cart_close_btn():
            self.click(product_tile)
            self.click(add_button)
        else:
            cartPage.close_side_cart()
            self.click(product_tile)
            self.click(add_button)

        self.logger.info(f"Added {product_name} to cart")
