from dataclasses import dataclass, field
from datetime import time
from typing import List

# Adds readability for printout debugging
def format_time(t: time) -> str:
    return t.strftime("%I:%M %p").lstrip("0")

@dataclass
class AssignedSlot:
    start: time
    associates: List[str]

@dataclass
class GeneratedSchedule:
    increment_minutes: int
    slots: List[AssignedSlot] = field(default_factory=list)

    def __str__(self) -> str:
        lines = []
        lines.append(
            f"Cart Schedule (Increment: {self.increment_minutes} minutes)"
        )
        lines.append("-" * 50)

        for slot in self.slots:
            start_str = format_time(slot.start)
            names = ", ".join(slot.associates) if slot.associates else "—"

            lines.append(f"{start_str:<10} | {names}")

        return "\n".join(lines)
