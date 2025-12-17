Feature: BrowserStack Demo catalog API
  As a developer in test
  I want confidence that the BrowserStack demo APIs stay healthy
  So that UI journeys have dependable backend data

  Background:
    Given the BrowserStack Demo API is reachable

  @api @api_catalog
  Scenario: Product catalog endpoint returns data
    When I request the product catalog
    Then the API response status should be 200
    And the response should contain at least 1 products
    And each product item should include the fields "title, price, description"

  @api @api_login
  Scenario Outline: Valid persona credentials can authenticate via the API
    When I authenticate via the API as "<username>" with password "<password>"
    Then the API response status should be 200

    Examples:
      | username  | password       |
      | demouser  | testingisfun99 |
      | fav_user  | testingisfun99 |
