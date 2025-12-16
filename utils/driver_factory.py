"""
Simple driver factory responsible for creating WebDriver instances.

This module provides a clean interface for starting Chrome or Firefox in both
headed and headless modes. The goal is to keep WebDriver initialisation
isolated so that page objects and tests remain focused on behaviour.
"""
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException, JavascriptException


def get_local_driver(browser_name: str):
    """
    Create and return a WebDriver instance for the given browser.

    Supported values for browser_name:
        - "chrome"
        - "firefox"
        - "chrome-headless"
        - "firefox-headless"

    Returns:
        A configured Selenium WebDriver instance.

    Raises:
        ValueError: If an unsupported browser name is provided.
    """
    os_name = platform.system().lower()
    name = browser_name.lower()

    is_headless = "headless" in name
    is_chrome = name.startswith("chrome")
    is_firefox = name.startswith("firefox")

    # Chrome driver setup
    if is_chrome:
        chrome_options = ChromeOptions()

        if is_headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1600,1000")
        else:
            chrome_options.add_argument("--start-maximized")

        # Stable CI/CD options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        if os_name == "linux":
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )


        if not is_headless:
            try:
                driver.maximize_window()  # Try first for Windows / Linux
                print("Maximized window using maximize_window()")
            except WebDriverException:
                pass

        return driver

    # Firefox driver setup
    elif is_firefox:
        firefox_options = FirefoxOptions()

        if is_headless:
            firefox_options.add_argument("--headless")
            # explicit headless viewport
            firefox_options.add_argument("--width=1600")
            firefox_options.add_argument("--height=1000")

        # CI/CD safe flags
        firefox_options.set_preference("dom.disable_beforeunload", True)
        firefox_options.set_preference("dom.popup_maximum", 0)
        firefox_options.set_preference("privacy.trackingprotection.enabled", False)

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )

        if not is_headless:
            try:
                screen_width = driver.execute_script("return screen.width")
                screen_height = driver.execute_script("return screen.height")
                driver.set_window_size(screen_width, screen_height)
                print("Maximized window using JavaScript")
            except (JavascriptException, WebDriverException):
                pass

        return driver

    else:
        raise ValueError(
            "Unsupported browser. Use: chrome, firefox, chrome-headless, or firefox-headless.")


def get_grid_driver(config: dict):
    """
    Create a remote WebDriver instance that targets a Selenium Grid.

    The grid URL can be supplied via the configuration file or the GRID_URL
    environment variable. Browsers are selected using the same `browser`
    property as local runs, allowing a single toggle between environments.
    """
    grid_url = config.get("grid_url") or os.getenv("GRID_URL")
    if not grid_url:
        raise RuntimeError(
            "GRID_URL must be configured when run_mode is set to 'grid'."
        )

    browser_name = (config.get("browser") or "chrome").lower()

    if "chrome" in browser_name:
        options = webdriver.ChromeOptions()
        if "-headless" in browser_name:
            options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        return webdriver.Remote(command_executor=grid_url, options=options)

    if "firefox" in browser_name:
        options = webdriver.FirefoxOptions()
        if "-headless" in browser_name:
            options.add_argument("-headless")
        return webdriver.Remote(command_executor=grid_url, options=options)

    raise Exception(
        "Unsupported browser for grid execution. "
        "Valid options: chrome, firefox, chrome-headless, firefox-headless."
    )


def get_browserstack_driver(browserstack_config):
    """
    Create a remote WebDriver instance for BrowserStack.

    This function expects BrowserStack credentials to be provided via
    environment variables and uses a minimal set of capabilities suitable
    for running demo tests in the cloud.

    Required environment variables:
        BROWSERSTACK_USERNAME
        BROWSERSTACK_ACCESS_KEY

    Args:
        config: Loaded configuration dictionary which may include browser
                name and other runtime options.

    Returns:
        A remote Selenium WebDriver instance pointing to BrowserStack.

    Raises:
        RuntimeError: If the BrowserStack credentials are not available.
    """
    user = os.getenv("BROWSERSTACK_USERNAME")
    key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    if not user or not key:
        raise EnvironmentError(
            "BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY must be set "
            "to run tests in BrowserStack."
        )

    remote_url = f"https://{user}:{key}@hub-cloud.browserstack.com/wd/hub"

    capabilities = {
        "browserName": browserstack_config["browser_name"],
        "browserVersion": browserstack_config["browser_version"],
        "bstack:options": {
            "os": browserstack_config["os_name"],
            "osVersion": browserstack_config["os_version"],
            "sessionName": browserstack_config["session_name"],
            "buildName": "Pytest BDD Parametrized Build",
        },
    }

    browser_name = browserstack_config["browser_name"].lower()
    if browser_name == "firefox":
        options = FirefoxOptions()
    else:
        options = ChromeOptions()

    for key, value in capabilities.items():
        options.set_capability(key, value)

    return webdriver.Remote(
        command_executor=remote_url,
        options=options
    )


def get_driver(config: dict):
    """
    Return a WebDriver instance based on the runtime configuration.

    The decision whether to run locally or in BrowserStack is driven by the
    `run_mode` value in the config. If no value is provided, local execution
    is used by default.

    Example config keys:
        run_mode: "local" or "browserstack"
        browser: "chrome", "firefox", ...

    Args:
        config: Loaded configuration dictionary.

    Returns:
        A Selenium WebDriver instance ready for test execution.
    """
    run_mode = (config.get("run_mode") or "local").lower()
    browser = config.get("browser", "chrome")

    if run_mode == "browserstack":
        return get_browserstack_driver(config)
    if run_mode == "grid":
        return get_grid_driver(config)

    return get_local_driver(browser)
