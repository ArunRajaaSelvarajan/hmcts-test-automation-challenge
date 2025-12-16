import os
from pathlib import Path

from axe_selenium_python import Axe
from pytest_bdd import given, when, then, parsers
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.confirmation_page import ConfirmationPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


@given("I am on the bstackdemo homepage")
def open_home(driver, config):
    """Navigate to the application home page."""
    LoginPage(driver).open_home(config["base_url"])


@given("I click on Sign In link")
@when("I click on Sign In link")
def click_sign_in(driver):
    """Open the login modal from the home page header."""
    LoginPage(driver).open_login_panel()


@when(parsers.parse('I log in with valid username "{username}" and password "{password}"'))
def login_with_credentials(driver, username, password):
    """Log in using the provided username and password."""
    LoginPage(driver).login_with_valid_credentials(username, password)


@when("I try log in without entering credentials")
def login_without_credentials(driver):
    """Attempt to log in without populating the username/password fields."""
    LoginPage(driver).login_without_credentials()


@when(parsers.parse('I add "{product_name}" to the cart'))
def add_product_to_cart(driver, product_name):
    """Add a product to the cart from the product page."""
    ProductPage(driver).add_product_to_cart(product_name)


@then(parsers.parse('I see the side cart opens automatically with added "{product_name}" along with its "{product_price}"'))
def validate_side_cart(driver, product_name, product_price):
    """Check the side cart for the recently added item."""
    page = CartPage(driver)
    page.validate_side_cart(product_name, product_price)
    page.logger.info(
        f"Side cart opened with {product_name} and {product_price}")


@then("I should see the subtotal displayed correctly")
def validate_subtotal(driver):
    """Verify the subtotal displayed in the side cart."""
    CartPage(driver).validate_subtotal()


@when("I proceed to the checkout page")
def proceed_to_checkout(driver):
    """Navigate from the cart to the checkout page."""
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()
    cart_page.logger.info("Proceeding to checkout page")


@then("I should be on the checkout page")
def verify_checkout_page(driver):
    """Confirm that the checkout page is displayed."""
    checkout_page = CheckoutPage(driver)
    assert checkout_page.verify_checkout_page(), "Checkout page was not loaded"
    checkout_page.logger.info("Verified checkout page")


@then(parsers.parse('I should see "{product_name}" and its "{product_price}" in the order summary'))
def verify_product_in_order_summary(driver, product_name, product_price):
    """Verify that a product is listed in the checkout order summary."""
    checkout_page = CheckoutPage(driver)
    assert checkout_page.verify_product_in_order_summary(
        product_name, product_price
    ), f"{product_name} was not found in the order summary"
    checkout_page.logger.info(
        f"Verified the product '{product_name}' with its '{product_price}' was found in the order summary"
    )


@then("I should see total updated correctly in the order summary")
def order_summary_total_check(driver):
    """Validate the grand total in the order summary."""
    checkout_page = CheckoutPage(driver)
    assert checkout_page.check_order_summary_total(), "Order summary total is not correct"
    checkout_page.logger.info("Order summary total is correct")


@when(
    parsers.parse(
        'I enter checkout details "{first_name}", "{last_name}", "{address}", "{state_or_province}", "{postcode}"'
    )
)
def enter_checkout_details(driver, first_name, last_name, address, state_or_province, postcode):
    """Fill the checkout form using data from the scenario outline."""
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_checkout_form(
        first_name=first_name,
        last_name=last_name,
        address=address,
        state_or_province=state_or_province,
        postcode=postcode,
    )
    checkout_page.logger.info("Entered checkout details")


@when("I submit the order")
def submit_the_order(driver):
    """Place the order from the checkout page."""
    CheckoutPage(driver).place_order()


@then("I should see an order confirmation message")
def verify_order_confirmation(driver):
    """Validate the confirmation banner after placing an order."""
    confirmation_page = ConfirmationPage(driver)
    expected_confirmation_message = "Your Order has been successfully placed."
    actual_confirmation_message = confirmation_page.get_confirmation_message()
    assert actual_confirmation_message == expected_confirmation_message, "Order confirmation message not found"
    confirmation_page.logger.info("Verified order confirmation message")


@when("I navigate to the side cart adding any items")
def navigate_to_side_cart_without_adding_items(driver):
    """Open the side cart without adding products to it."""
    cart_page = CartPage(driver)
    cart_page.navigate_to_side_cart_without_adding_items()
    cart_page.logger.info("Navigated to side cart adding items")


@then("I should see continue shopping button instead of checkout")
def verify_continue_shopping_button(driver):
    """Ensure the continue shopping button is shown when the cart is empty."""
    cart_page = CartPage(driver)
    cart_page.check_presence_of_continue_shopping_button()
    cart_page.logger.info("Verified continue shopping button")


@then("the page should pass accessibility checks")
def check_accessibility_compliance(driver, request):
    """Run axe-core accessibility scan to ensure the current page has no violations."""
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    violations = results.get("violations", [])

    if violations:
        output_dir = Path("reports/accessibility")
        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / f"{request.node.name}.json"
        axe.write_results(results, str(report_path))
        ids = ", ".join(v.get("id", "unknown") for v in violations)
        raise AssertionError(
            f"Accessibility violations detected: {ids}. See {report_path} for details.")
    

@then("I should logout successfully")
def logout(driver):
    LoginPage(driver).select_logout()
