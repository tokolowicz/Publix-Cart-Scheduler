from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional

@dataclass
class AvailabilityBlock:
    start: time
    end: time

@dataclass
class Associate:
    name: str
    bagging_times: List[AvailabilityBlock]
    last_cart_end: Optional[time] = field(default=None)
