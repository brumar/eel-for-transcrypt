# Note that CPython will ignore all pragma's

# __pragma__('skip')
def __pragma__(*args, **kwargs) -> None:
    pass


# __pragma__('noskip')

__pragma__("skip")
import eel
from unittest.mock import MagicMock

document = MagicMock()
# Another deviation from CPython is that the inclusion of a module has to be decided upon compiletime.
# This means that imports cannot be runtime conditional, so e.g. cannot be under an if.
# For compiletime conditional imports you can use __pragma__ (‘ifdef’).
# Also, since imports are resolved in one pass, cyclic imports are not supported.
alert = console = print
with eel.import_backend_modules(fake=True):
    import backend
    import anotherbackend
__pragma__("noskip")


def biglogger(val):
    console.log("------")
    console.log(val)
    console.log("------")
