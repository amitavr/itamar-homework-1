"""Homework 1: all nine answers from the supplied 15-page PDF.

Generated from the explained scripts in part_1, part_2, and part_3.
Each section keeps its approach explanation and implementation comments.
No imports, external libraries, or demonstration code are needed here.
Edit the review scripts and run python tools/build_submission.py to rebuild.
"""


# Source: part_1/question_a_ticket_price.py
# Part 1, Question A: calculate a passenger's ticket price.
#
# Approach:
# 1. Check the discounts from largest to smallest: free, 50%, then 20%.
# 2. Use if/elif so only one discount applies, even to a senior student.
# 3. Convert the result to float and round to one decimal place.
#
# Inputs: a positive base price, a positive integer age, and a student flag.
# Output: the discounted price as a float, rounded to one decimal place.
# Example: calculate_ticket_price(50, 70, True) returns 25.0, not 20.0.
# The function does not change any input.


def calculate_ticket_price(base_price, passenger_age, is_student):
    """Return the ticket price after the single largest eligible discount."""
    if passenger_age < 5:
        # Children younger than five travel free.
        price = 0.0
    elif passenger_age <= 17 or passenger_age >= 65:
        # This branch also handles senior students before the student branch.
        price = base_price * 0.5
    elif passenger_age >= 18 and is_student:
        price = base_price * 0.8
    else:
        price = base_price

    # float keeps the output type correct even if the caller supplies 50.
    return round(float(price), 1)


# Source: part_1/question_b_direct_route.py
# Part 1, Question B: decide whether one train offers a direct journey.
#
# Approach:
# 1. Reject out-of-range indices before reading the schedule.
# 2. Reject identical stations and stations marked (-1, -1), meaning no stop.
# 3. Check station order: increasing indices for ltr, decreasing for rtl.
# 4. Require destination arrival to be at least the origin departure time.
#
# Inputs: one schedule, its direction, and origin/destination station indices.
# Output: True if every rule holds, otherwise False. No inputs are changed.
# Example: is_direct_route([(0, 5), (20, 25)], 'ltr', 0, 1) returns True.
# A train may skip intermediate stations; only the two endpoints must be stops.


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


# Source: part_1/question_c_travel_time.py
# Part 1, Question C: calculate the duration of a possible direct journey.
#
# Approach:
# 1. Reuse Question B to check all the direct-journey rules.
# 2. Return -1 if the journey is impossible.
# 3. Otherwise subtract origin departure from destination arrival.
#
# Inputs: one schedule, its direction, and origin/destination station indices.
# Output: an integer duration, or -1. No inputs are changed.
# Example: calculate_travel_time([(0, 5), (35, 40)], 'ltr', 0, 1) returns 30.
# The import shares the earlier answer; the combined submission needs no imports.


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


# Source: part_2/question_a_initialize_station.py
# Part 2, Question A: insert a new, unused station into every schedule.
#
# Approach:
# 1. Visit each train's existing schedule.
# 2. Check that the insertion index is between zero and its length, inclusive.
# 3. Use list.insert to add (-1, -1), meaning this train does not stop there yet.
#
# Inputs: the company's schedules and the new station's index.
# Output: no new value; the existing schedules are changed in-place.
# Example: inserting at index 1 in [(0, 5), (10, 15)] produces
# [(0, 5), (-1, -1), (10, 15)]. Index len(schedule) appends a station.
# Negative indices are rejected rather than using Python's negative indexing.


def initialize_station(schedules, station_index):
    """Insert a non-stopping station into each schedule where the index is valid."""
    for train_schedule in schedules:
        # Validate each row separately, as requested in the question.
        if 0 <= station_index <= len(train_schedule):
            train_schedule.insert(station_index, (-1, -1))


# Source: part_2/question_b_split_schedule.py
# Part 2, Question B: replace one train with two independent schedules.
#
# Approach:
# 1. Validate both indices before changing either input list.
# 2. Build two new lists with the same length as the original schedule.
# 3. Keep indices below split_station in the first; keep the rest in the second.
#    Fill the unused positions in each list with (-1, -1).
# 4. Replace the old train and insert the second train immediately after it.
# 5. Duplicate the original direction at the matching position.
#
# Inputs: schedules, matching directions, a train index, and a split index.
# Output: no new value; both company lists are changed in-place.
# Example: splitting [(0, 5), (10, 15)] at 1 gives [(0, 5), (-1, -1)]
# and [(-1, -1), (10, 15)]. This index-based rule is the same for ltr and rtl.


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


# Source: part_2/question_c_find_conflicts.py
# Part 2, Question C: find trains occupying the same station at the same time.
#
# Approach:
# 1. Visit each train pair once, always with the smaller index first.
# 2. Compare their stops at each station; skip (-1, -1) entries.
# 3. Treat each stop as a closed interval [arrival, departure]. Two intervals
#    overlap when each arrival is no later than the other train's departure.
# 4. Append (first_train_index, second_train_index, station_index) on overlap.
#
# Input: the company's schedules. Output: a list of conflict tuples.
# Example: [[(5, 10)], [(10, 12)]] produces [(0, 1, 0)]; equality counts.
# Directions do not matter. The input is not changed and no pair is duplicated.


def find_conflicts(schedules):
    """Return every pairwise station conflict, counting shared endpoints."""
    conflicts = []
    for train_index_a in range(len(schedules)):
        # Starting at a + 1 avoids self-comparisons and reversed duplicates.
        for train_index_b in range(train_index_a + 1, len(schedules)):
            for station in range(len(schedules[train_index_a])):
                stop_a = schedules[train_index_a][station]
                stop_b = schedules[train_index_b][station]
                if stop_a == (-1, -1) or stop_b == (-1, -1):
                    continue

                # <= includes a train arriving exactly when the other leaves.
                if stop_a[0] <= stop_b[1] and stop_b[0] <= stop_a[1]:
                    conflicts.append((train_index_a, train_index_b, station))

    return conflicts


# Source: part_2/question_d_delay_train.py
# Part 2, Question D: delay a train from one station onward in its direction.
#
# Approach:
# 1. For ltr, visit indices from start_station up to the last station.
# 2. For rtl, visit indices from start_station down to zero.
# 3. Leave (-1, -1) unchanged, but continue to the remaining stations.
# 4. Replace each real stop's tuple with (arrival + delay, departure + delay).
#    A tuple cannot be edited, so its replacement is stored in the same list.
#
# Inputs: one schedule, a valid starting index, a positive delay, and direction.
# Output: no new value; the existing schedule is changed in-place.
# Example: delay_train([(0, 5), (10, 15)], 1, 3) changes the last stop to (13, 18).
# The default direction is ltr. The starting station is included in the delay.


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


# Source: part_2/question_e_resolve_conflicts.py
# Part 2, Question E: repeatedly delay trains until no conflicts remain.
#
# Approach:
# 1. Reuse Question C to find the current conflicts.
# 2. Select min(conflicts): Python compares integer tuples from left to right,
#    exactly matching the required train A, train B, then station priority.
# 3. Reuse Question D to delay train A in its own direction, by exactly delay.
# 4. Count this one treatment and scan all schedules again before choosing again.
#
# Inputs: schedules, matching directions, and a positive integer delay.
# Output: the number of delay operations; schedules are changed in-place.
# Example: trains [(0, 5)] and [(3, 8)] with delay 5 need two treatments:
# the first train becomes [(5, 10)], then [(10, 15)], so the answer is 2.
# One treatment can clear several conflicts, or fail to clear the selected one.
# The imports share earlier answers; the combined submission has no imports.


def resolve_conflicts(schedules, train_directions, delay):
    """Resolve conflicts in tuple priority order and return the treatment count."""
    total_fixed = 0
    conflicts = find_conflicts(schedules)

    while conflicts:
        # min works even if find_conflicts returns its list in a different order.
        train_index_a, train_index_b, station = min(conflicts)
        delay_train(
            schedules[train_index_a], station, delay, train_directions[train_index_a]
        )
        total_fixed += 1

        # Never reuse the old list: a delay can remove or create other conflicts.
        conflicts = find_conflicts(schedules)

    return total_fixed


# Source: part_3/question_a_find_direct_trains.py
# Part 3, Question A: find direct trains inside a departure-time window.
#
# Approach:
# 1. Translate the two station names into indices with list.index.
# 2. Visit every train and reuse Part 1's calculate_travel_time. It already calls
#    is_direct_route, so directions, stopping stations, and times are checked once.
# 3. Skip impossible journeys and departures outside the inclusive window.
# 4. Append a new dictionary with exactly the five requested fields.
#
# Inputs: the company dictionary, two existing station names, and a valid window.
# Output: a list of journey dictionaries, or [] if none match. No input is changed.
# For the PDF company, Beer Sheva to Haifa in (0, 20) returns trains 0 and 2.
# Return the base price, not a passenger discount; passenger data is not an input.
# The import shares the earlier answer; the combined submission has no imports.


def find_direct_trains(company, start_station, destination_station, departure_window):
    """Return direct journeys whose origin departure is within the given window."""
    start_index = company["station_names"].index(start_station)
    destination_index = company["station_names"].index(destination_station)
    earliest_departure, latest_departure = departure_window
    options = []

    for train_index, train_schedule in enumerate(company["schedules"]):
        direction = company["train_directions"][train_index]
        travel_time = calculate_travel_time(
            train_schedule, direction, start_index, destination_index
        )
        # A duration of zero is valid; only -1 means the journey is impossible.
        if travel_time == -1:
            continue

        departure_time = train_schedule[start_index][1]
        if earliest_departure <= departure_time <= latest_departure:
            # Each option is a fresh dictionary, not a change to the company.
            options.append(
                {
                    "train_index": train_index,
                    "departure_time": departure_time,
                    "arrival_time": train_schedule[destination_index][0],
                    "travel_time": travel_time,
                    "base_price": float(company["base_ticket_prices"][train_index]),
                }
            )

    return options
