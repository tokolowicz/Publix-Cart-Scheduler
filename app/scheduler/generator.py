from typing import List
from datetime import time, timedelta, datetime

from app.models.associate import Associate
from app.models.cart_schedule import CartScheduleOutline
from app.models.generated_schedule import GeneratedSchedule, AssignedSlot
from app.scheduler.availability import is_associate_available

def generate_cart_schedule(
    associates: List[Associate],
    outline: CartScheduleOutline
) -> GeneratedSchedule:
    """
    Scheduling logic will be implemented next.
    """
    raise NotImplementedError
