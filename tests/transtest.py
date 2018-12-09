import re
import sys
from web import backend_pytest
import pytest
import eel_for_transcrypt as eel

from hypothesis import given, example
from hypothesis.strategies import text, integers, one_of, booleans, floats, tuples, lists

from web.backend_pytest import InventoryItem

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
    sys.argv = ["transcrypt.py", "-e", "6", "-b", "./web/tests.py", "-n"]
    sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    transpile()

@pytest.fixture
def build_send_getback_a_dataclass(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import build_send_getback_a_dataclass
    start(selenium)
    return build_send_getback_a_dataclass

@pytest.fixture
def accept_a_dataclass(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import accept_a_dataclass
    start(selenium)
    return accept_a_dataclass

@pytest.fixture
def get_a_dataclass(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import get_a_dataclass
    start(selenium)
    return get_a_dataclass

@pytest.fixture
def identity_js(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import identity_js
    start(selenium)
    return identity_js

@pytest.fixture
def call_a_python_generator_from_js(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import call_a_python_generator_from_js
    start(selenium)
    return call_a_python_generator_from_js

@pytest.fixture
def transcrypt_generator(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import transcrypt_generator
    start(selenium)
    return transcrypt_generator

@pytest.fixture
def identity_py(transpiled_file, selenium):
    with eel.import_frontend_functions():
        from web.tests import identity_caller
    start(selenium)
    return identity_caller

def start(selenium, block=False, webpath="web", alive=False):
    eel.init(webpath, search_exposed_js=False, search_into_imports=True)  # Give folder containing web files
    eel.set_timeouts(1)
    eel.register_frontend_js_files(["./web/__target__/tests.js"])
    eel.register_backend_names(["test_web", "backend_pytest", "transtest"])
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
    start(selenium, block=False, webpath="web", alive=True)
    
    
def wait_for_value1(selenium):
    try:
        selenium.find_element_by_name("value_1")
        return True
    except:
        return False

#lists, sets, tuples,
@given(s=one_of(text(), integers(max_value=1_000_000_000),
                booleans(), floats(max_value=1_000_000_000, min_value=-1_000_000_000)
                ))
def test_identity_simple_types_strategy(s, identity_js):
    v = identity_js(s)()
    assert v== s


@given(s=tuples(text(), integers(max_value=1_000_000_000), text(), text()))
@example(s=("", 1000000000, '0', ''))
def test_identity_collections(s, identity_js):
    assert identity_js(s)() == list(s)
    assert identity_js(list(s))() == list(s)
    d = {s[0]: s[1], s[2]: s[3]}
    i = identity_js(d)()
    assert i == d


def test_identity_simple_types(identity_js):
    assert identity_js(0)() is 0
    assert identity_js(False)() is False
    assert identity_js(True)() is True
    assert identity_js({"a": "b", "c": "d"})() == {"a": "b", "c": "d"}

def test_identity_caller(identity_py):
    assert identity_py(0)() is 0
    assert identity_py(False)() is False
    assert identity_py(True)() is True
    assert identity_py({"a": "b", "c": "d"})() == {"a": "b", "c": "d"}

@given(s=one_of(text(), integers(max_value=1_000_000_000),
                booleans(), floats(max_value=1_000_000_000, min_value=-1_000_000_000)
                ))
def test_identity_simple_types_strategy_py(s, identity_py):
    assert identity_py(s)() == s


@given(s=tuples(text(), integers(max_value=1_000_000_000), text(), text()))
@example(s=("", 1000000000, '0', ''))
def test_identity_collections_py(s, identity_py):
    assert identity_py(s)() == list(s)
    assert identity_py(list(s))() == list(s)
    d = {s[0]: s[1], s[2]: s[3]}
    i = identity_py(d)()
    assert i == d


def test_transcrypt_generator(transcrypt_generator):
    vals = transcrypt_generator(mn=0, mx=10)()
    assert list(vals) == list(range(0, 10))

def test_python_generator(call_a_python_generator_from_js):
    vals = call_a_python_generator_from_js(mn=0, mx=10)()
    assert list(vals) == list(range(0, 10))

def test_transcrypt_generator_single_val(transcrypt_generator):
    vals = transcrypt_generator(mn=0, mx=1)()
    assert list(vals) == list(range(0, 1))

def test_python_generator_single_val(call_a_python_generator_from_js):
    vals = call_a_python_generator_from_js(mn=0, mx=1)()
    assert list(vals) == list(range(0, 1))

@given(s=tuples(text(), floats(max_value=1_000_000_000, min_value=-1_000_000_000), integers(max_value=1_000_000_000)))
def test_spike_dataclass(s, get_a_dataclass, build_send_getback_a_dataclass, accept_a_dataclass):
    v1 = InventoryItem(*s)
    val1 = v1.compute()
    v = get_a_dataclass(*s)()
    v2 = backend_pytest.InventoryItem(**v)
    val2 = v2.compute()
    v3_temp = build_send_getback_a_dataclass(**v)()
    v3 = backend_pytest.InventoryItem(**v3_temp)
    v4_temp = accept_a_dataclass(v)()
    v4 = backend_pytest.InventoryItem(**v4_temp)
    assert v1 == v2
    assert v2 == v3
    assert v3 == v4
    assert val1 == pytest.approx(val2, 0.1)


def test_not_too_sluggish_js_function(transpiled_file, selenium):
    start(selenium)
    eel.set_timeouts(1)
    eel.set_timeout_js(2)
    with eel.import_frontend_functions():
        from web.tests import sluggish
    val = sluggish(1.5)()
    assert val is True


    eel.set_timeout_js(1)
    with eel.import_frontend_functions():
        from web.tests import sluggish
    val = sluggish(0.5)()
    assert val is True


def test_too_sluggish_js_function(transpiled_file, selenium):
    start(selenium)
    eel.set_timeouts(1)
    eel.set_timeout_js(1)
    with eel.import_frontend_functions():
        from web.tests import sluggish
    val = sluggish(1.5)()
    assert val is None
    
    
    eel.set_timeout_js(0.2)
    with eel.import_frontend_functions():
        from web.tests import sluggish
    val = sluggish(0.5)()
    assert val is None
