Feature: End to End purchase journeys
  As a user
  I want to complete full purchase journeys from login to order confirmation
  So that I can ensure the end-to-end flow works as expected

  Background:
    Given I am on the bstackdemo homepage
    And I click on Sign In link

  @smoke @regression @e2e @e2e_single_item
  Scenario Outline: User can log in, add a single product and complete a purchase
    When I log in with valid username "<username>" and password "<password>"
    And I add "<product_name>" to the cart
    Then I see the side cart opens automatically with added "<product_name>" along with its "<product_price>"
    And I should see the subtotal displayed correctly
    When I proceed to the checkout page
    Then I should be on the checkout page
    And I should see "<product_name>" and its "<product_price>" in the order summary
    And I should see total updated correctly in the order summary
    When I enter checkout details "<first_name>", "<last_name>", "<address>", "<state_or_province>", "<postcode>"
    And I submit the order
    Then I should see an order confirmation message

    Examples:
      | username | password       | product_name     | product_price | first_name | last_name  | address        | state_or_province | postcode |
      | demouser | testingisfun99 | iPhone 12        | $ 799.00      | Arun       | Selvarajan | 10 Demo Street | Cambridgeshire    | CB1 2AB  |
      | fav_user | testingisfun99 | Galaxy S20 Ultra | $ 1399.00     | John       | Doe        | 22 Sample Road | Hertfordshire     | HP2 1XY  |

  @regression @e2e @e2e_multi_item
  Scenario Outline: User can log in, add multiple products and complete a purchase
    When I log in with valid username "<username>" and password "<password>"
    And I add "<product_name_1>" to the cart
    And I add "<product_name_2>" to the cart
    And I add "<product_name_3>" to the cart
    Then I see the side cart opens automatically with added "<product_name_1>" along with its "<product_price_1>"
    And I see the side cart opens automatically with added "<product_name_2>" along with its "<product_price_2>"
    And I see the side cart opens automatically with added "<product_name_3>" along with its "<product_price_3>"
    And I should see the subtotal displayed correctly
    When I proceed to the checkout page
    Then I should be on the checkout page
    And I should see "<product_name_1>" and its "<product_price_1>" in the order summary
    And I should see "<product_name_2>" and its "<product_price_2>" in the order summary
    And I should see "<product_name_3>" and its "<product_price_3>" in the order summary
    And I should see total updated correctly in the order summary
    When I enter checkout details "<first_name>", "<last_name>", "<address>", "<state_or_province>", "<postcode>"
    And I submit the order
    Then I should see an order confirmation message
  

    Examples:
      | username | password       | product_name_1 | product_name_2 | product_name_3 | product_price_1 | product_price_2 | product_price_3 | first_name | last_name | address        | state_or_province | postcode |
      | fav_user | testingisfun99 | iPhone 12      | Galaxy S10     | Pixel 4        | $ 799.00        | $ 899.00        | $ 899.00        | John       | Doe       | 22 Sample Road | Hertfordshire     | HP2 1XY  |
