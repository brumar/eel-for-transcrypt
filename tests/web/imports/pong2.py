# __pragma__('skip')
def __pragma__(*args, **kwargs) -> None:
    pass


# __pragma__('noskip')

__pragma__("skip")
import eel_for_transcrypt as eel
from unittest.mock import MagicMock

document = MagicMock()
# Another deviation from CPython is that the inclusion of a module has to be decided upon compiletime.
# This means that imports cannot be runtime conditional, so e.g. cannot be under an if.
# For compiletime conditional imports you can use __pragma__ (‘ifdef’).
# Also, since imports are resolved in one pass, cyclic imports are not supported.
alert = console = print
with eel.import_backend_modules(already_imported=True):
    import ping1
    import ping2
__pragma__("noskip")

def pingball(counter):
    counter += 1
    return ping2.pingball(counter)