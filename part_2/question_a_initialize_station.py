"""Part 2, Question A: insert a new, unused station into every schedule.

Approach:
1. Visit each train's existing schedule.
2. Check that the insertion index is between zero and its length, inclusive.
3. Use list.insert to add (-1, -1), meaning this train does not stop there yet.

Inputs: the company's schedules and the new station's index.
Output: no new value; the existing schedules are changed in-place.
Example: inserting at index 1 in [(0, 5), (10, 15)] produces
[(0, 5), (-1, -1), (10, 15)]. Index len(schedule) appends a station.
Negative indices are rejected rather than using Python's negative indexing.
"""


def initialize_station(schedules, station_index):
    """Insert a non-stopping station into each schedule where the index is valid."""
    for train_schedule in schedules:
        # Validate each row separately, as requested in the question.
        if 0 <= station_index <= len(train_schedule):
            train_schedule.insert(station_index, (-1, -1))