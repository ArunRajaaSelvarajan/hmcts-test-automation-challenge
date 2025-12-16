"""
Shared pytest fixtures and hooks for the UI test suite.

This module provides fixtures for loading configuration and managing the
WebDriver lifecycle. It also captures screenshots for failed tests to aid
debugging and reporting.
"""

import os
from datetime import datetime

import pytest
import yaml

from utils.driver_factory import get_driver

pytest_plugins = ["tests.step_definitions.common_steps"]

# Sample BrowserStack Platform, OS version and browser combinations
BROWSERSTACK_ENVIRONMENTS = [
    {
        "browser_name": "chrome",
        "browser_version": "latest",
        "os_name": "Windows",
        "os_version": "10",
        "session_name": "Chrome on Win 10"
    },
    {
        "browser_name": "firefox",
        "browser_version": "latest",
        "os_name": "OS X",
        "os_version": "Ventura",
        "session_name": "Firefox on Mac"
    }
    # can be extended as per requirement
]


@pytest.fixture(params=BROWSERSTACK_ENVIRONMENTS, scope="session")
def browserstack_config(request):
    """Fixture that yields one configuration dict per test run."""
    return request.param


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Capture test results for use in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_html_report_title(report):
    """Set custom title for HTML report."""
    report.title = "UI Test Report"


def pytest_html_results_table_header(cells):
    """Add screenshot column to HTML report table."""
    cells.insert(2, "<th>Screenshot</th>")


def pytest_html_results_table_row(report, cells):
    """Add screenshot to HTML report table row."""
    if report.failed and hasattr(report, 'screenshot_path'):
        cells.insert(2, f'<td><a href="{report.screenshot_path}" target="_blank">Screenshot</a></td>')
    elif report.failed:
        cells.insert(2, "<td>No screenshot</td>")
    else:
        cells.insert(2, "<td>N/A</td>")


@pytest.fixture(scope="session")
def config():
    """
    Load the test configuration from config.yaml.

    The configuration is shared across the entire test session and contains
    basic runtime settings such as base URL, browser and run mode.

    Returns:
        Dictionary loaded from the YAML configuration file.
    """
    with open("config/config.yaml") as f:
        config_data = yaml.safe_load(f)

    # Allow environment variables to override key runtime settings so Docker/CI
    # pipelines can change behaviour without editing the YAML file.
    overrides = {
        "base_url": os.getenv("BASE_URL"),
        "browser": os.getenv("BROWSER"),
        "run_mode": os.getenv("RUN_MODE"),
        "grid_url": os.getenv("GRID_URL"),
        "implicit_wait": os.getenv("IMPLICIT_WAIT"),
    }

    for key, value in overrides.items():
        if value is None:
            continue
        if key == "implicit_wait":
            config_data[key] = int(value)
        else:
            config_data[key] = value

    return config_data


@pytest.fixture
def driver(config, request):
    """
    Provide a WebDriver instance to each test and handle clean-up.

    The fixture:
    - creates a WebDriver using the driver factory
    - applies implicit wait settings
    - captures a screenshot if the test fails
    - quits the browser when the test is finished

    Args:
        config: Session-level configuration dictionary.
        request: Pytest request object used to inspect the test outcome.

    Yields:
        A Selenium WebDriver instance for use in tests.
    """
    driver = get_driver(config)
    driver.implicitly_wait(config.get("implicit_wait", 10))

    yield driver

    # Screenshot on failure
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/screenshots/{request.node.name}_{timestamp}.png"
        driver.save_screenshot(filename)
        screenshot_relative_path = f"screenshots/{request.node.name}_{timestamp}.png"
        report.screenshot_path = screenshot_relative_path

    driver.quit()
