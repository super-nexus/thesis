import pytest
import os

def pytest_addoption(parser):
    parser.addoption("--config", action="store", help="mobile config file")
    parser.addoption("--app", action="store", help="application name")


def pytest_configure(config):
    pytest.config_name = config.getoption('config')
    pytest.app_name = config.getoption('app')


def pytest_logger_config(logger_config):
    logger_config.add_loggers(['main_logger'], stdout_level='info')
    logger_config.set_log_option_default('main_logger')


def pytest_logger_logdirlink(config):
    return os.path.join(os.path.dirname(__file__), 'mylogs')

