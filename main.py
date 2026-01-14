from datetime import time

from app.models.associate import Associate, AvailabilityBlock
from app.models.cart_schedule import CartScheduleOutline, CartSlot
from app.scheduler.generator import generate_cart_schedule

if __name__ == "__main__":
    associates = [
        Associate(
            name="Alex",
            bagging_times=[
                AvailabilityBlock(time(9, 0), time(11, 0)),
                AvailabilityBlock(time(12, 0), time(16, 0)),
            ]
        ),
        Associate(
            name="Jamie",
            bagging_times=[
                AvailabilityBlock(time(9, 0), time(13, 0)),
            ]
        ),
    ]

    outline = CartScheduleOutline(
        increment_minutes=15,
        slots=[
            CartSlot(time(9, 0), 1),
            CartSlot(time(9, 15), 2),
            CartSlot(time(9, 30), 0.5),
        ]
    )

    schedule = generate_cart_schedule(associates, outline)
    print(schedule)
