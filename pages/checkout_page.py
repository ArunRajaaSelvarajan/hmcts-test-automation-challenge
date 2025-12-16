from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

class CheckoutPage(BasePage):

    logger = get_logger(__name__)

    SHIPPING_ADDRESS_HEADING = (By.XPATH, "//div/legend[@data-test='shipping-address-heading']")
    FIRST_NAME_FIELD = (By.ID, "firstNameInput")
    LAST_NAME_FIELD = (By.ID, "lastNameInput")
    ADDRESS_FIELD = (By.ID, "addressLine1Input")
    STATE_FIELD = (By.ID, "provinceInput")
    POSTCODE_FIELD = (By.ID, "postCodeInput")
    SUBMIT_BUTTON = (By.ID, "checkout-shipping-continue")
    TOTAL_AMOUNT = (By.XPATH, "//span[@class='cart-priceItem-value']")


    def verify_checkout_page(self):
        if self.element_visible(self.SHIPPING_ADDRESS_HEADING):
            return True
        else:
            return False

    def verify_product_in_order_summary(self, product_name, product_price):
        actual_product_name = self.get_text((By.XPATH, f"//h5[normalize-space()='{product_name}']"))
        assert actual_product_name == product_name, f"Expected product name '{product_name}' but got '{actual_product_name}'"
        print(f"(//div[@class='product-price optimizedCheckout-contentPrimary'][ancestor::div//h5[normalize-space()='{product_name}']])[1]")
        actual_product_price = self.get_text((By.XPATH, f"//h5[normalize-space()='{product_name}']/parent::div/following-sibling::div/div"))
        print(actual_product_price)
        product_price = product_price.replace(' ', '').replace('.00', '')
        assert actual_product_price == product_price, f"Expected product price '{product_price}' but got '{actual_product_price}'"
        self.logger.info(f"Product '{product_name}' with price '{product_price}' found in order summary")
        return True


    def fill_checkout_form(self, first_name, last_name, address, state_or_province, postcode):
        self.type(self.FIRST_NAME_FIELD, first_name)
        self.type(self.LAST_NAME_FIELD, last_name)
        self.type(self.ADDRESS_FIELD, address)
        self.type(self.STATE_FIELD, state_or_province)
        self.type(self.POSTCODE_FIELD, postcode)

    def place_order(self):
        self.click(self.SUBMIT_BUTTON)


    def check_order_summary_total(self):
        num_items = len(self.find_elements((By.CSS_SELECTOR, "section.cart-section ul li.productList-item")))
        total = 0.0
        for i in range(num_items):
            price_text = self.get_text((By.CSS_SELECTOR, f"section.cart-section ul li.productList-item:nth-child({i+1}) .product-price"))
            price = float(price_text.replace('$', '').strip())
            total += price
            self.logger.info(f"Item {i+1} price: {price}")

        displayed_total = float(self.get_text(self.TOTAL_AMOUNT).replace('$', '').replace('.00', '').strip())
        self.logger.info(f"Displayed total: {displayed_total}")
        assert total == displayed_total, f"Total mismatch: expected {total}, got {displayed_total}"
        self.logger.info(f"Order summary total validated: ${total}")
        return True





