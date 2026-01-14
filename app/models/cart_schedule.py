from dataclasses import dataclass, field
from datetime import time
from typing import List

@dataclass
class CartSlot:
    start: time
    quantity: float  # 0, 0.5 (this is for lot/bag intervals), 1, 2, or 3

@dataclass
class CartScheduleOutline:
    increment_minutes: int  # 15 or 30
    slots: List[CartSlot] = field(default_factory=list)
