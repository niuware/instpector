import configparser
import atexit
import pytest
from instpector import Instpector

CONFIG = configparser.ConfigParser()
CONFIG.read("tests/pytest.ini")

INSTANCE = Instpector()
USERNAME = CONFIG["account"]["username"]
INSTANCE.login(user=USERNAME, password=CONFIG["account"]["password"])

def on_finish():
    if INSTANCE:
        INSTANCE.logout()

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)

@pytest.fixture
def base_url():
    return "https://www.instagram.com"

@pytest.fixture
def instance():
    return INSTANCE

@pytest.fixture
def username():
    return USERNAME

atexit.register(on_finish)
