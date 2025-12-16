Feature: Checkout
  As a user
  I want to review my order and complete checkout
  So that I can ensure the checkout flow behaves correctly

  Background:
    Given I am on the bstackdemo homepage
    And I click on Sign In link

  @smoke @regression @checkout @checkout_single_cart
  Scenario Outline: User can add one product to cart, validate cart
    When I log in with valid username "<username>" and password "<password>"
    And I add "<product_name>" to the cart
    Then I see the side cart opens automatically with added "<product_name>" along with its "<product_price>"
    And I should see the subtotal displayed correctly
    When I proceed to the checkout page
    Then I should be on the checkout page


    Examples:
      | username  | password        | product_name       | product_price |
      | demouser  | testingisfun99  | iPhone 12          | $ 799.00      |
      | fav_user  | testingisfun99  | Galaxy S20 Ultra   | $ 1399.00     |

  @regression @checkout @checkout_shipping_details
  Scenario Outline: User can add one product to cart, validate cart, complete checkout and place the order
    When I log in with valid username "<username>" and password "<password>"
    And I add "<product_name>" to the cart
    And I proceed to the checkout page
    Then I should see "<product_name>" and its "<product_price>" in the order summary
    When I enter checkout details "<first_name>", "<last_name>", "<address>", "<state_or_province>", "<postcode>"

    Examples:
      | username  | password        | product_name      | product_price | first_name | last_name | address          | state_or_province | postcode |
      | demouser  | testingisfun99  | iPhone 12         | $ 799.00      | Arun       | Selvarajan | 10 Demo Street   | Cambridgeshire    | CB1 2AB |
      | fav_user  | testingisfun99  | Galaxy S20 Ultra  | $ 1399.00     | John       | Doe        | 22 Sample Road   | Hertfordshire     | HP2 1XY |


  @regression @checkout @checkout_empty_cart
  Scenario Outline: User cannot check out with an empty cart
    When I log in with valid username "<username>" and password "<password>"
    And I navigate to the side cart adding any items
    Then I should see continue shopping button instead of checkout

    Examples:
      | username  | password        |
      | demouser  | testingisfun99  |
      | fav_user  | testingisfun99  |

  # Planned checkout validations (commented for future implementation)
  # @todo @checkout_validation Scenario: Required checkout fields prompt inline errors
  #   When I submit the checkout form without filling mandatory fields
  #   Then inline validation messages should appear for each missing value
  #
  # @todo @checkout_invalid_postcode Scenario: Invalid postcode shows validation error
  #   When I enter an invalid postcode
  #   Then the postcode field should display an appropriate error
  #
  # @todo @checkout_images Scenario: Selected product image is shown during review
  #   Then the checkout summary should display the thumbnail for each selected product
