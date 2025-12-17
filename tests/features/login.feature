Feature: Login
  As a user
  I want to validate correct and incorrect login attempts
  So that I can ensure the login functionality behaves correctly

  Background:
    Given I am on the bstackdemo homepage
    When I click on Sign In link

  @smoke @login @ui_baseline
  Scenario: Login modal displays core UI controls
    Then I should see the login UI controls

  @smoke @regression @login @login_valid
  Scenario Outline: Valid user can log in successfully
    When I log in with valid username "<username>" and password "<password>"
    Then I should see "<expected_header>" in the username header
    And I should logout successfully
#

    Examples:
      | username               | password       | expected_header        |
      | demouser               | testingisfun99 | demouser               |
      | existing_orders_user   | testingisfun99 | existing_orders_user   |
      | fav_user               | testingisfun99 | fav_user               |
      | image_not_loading_user | testingisfun99 | image_not_loading_user |

  @regression @login @login_invalid
  Scenario: Login should fail with invalid or missing credentials
    When I try log in without entering credentials
    Then I should see an error message indicating login failed
    And I should remain on the login page without being logged in

@login @login_accessibility
  Scenario: Login page should pass accessibility checks
    Then the page should pass accessibility checks
