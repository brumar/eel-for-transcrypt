import eel_for_transcrypt as eel
from web.common import InventoryItem

@eel.expose
def i_return_the_same(anything):
    return anything

@eel.expose
def a_generator(mn, mx):
    yield from range(mn, mx)
    


@eel.expose
@eel.apply_factories(inputfactory=InventoryItem)
def return_a_dataclass(datac: InventoryItem):
    assert isinstance(datac, InventoryItem)
    return datac
