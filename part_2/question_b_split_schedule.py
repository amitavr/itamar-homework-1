"""Part 2, Question B: replace one train with two independent schedules.

Approach:
1. Validate both indices before changing either input list.
2. Build two new lists with the same length as the original schedule.
3. Keep indices below split_station in the first; keep the rest in the second.
   Fill the unused positions in each list with (-1, -1).
4. Replace the old train and insert the second train immediately after it.
5. Duplicate the original direction at the matching position.

Inputs: schedules, matching directions, a train index, and a split index.
Output: no new value; both company lists are changed in-place.
Example: splitting [(0, 5), (10, 15)] at 1 gives [(0, 5), (-1, -1)]
and [(-1, -1), (10, 15)]. This index-based rule is the same for ltr and rtl.
"""


def split_schedule(schedules, train_directions, train_index, split_station):
    """Replace a valid train with two full-length schedules and copy its direction."""
    if not 0 <= train_index < len(schedules):
        return

    original_schedule = schedules[train_index]
    if not 1 <= split_station < len(original_schedule):
        return

    first_schedule = []
    second_schedule = []
    for station_index, stop in enumerate(original_schedule):
        # The split station belongs only to the second new schedule.
        if station_index < split_station:
            first_schedule.append(stop)
            second_schedule.append((-1, -1))
        else:
            first_schedule.append((-1, -1))
            second_schedule.append(stop)

    # Keep the outer lists, while replacing one row with two newly built rows.
    schedules[train_index] = first_schedule
    schedules.insert(train_index + 1, second_schedule)
    train_directions.insert(train_index + 1, train_directions[train_index])