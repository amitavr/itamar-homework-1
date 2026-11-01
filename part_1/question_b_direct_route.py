"""Part 1, Question B: decide whether one train offers a direct journey.

Approach:
1. Reject out-of-range indices before reading the schedule.
2. Reject identical stations and stations marked (-1, -1), meaning no stop.
3. Check station order: increasing indices for ltr, decreasing for rtl.
4. Require destination arrival to be at least the origin departure time.

Inputs: one schedule, its direction, and origin/destination station indices.
Output: True if every rule holds, otherwise False. No inputs are changed.
Example: is_direct_route([(0, 5), (20, 25)], 'ltr', 0, 1) returns True.
A train may skip intermediate stations; only the two endpoints must be stops.
"""


def is_direct_route(
    train_schedule, direction, start_station_index, destination_station_index
):
    """Return whether the train can carry a passenger between these stations."""
    # Python accepts negative indices, but the homework does not.
    if not 0 <= start_station_index < len(train_schedule):
        return False
    if not 0 <= destination_station_index < len(train_schedule):
        return False
    if start_station_index == destination_station_index:
        return False

    start_stop = train_schedule[start_station_index]
    destination_stop = train_schedule[destination_station_index]
    if start_stop == (-1, -1) or destination_stop == (-1, -1):
        return False

    # The direction describes index order, not how the times are stored.
    if direction == "ltr":
        if start_station_index > destination_station_index:
            return False
    elif direction == "rtl":
        if start_station_index < destination_station_index:
            return False
    else:
        return False

    # Equal times are valid: a journey is allowed to take zero time units.
    return destination_stop[0] >= start_stop[1]