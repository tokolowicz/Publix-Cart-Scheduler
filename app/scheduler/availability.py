from datetime import time
from app.models.associate import Associate

def is_associate_available(
    associate: Associate,
    slot_start: time,
    slot_end: time
) -> bool:
    for block in associate.bagging_times:
        if block.start <= slot_start and block.end >= slot_end:
            return True
    return False
