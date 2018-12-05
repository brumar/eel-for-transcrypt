import re
import sys

import backend
import pytest
import eel
import time


web_app_options = {
    "mode": "chromium",  # or "chrome"
    "port": 8000,
    "chromeFlags": [
        "--start-fullscreen",
        "-disable-application-cache",
        "–media-cache-size=1",
        "--disk-cache-dir=/dev/null",
        "–disk-cache-size=1",
    ],
}

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1024,768")  # hacky fix
    return chrome_options


@pytest.fixture
def transpiled_file():
    from transcrypt.__main__ import main as transpile
    sys.argv = ["transcrypt.py", "-e", "6", "-b", "./web/tests.py", "-n"]
    sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    transpile()


@pytest.fixture
def identity(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import identity_js
    eel.register_frontend_js_files(["./web/__target__/tests.js"])
    eel.register_backend_names(["test_web"])
    start()
    selenium.get("http://localhost:8000/additions_diary.html")
    wait_for(wait_for_value1, selenium, delay=10)
    return identity_js


def start(block=False, webpath="web", alive=False):
    eel.init(webpath, search_exposed_js=False, search_into_imports=True)  # Give folder containing web files
    eel.start(
        "index.html",
        size=(300, 200),
        block=block,
        options=web_app_options,
        callback=restart,
        alive=alive,
    )  # Start

def restart(page, websockets):
    start(block=False, webpath="web", alive=True)
    
    
def wait_for_value1(selenium):
    try:
        selenium.find_element_by_name("value_1")
        return True
    except:
        return False
    
def test_identity(identity):
    j = "string"
    assert identity(j)() == j
    


def wait_for(condition_function, selenium, delay=3):
    start_time = time.time()
    while time.time() < start_time + delay:
        if condition_function(selenium):
            return True
        else:
            time.sleep(0.1)
    raise Exception('Timeout waiting for {}'.format(condition_function.__name__))


def test_interface(selenium):
    backend.start(block=False, webpath="web")
    selenium.get("http://localhost:8000/additions_diary.html")
    wait_for(wait_for_value1, selenium, delay=10)
    selenium.execute_script("document.getElementsByName('value_1')[0].value='6'")
    selenium.execute_script("document.getElementsByName('value_2')[0].value='10'")
    selenium.find_element_by_id("compute").click()
    # time.sleep(4)
    assert "16" in selenium.find_element_by_id("result").get_attribute('innerHTML')
