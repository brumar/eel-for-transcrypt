import eel_for_transcrypt as eel

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

def restart(page, websockets):
    start(block=False, webpath="web", alive=True)


def start(block=True, webpath="web", alive=False):
    eel.init(webpath, search_exposed_js=False, search_into_imports=True)  # Give folder containing web files
    eel.register_backend_names(["backend", "anotherbackend"])  # SOOOON
    eel.register_frontend_js_files(["web/__target__/frontendscrypt.js", "web/__target__/anotherfrontend.js"])  # SOON TWO
    eel.start(
        "additions_diary.html",
        size=(300, 200),
        block=block,
        options=web_app_options,
        callback=restart,
        alive=alive,
    )  # Start
