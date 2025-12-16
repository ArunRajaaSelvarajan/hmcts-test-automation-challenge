Feature: Product catalog enhancements
  As a user
  I want richer coverage of the product grid interactions
  So that the catalog remains filterable, sortable and visually correct

  # Planned scenarios for future automation (kept as comments to avoid execution)

  # @todo @product_search Scenario: Search results reflect entered keywords
  #   When I search for "iphone"
  #   Then only products matching "iphone" should be listed
  #
  # @todo @product_vendor_filter Scenario: Filtering by vendor updates the product list
  #   When I filter products by vendor "Apple"
  #   Then only Apple items should be displayed in the grid
  #
  # @todo @product_sort Scenario Outline: Sorting products updates the price order
  #   When I sort products "<direction>"
  #   Then product tiles should appear in "<direction>" order based on price
  #
  #   Examples:
  #     | direction            |
  #     | high to low          |
  #     | low to high          |
  #
  # @todo @product_favorites Scenario: Marking an item as favourite shows it in favourites panel
  #   When I favourite the "Galaxy S20 Ultra"
  #   Then it should appear in the favourites section
  #
  # @todo @product_images Scenario: Product thumbnails should load successfully
  #   Then every product card image should be displayed without broken placeholders
