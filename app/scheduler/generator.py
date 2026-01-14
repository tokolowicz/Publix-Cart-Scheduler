from typing import List, Optional, Tuple
from datetime import time

from app.models import (
    Associate,
    CartScheduleOutline,
    GeneratedSchedule,
    AssignedSlot,
    CartSlot,
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
    allowed_time = add_minutes(associate.last_cart_end, cooldown_minutes)
    return slot_start >= allowed_time


def _covering_block_start(
    associate: Associate,
    slot_start: time,
    slot_end: time
) -> Optional[time]:
    for block in associate.bagging_times:
        if block.start <= slot_start and block.end >= slot_end:
            return block.start
    return None


def _promote_newly_available(
    rotation: List[Associate],
    slot_start: time,
    slot_end: time,
    prev_slot_start: Optional[time],
    prev_slot_end: Optional[time],
) -> List[Associate]:
    if prev_slot_start is None or prev_slot_end is None:
        return rotation

    newly_available: List[Associate] = []
    others: List[Associate] = []

    for a in rotation:
        eligible_now = _covering_block_start(a, slot_start, slot_end) is not None
        eligible_prev = _covering_block_start(a, prev_slot_start, prev_slot_end) is not None

        if eligible_now and not eligible_prev:
            newly_available.append(a)
        else:
            others.append(a)

    newly_available.sort(
        key=lambda a: _covering_block_start(a, slot_start, slot_end) or slot_start
    )
    return newly_available + others


def _time_to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute


def _expand_outline_slots_to_increment(
    outline: CartScheduleOutline
) -> List[Tuple[CartSlot, int]]:
    """
    Returns a list of (slot, duration_minutes) that the generator will schedule.

    Rule requested:
    - If increment is 30: do nothing; each slot duration is 30.
    - If increment is 15:
        * For slots with quantity >= 1: split 30-minute printed block into two 15-min slots
          (start and start+15), each inheriting the same quantity.
        * For slots with quantity 0 or 0.5: keep as a single 30-min slot (NO :15/:45 generated).
    """
    inc = outline.increment_minutes
    slots_sorted = sorted(outline.slots, key=lambda s: _time_to_minutes(s.start))

    if inc == 30:
        return [(s, 30) for s in slots_sorted]

    if inc != 15:
        # If you ever support other increments, default each slot to that increment.
        return [(s, inc) for s in slots_sorted]

    expanded: List[Tuple[CartSlot, int]] = []

    for s in slots_sorted:
        if s.quantity >= 1:
            # Split into two 15-min slots
            expanded.append((CartSlot(start=s.start, quantity=s.quantity), 15))

            mid = add_minutes(s.start, 15)
            expanded.append((CartSlot(start=mid, quantity=s.quantity), 15))
        else:
            # Keep 0 or 0.5 as a 30-min interval (no mid-slot)
            expanded.append((CartSlot(start=s.start, quantity=s.quantity), 30))

    expanded.sort(key=lambda pair: _time_to_minutes(pair[0].start))
    return expanded


def generate_cart_schedule(
    associates: List[Associate],
    outline: CartScheduleOutline
) -> GeneratedSchedule:
    increment = outline.increment_minutes
    cooldown_minutes = 2 * increment

    # Internal slots may be mixed-duration when increment=15
    slots_with_duration = _expand_outline_slots_to_increment(outline)

    rotation: List[Associate] = associates.copy()
    generated = GeneratedSchedule(increment_minutes=increment)

    prev_slot_start: Optional[time] = None
    prev_slot_end: Optional[time] = None

    for slot, duration_minutes in slots_with_duration:
        slot_start = slot.start
        slot_end = add_minutes(slot_start, duration_minutes)

        # Promote anyone who just became eligible (based on the actual slot duration)
        rotation = _promote_newly_available(
            rotation=rotation,
            slot_start=slot_start,
            slot_end=slot_end,
            prev_slot_start=prev_slot_start,
            prev_slot_end=prev_slot_end,
        )

        required_full = int(slot.quantity)
        needs_half = abs(slot.quantity - required_full - 0.5) < 1e-9

        assigned_names: List[str] = []

        # If quantity is 0, just record an empty assignment and continue
        if slot.quantity == 0:
            generated.slots.append(
                AssignedSlot(start=slot_start, associates=[])
            )
            prev_slot_start, prev_slot_end = slot_start, slot_end
            continue

        # FULL SLOTS — PASS 1 (STRICT)
        assigned_full: List[Associate] = []
        used_names = set()

        for _ in range(len(rotation)):
            if len(assigned_full) >= required_full:
                break

            associate = rotation.pop(0)

            if not is_associate_available(associate, slot_start, slot_end):
                rotation.append(associate)
                continue

            if not cooldown_satisfied(associate, slot_start, cooldown_minutes):
                rotation.append(associate)
                continue

            assigned_full.append(associate)
            used_names.add(associate.name)
            associate.last_cart_end = slot_end
            rotation.append(associate)

        # FULL SLOTS — PASS 2 (COOLDOWN OVERRIDE)
        if len(assigned_full) < required_full:
            for _ in range(len(rotation)):
                if len(assigned_full) >= required_full:
                    break

                associate = rotation.pop(0)

                if associate.name in used_names:
                    rotation.append(associate)
                    continue

                if not is_associate_available(associate, slot_start, slot_end):
                    rotation.append(associate)
                    continue

                assigned_full.append(associate)
                used_names.add(associate.name)
                associate.last_cart_end = slot_end
                rotation.append(associate)

        assigned_names.extend(a.name for a in assigned_full)

        # HALF SLOT (0.5) — NO COOLDOWN
        if needs_half:
            for _ in range(len(rotation)):
                associate = rotation.pop(0)

                if not is_associate_available(associate, slot_start, slot_end):
                    rotation.append(associate)
                    continue

                assigned_names.append(associate.name)
                rotation.append(associate)
                break

        generated.slots.append(
            AssignedSlot(start=slot_start, associates=assigned_names)
        )

        prev_slot_start, prev_slot_end = slot_start, slot_end

    return generated
