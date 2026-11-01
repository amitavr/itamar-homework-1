"""Part 3, Question A: find direct trains inside a departure-time window.

Approach:
1. Translate the two station names into indices with list.index.
2. Visit every train and reuse Part 1's calculate_travel_time. It already calls
   is_direct_route, so directions, stopping stations, and times are checked once.
3. Skip impossible journeys and departures outside the inclusive window.
4. Append a new dictionary with exactly the five requested fields.

Inputs: the company dictionary, two existing station names, and a valid window.
Output: a list of journey dictionaries, or [] if none match. No input is changed.
For the PDF company, Beer Sheva to Haifa in (0, 20) returns trains 0 and 2.
Return the base price, not a passenger discount; passenger data is not an input.
The import shares the earlier answer; the combined submission has no imports.
"""

from part_1.question_c_travel_time import calculate_travel_time


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