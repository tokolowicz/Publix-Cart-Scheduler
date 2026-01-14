from dataclasses import dataclass, field
from datetime import time
from typing import List

@dataclass
class AssignedSlot:
    start: time
    associates: List[str]

@dataclass
class GeneratedSchedule:
    increment_minutes: int
    slots: List[AssignedSlot] = field(default_factory=list)
