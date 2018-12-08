import re
import sys
from web import backend_pytest
import pytest
import eel_for_transcrypt as eel

from hypothesis import given, example
from hypothesis.strategies import text, integers, one_of, booleans, floats, tuples, lists

from web.imports.ping1 import pingball

web_app_options = {
    "mode": "chromium",  # or "chrome"
    "port": 8000,
    "chromeFlags": [
        "--remote-debugging-port=9222",
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
    sys.argv = ["transcrypt.py", "-e", "6", "-b", "./web/imports/allthepongs.py", "-n"]
    sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    transpile()


def start(selenium, block=False, webpath="web/imports", alive=False):
    eel.init(webpath, search_exposed_js=False, search_into_imports=True)  # Give folder containing web files
    eel.set_timeout(1)
    eel.register_frontend_js_files(["./__target__/allthepongs.js", "./__target__/pong1.js", "./__target__/pong2.js"])
    eel.register_backend_names(["ping1", "ping2"])
    eel.start(
        "index.html",
        size=(300, 200),
        block=block,
        options=web_app_options,
        #callback=restart,
        alive=alive,
    )  # Start
    selenium.get("http://localhost:8000/index.html")


def restart(selenium, page, websockets):
    start(selenium, block=False, webpath="web/imports", alive=True)
    
    
def wait_for_value1(selenium):
    try:
        selenium.find_element_by_name("value_1")
        return True
    except:
        return False

def test_imports(transpiled_file, selenium):
    start(selenium)
    v = pingball(0)
    assert v > 50

@pytest.mark.skip(reason="not working")
def test_already_imported(transpiled_file, selenium):
    with pytest.raises(Exception, match="Already exposed function with name"):
        from web.imports import ping2

def test_already_imported_but_safer(transpiled_file, selenium):
    try:
        with eel.import_backend_modules(already_imported=True):
            import web.imports.ping2
    except:
        pytest.fail("should have been secure")
    assert True


def test_back_uncorrect_imports(transpiled_file, selenium):
    with pytest.raises(Exception, match="You must write your imports under the form 'import x.y.z [as z]"):
        with eel.import_backend_modules(already_imported=True):
            from web.imports.ping1 import pingball

def test_uncorrect_imports_front(transpiled_file, selenium):
    with pytest.raises(Exception, match="You must write your imports under the form 'from x.y import z'"):
        with eel.import_frontend_functions():
            import web.imports.pong2

