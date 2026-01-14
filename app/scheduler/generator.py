from typing import List
from datetime import time

from app.models import (
    Associate,
    CartScheduleOutline,
    GeneratedSchedule,
    AssignedSlot
)
from app.scheduler.availability import is_associate_available
from app.utils.time_utils import add_minutes

def cooldown_satisfied(
    associate: Associate,
    slot_start: time,
    cooldown_minutes: int
) -> bool:
    if associate.last_cart_end is None:
        return True

    allowed_time = add_minutes(
        associate.last_cart_end,
        cooldown_minutes
    )
    return slot_start >= allowed_time

def generate_cart_schedule(
    associates: List[Associate],
    outline: CartScheduleOutline
) -> GeneratedSchedule:

    increment = outline.increment_minutes
    cooldown_minutes = 2 * increment

    # Rotation queue (names)
    rotation = associates.copy()

    generated = GeneratedSchedule(
        increment_minutes=increment
    )

    for slot in outline.slots:
        slot_start = slot.start
        slot_end = add_minutes(slot_start, increment)

        required = int(slot.quantity)
        assigned: List[str] = []

        for _ in range(len(rotation)):
            if len(assigned) >= required:
                break

            associate = rotation.pop(0)

            if not is_associate_available(
                associate, slot_start, slot_end
            ):
                rotation.append(associate)
                continue

            if not cooldown_satisfied(
                associate, slot_start, cooldown_minutes
            ):
                rotation.append(associate)
                continue

            # Assign associate
            assigned.append(associate.name)
            associate.last_cart_end = slot_end
            rotation.append(associate)

        generated.slots.append(
            AssignedSlot(
                start=slot_start,
                associates=assigned
            )
        )

    return generated
