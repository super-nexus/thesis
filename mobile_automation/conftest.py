import pytest


def pytest_addoption(parser):
    parser.addoption("--config", action="store", help="mobile config file")
    parser.addoption("--app", action="store", help="application name")


def pytest_configure(config):
    pytest.config_name = config.getoption('config')
    pytest.app_name = config.getoption('app')


