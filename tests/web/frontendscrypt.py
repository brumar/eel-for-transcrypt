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
with eel.import_backend_modules(already_imported=True):
    from web import backendcalc

#with eel.import_backend_modules(fake=False):
#    from sources import  anotherbackend
__pragma__("noskip")


async def frontcompute():
    a = document.getElementsByName("value_1")[0].value
    b = document.getElementsByName("value_2")[0].value
    v = await backendcalc.compute(a, b)()
    console.log(v)
    document.getElementById("result").innerHTML = v


def logdone():
    alert("this has been logged")



class SharedState:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

myvar = "hello"

def show_previous_results(lines):
    el = document.getElementById("previous")
    el.innerHTML = "<br/>".join(lines)
document.addEventListener("DOMContentLoaded", lambda e: backend.showpreviousvalues())

