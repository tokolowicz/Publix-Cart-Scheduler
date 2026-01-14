from datetime import time

from app.models.associate import Associate, AvailabilityBlock
from app.models.cart_schedule import CartScheduleOutline, CartSlot
from app.scheduler.generator import generate_cart_schedule

if __name__ == "__main__":
    associates = [
        Associate(
            name="Sig",
            bagging_times=[
                AvailabilityBlock(time(11, 15), time(15, 0))
            ]
        ),
        Associate(
            name="Ben",
            bagging_times=[
                AvailabilityBlock(time(7, 0), time(11, 0))
            ]
        ),
        Associate(
            name="Braeden",
            bagging_times=[
                AvailabilityBlock(time(13, 30), time(17, 15))
            ]
        ),
        Associate(
            name="Sarah",
            bagging_times=[
                AvailabilityBlock(time(9, 0), time(13, 30))
            ]
        ),
        Associate(
            name="Andrew",
            bagging_times=[
                AvailabilityBlock(time(9, 0), time(13, 45))
            ]
        ),
        Associate(
            name="Tim",
            bagging_times=[
                AvailabilityBlock(time(12, 15), time(14, 15)),
                AvailabilityBlock(time(18, 15), time(19, 15))
            ]
        ),
        Associate(
            name="Jalis",
            bagging_times=[
                AvailabilityBlock(time(14, 15), time(18, 15))
            ]
        ),
        Associate(
            name="Rilee",
            bagging_times=[
                AvailabilityBlock(time(15, 0), time(15, 30)),
                AvailabilityBlock(time(16, 30), time(18, 0))
            ]
        ),
        Associate(
            name="Bella",
            bagging_times=[
                AvailabilityBlock(time(15, 30), time(15, 45)),
                AvailabilityBlock(time(16, 45), time(18, 45))
            ]
        ),
        Associate(
            name="Ryleigh",
            bagging_times=[
                AvailabilityBlock(time(16, 0), time(16, 45))
            ]
        ),
        Associate(
            name="Bryan",
            bagging_times=[
                AvailabilityBlock(time(14, 15), time(18, 15))
            ]
        ),
        Associate(
            name="Drew",
            bagging_times=[
                AvailabilityBlock(time(19, 45), time(21, 15))
            ]
        ),
        Associate(
            name="Rivers",
            bagging_times=[
                AvailabilityBlock(time(18, 0), time(20, 0))
            ]
        ),
    ]

    outline = CartScheduleOutline(
        increment_minutes=15,
        slots=[
            CartSlot(time(7, 0), 0.5),
            CartSlot(time(7, 30), 0.5),
            CartSlot(time(8, 0), 0.5),
            CartSlot(time(8, 30), 0.5),
            CartSlot(time(9, 0), 0.5),
            CartSlot(time(9, 30), 0.5),
            CartSlot(time(10, 0), 1),
            CartSlot(time(10, 30), 1),
            CartSlot(time(11, 0), 1),
            CartSlot(time(11, 30), 1),
            CartSlot(time(12, 0), 1),
            CartSlot(time(12, 30), 1),
            CartSlot(time(13, 0), 1),
            CartSlot(time(13, 30), 1),
            CartSlot(time(14, 0), 1),
            CartSlot(time(14, 30), 1),
            CartSlot(time(15, 0), 1),
            CartSlot(time(15, 30), 1),
            CartSlot(time(16, 0), 1),
            CartSlot(time(16, 30), 1),
            CartSlot(time(17, 0), 1),
            CartSlot(time(17, 30), 1),
            CartSlot(time(18, 0), 1),
            CartSlot(time(18, 30), 1),
            CartSlot(time(19, 0), 1),
            CartSlot(time(19, 30), 1),
            CartSlot(time(20, 0), 0.5),
            CartSlot(time(20, 30), 0.5)
        ]
    )

    schedule = generate_cart_schedule(associates, outline)
    print(schedule)
