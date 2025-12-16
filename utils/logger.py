"""
Lightweight logging helper for the test framework.

The goal of this module is to provide a simple logger that can be reused
across page objects and utilities without repeated configuration.
"""

import logging


def get_logger(name: str = "test_logger") -> logging.Logger:
    """
    Return a configured logger instance.

    The logger writes messages to the standard output stream and is intended
    for ad-hoc debugging and traceability when running tests locally or in CI.

    Args:
        name: Name of the logger to create or retrieve.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
