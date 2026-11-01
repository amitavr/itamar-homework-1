"""Part 2, Question D: delay a train from one station onward in its direction.

Approach:
1. For ltr, visit indices from start_station up to the last station.
2. For rtl, visit indices from start_station down to zero.
3. Leave (-1, -1) unchanged, but continue to the remaining stations.
4. Replace each real stop's tuple with (arrival + delay, departure + delay).
   A tuple cannot be edited, so its replacement is stored in the same list.

Inputs: one schedule, a valid starting index, a positive delay, and direction.
Output: no new value; the existing schedule is changed in-place.
Example: delay_train([(0, 5), (10, 15)], 1, 3) changes the last stop to (13, 18).
The default direction is ltr. The starting station is included in the delay.
"""


def delay_train(train_schedule, start_station, delay, direction="ltr"):
    """Shift stopping times from start_station onward in the travel direction."""
    if direction == "ltr":
        station_indices = range(start_station, len(train_schedule))
    else:
        # range excludes its end, so -1 lets this loop include station zero.
        station_indices = range(start_station, -1, -1)

    for station in station_indices:
        stop = train_schedule[station]
        if stop == (-1, -1):
            continue

        # Replace the immutable tuple, not the schedule list itself.
        train_schedule[station] = (stop[0] + delay, stop[1] + delay)