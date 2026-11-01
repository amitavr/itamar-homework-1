"""Part 1, Question C: calculate the duration of a possible direct journey.

Approach:
1. Reuse Question B to check all the direct-journey rules.
2. Return -1 if the journey is impossible.
3. Otherwise subtract origin departure from destination arrival.

Inputs: one schedule, its direction, and origin/destination station indices.
Output: an integer duration, or -1. No inputs are changed.
Example: calculate_travel_time([(0, 5), (35, 40)], 'ltr', 0, 1) returns 30.
The import shares the earlier answer; the combined submission needs no imports.
"""

from part_1.question_b_direct_route import is_direct_route


def calculate_travel_time(
    train_schedule, direction, start_station_index, destination_station_index
):
    """Return arrival minus departure for a valid journey, or -1 otherwise."""
    # Reusing the earlier answer avoids duplicating its validation rules.
    if not is_direct_route(
        train_schedule, direction, start_station_index, destination_station_index
    ):
        return -1

    departure_time = train_schedule[start_station_index][1]
    arrival_time = train_schedule[destination_station_index][0]
    return arrival_time - departure_time