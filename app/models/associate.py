from dataclasses import dataclass
from datetime import time
from typing import List

@dataclass
class AvailabilityBlock:
    start: time
    end: time

@dataclass
class Associate:
    name: str
    bagging_times: List[AvailabilityBlock]
