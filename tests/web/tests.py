

#__pragma__("skip")
__pragma__ = lambda *args: None
import eel
with eel.import_backend_modules(already_imported=False):
    from web import backend_pytest
#__pragma__("noskip")

from dataclasses import dataclass

#@dataclass
#class InventoryItem:
#    nam: str = "val"
#    unit_price: float = 0.5
#    quantity_on_hand: int = 0
from web.common import InventoryItem

def applyfact(inputfactory=None, outputfactory=None):
    def applyfact_inside(func):
        __pragma__("kwargs")
        def newfunction(*args, **kwargs):
            if inputfactory is not None:
                if outputfactory is not None:
                    return outputfactory(func(inputfactory(*args, **kwargs)))
                else:
                    return func(inputfactory(*args, **kwargs))
            else:
                if outputfactory is not None:
                    try:
                        outputfactory(func(**args[0][0]))
                    except:
                        return outputfactory(func(*args, **kwargs))
                else:
                    return func(*args, **kwargs)
        return newfunction
        #def f(*args, **kwargs):
        #    return func(*args, **kwargs)
        #f.__name__ = func.__name__
        #return f
        __pragma__("nokwargs")
    return applyfact_inside
    

def identity_js(anything):
    return anything

async def identity_caller(anything):
    v = await backend_pytest.i_return_the_same(anything)()
    return v


def transcrypt_generator(mn, mx):
    # NOTE : kwargs not working
    #console.log(mn, mx)
    for v in range(mn, mx):
        yield v
    #v = list(eel.a_generator(mn, mx)())
    #return y

async def call_a_python_generator_from_js(mn, mx):
    v = await backend_pytest.a_generator(mn, mx)()
    return v

@applyfact(outputfactory=InventoryItem)
async def get_a_dataclass(strg, flt, intval):
    d = await backend_pytest.return_a_dataclass(strg, flt, intval)()
    return d
__pragma__("js", {},'Object.defineProperty(get_a_dataclass, "name", { value: "get_a_dataclass" });')

@applyfact(outputfactory=InventoryItem)
async def build_send_getback_a_dataclass(strg, flt, intval):
    dc = InventoryItem(strg, flt, intval)
    d = await backend_pytest.return_a_dataclass(dc)()
    return d
__pragma__("js", {},'Object.defineProperty(build_send_getback_a_dataclass, "name", { value: "build_send_getback_a_dataclass" });')

__pragma__("kwargs")
@applyfact(outputfactory=InventoryItem)
async def accept_a_dataclass(*args, **kwargs):
    dc = args[0]
    d = await backend_pytest.return_a_dataclass(dc)()
    return d
__pragma__("nokwargs")
__pragma__("js", {},'Object.defineProperty(accept_a_dataclass, "name", { value: "accept_a_dataclass" });')
