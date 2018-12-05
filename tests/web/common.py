from dataclasses import dataclass


@dataclass
class InventoryItem:
    nam: str = "val"
    unit_price: float = 0.5
    quantity_on_hand: int = 0
    
    def compute(self):
        return self.unit_price * self.quantity_on_hand
