"""Development checks; the homework's command restrictions do not apply here."""

import unittest
from copy import deepcopy
from unittest.mock import patch

from part_1.question_a_ticket_price import calculate_ticket_price
from part_1.question_b_direct_route import is_direct_route
from part_1.question_c_travel_time import calculate_travel_time
from part_2.question_a_initialize_station import initialize_station
from part_2.question_b_split_schedule import split_schedule
from part_2.question_c_find_conflicts import find_conflicts
from part_2.question_d_delay_train import delay_train
from part_2.question_e_resolve_conflicts import resolve_conflicts
from part_3.question_a_find_direct_trains import find_direct_trains


class TicketPriceTests(unittest.TestCase):
    """Check the PDF examples and the boundaries between discount groups."""

    def test_pdf_examples(self):
        """Reproduce all five ticket-price examples from the PDF."""
        cases = [
            (50, 4, False, 0.0),
            (50, 14, False, 25.0),
            (50, 23, True, 40.0),
            (50, 40, False, 50.0),
            (50, 70, True, 25.0),
        ]
        for base_price, age, student, expected in cases:
            with self.subTest(age=age, student=student):
                result = calculate_ticket_price(base_price, age, student)
                self.assertEqual(result, expected)
                self.assertIs(type(result), float)

    def test_age_boundaries_and_discount_priority(self):
        """Exercise both sides of each age cutoff with both student flags."""
        for student in (False, True):
            for age in (1, 4):
                self.assertEqual(calculate_ticket_price(50, age, student), 0.0)
            for age in (5, 17, 65, 66):
                self.assertEqual(calculate_ticket_price(50, age, student), 25.0)
            for age in (18, 64):
                expected = 40.0 if student else 50.0
                self.assertEqual(calculate_ticket_price(50, age, student), expected)

    def test_rounding_and_full_price_output_type(self):
        """Keep one decimal place and return float even for an integer price."""
        self.assertEqual(calculate_ticket_price(12.34, 20, True), 9.9)
        self.assertEqual(calculate_ticket_price(12.34, 10, False), 6.2)
        self.assertEqual(calculate_ticket_price(12.34, 40, False), 12.3)
        self.assertIs(type(calculate_ticket_price(50, 40, False)), float)


class DirectRouteTests(unittest.TestCase):
    """Validate bounds, stopping stations, direction, and time ordering."""

    def test_pdf_examples(self):
        """Reproduce both direct-route examples."""
        self.assertTrue(
            is_direct_route([(0, 5), (20, 25), (35, 40)], "ltr", 0, 2)
        )
        self.assertFalse(
            is_direct_route([(0, 5), (-1, -1), (35, 40)], "ltr", 0, 1)
        )

    def test_invalid_indices_and_identical_stations(self):
        """Invalid indices must return False rather than index the list."""
        schedule = [(0, 5), (20, 25), (35, 40)]
        for start, destination in [(-1, 2), (0, -1), (3, 0), (0, 3), (1, 1)]:
            with self.subTest(start=start, destination=destination):
                self.assertFalse(is_direct_route(schedule, "ltr", start, destination))
        self.assertFalse(is_direct_route([], "ltr", 0, 1))

    def test_stops_and_both_directions(self):
        """Both endpoints must be stops, but intermediate stops are optional."""
        left_to_right = [(0, 5), (-1, -1), (35, 40)]
        right_to_left = [(35, 40), (-1, -1), (0, 5)]
        self.assertTrue(is_direct_route(left_to_right, "ltr", 0, 2))
        self.assertTrue(is_direct_route(right_to_left, "rtl", 2, 0))
        self.assertFalse(is_direct_route(left_to_right, "rtl", 0, 2))
        self.assertFalse(is_direct_route(right_to_left, "ltr", 2, 0))
        self.assertFalse(is_direct_route(left_to_right, "ltr", 1, 2))
        self.assertFalse(is_direct_route(right_to_left, "rtl", 2, 1))

    def test_time_order_and_unchanged_input(self):
        """Reject arrival before departure, but accept equality."""
        schedule = [(0, 5), (4, 10)]
        self.assertFalse(is_direct_route(schedule, "ltr", 0, 1))
        self.assertEqual(schedule, [(0, 5), (4, 10)])
        self.assertTrue(is_direct_route([(0, 5), (5, 10)], "ltr", 0, 1))


class TravelTimeTests(unittest.TestCase):
    """Check that duration calculation follows the direct-route decision."""

    def test_pdf_examples(self):
        """Reproduce both travel-time examples."""
        self.assertEqual(
            calculate_travel_time([(0, 5), (20, 25), (35, 40)], "ltr", 0, 2),
            30,
        )
        self.assertEqual(
            calculate_travel_time([(0, 5), (-1, -1), (35, 40)], "ltr", 0, 1),
            -1,
        )

    def test_reverse_direction_zero_duration_and_invalid_journeys(self):
        """Check reverse travel, a zero-time trip, and impossible journeys."""
        schedule = [(35, 40), (-1, -1), (0, 5)]
        self.assertEqual(calculate_travel_time(schedule, "rtl", 2, 0), 30)
        self.assertEqual(schedule, [(35, 40), (-1, -1), (0, 5)])
        self.assertEqual(calculate_travel_time([(0, 5), (5, 10)], "ltr", 0, 1), 0)
        for start, destination in [(-1, 0), (2, 3), (2, 2), (2, 1), (0, 2)]:
            with self.subTest(start=start, destination=destination):
                self.assertEqual(
                    calculate_travel_time(schedule, "rtl", start, destination), -1
                )
        self.assertEqual(calculate_travel_time([(0, 5), (4, 6)], "ltr", 0, 1), -1)


class InitializeStationTests(unittest.TestCase):
    """Check valid insertions, invalid indices, and mutation of the actual rows."""

    def test_pdf_examples_and_row_identity(self):
        """Reproduce both examples and ensure existing row references see changes."""
        schedules = [
            [(0, 5), (10, 15), (20, 25)],
            [(2, 7), (12, 17), (22, 27)],
        ]
        first_row = schedules[0]
        self.assertIsNone(initialize_station(schedules, 1))
        expected = [
            [(0, 5), (-1, -1), (10, 15), (20, 25)],
            [(2, 7), (-1, -1), (12, 17), (22, 27)],
        ]
        self.assertEqual(schedules, expected)
        self.assertIs(schedules[0], first_row)
        self.assertIsNone(initialize_station(schedules, -3))
        self.assertEqual(schedules, expected)

    def test_first_last_empty_and_invalid_positions(self):
        """Allow insertion at both boundaries, but not outside them."""
        for index, expected in [
            (0, [[(-1, -1), (0, 5)]]),
            (1, [[(0, 5), (-1, -1)]]),
            (-1, [[(0, 5)]]),
            (2, [[(0, 5)]]),
        ]:
            with self.subTest(index=index):
                schedules = [[(0, 5)]]
                initialize_station(schedules, index)
                self.assertEqual(schedules, expected)
        schedules = [[]]
        initialize_station(schedules, 0)
        self.assertEqual(schedules, [[(-1, -1)]])
        self.assertIsNone(initialize_station([], 0))

    def test_each_schedule_is_validated_separately(self):
        """Follow the per-train validation rule even for different row lengths."""
        schedules = [[], [(0, 5)]]
        initialize_station(schedules, 1)
        self.assertEqual(schedules, [[], [(0, 5), (-1, -1)]])


class SplitScheduleTests(unittest.TestCase):
    """Check full-length masks, direction alignment, and invalid-request behavior."""

    def test_pdf_example(self):
        """Reproduce the PDF split without modifying a different train."""
        schedules = [
            [(0, 5), (10, 15), (20, 25)],
            [(2, 7), (12, 17), (22, 27)],
        ]
        directions = ["ltr", "rtl"]
        untouched_row = schedules[1]
        original_row = schedules[0]
        self.assertIsNone(split_schedule(schedules, directions, 0, 2))
        self.assertEqual(
            schedules,
            [
                [(0, 5), (10, 15), (-1, -1)],
                [(-1, -1), (-1, -1), (20, 25)],
                [(2, 7), (12, 17), (22, 27)],
            ],
        )
        self.assertEqual(directions, ["ltr", "ltr", "rtl"])
        self.assertIs(schedules[2], untouched_row)
        self.assertIsNot(schedules[0], schedules[1])
        self.assertIsNot(schedules[0], original_row)
        self.assertIsNot(schedules[1], original_row)

    def test_rtl_split_is_by_index_not_travel_order(self):
        """The lower-index half stays first even for right-to-left travel."""
        schedules = [[(20, 25), (-1, -1), (0, 5)]]
        directions = ["rtl"]
        split_schedule(schedules, directions, 0, 1)
        self.assertEqual(
            schedules,
            [[(20, 25), (-1, -1), (-1, -1)], [(-1, -1), (-1, -1), (0, 5)]],
        )
        self.assertEqual(directions, ["rtl", "rtl"])

    def test_invalid_indices_change_neither_list(self):
        """Reject invalid train/split indices before any mutation."""
        for train_index, split_index in [(-1, 1), (1, 1), (0, -1), (0, 0), (0, 3)]:
            with self.subTest(train=train_index, split=split_index):
                schedules = [[(0, 5), (10, 15), (20, 25)]]
                directions = ["ltr"]
                self.assertIsNone(
                    split_schedule(schedules, directions, train_index, split_index)
                )
                self.assertEqual(schedules, [[(0, 5), (10, 15), (20, 25)]])
                self.assertEqual(directions, ["ltr"])
        self.assertIsNone(split_schedule([], [], 0, 1))
        schedules = [[(0, 5)]]
        split_schedule(schedules, ["ltr"], 0, 1)
        self.assertEqual(schedules, [[(0, 5)]])


class FindConflictsTests(unittest.TestCase):
    """Check closed-interval overlap and unique conflict tuples."""

    def test_pdf_example_and_no_mutation(self):
        """Reproduce the six conflicts in the PDF without changing schedules."""
        schedules = [
            [(0, 5), (10, 15), (20, 25)],
            [(2, 7), (12, 17), (22, 27)],
            [(0, 3), (16, 18), (30, 35)],
        ]
        original = [row[:] for row in schedules]
        self.assertCountEqual(
            find_conflicts(schedules),
            [(0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 0), (1, 2, 0), (1, 2, 1)],
        )
        self.assertEqual(schedules, original)

    def test_interval_boundaries_containment_and_skipped_stops(self):
        """Cover touching endpoints, containment, zero-time stops, and no-stop cells."""
        cases = [
            ((5, 10), (9, 12), True),
            ((5, 10), (10, 12), True),
            ((5, 10), (0, 5), True),
            ((5, 10), (6, 8), True),
            ((5, 10), (0, 20), True),
            ((5, 10), (11, 12), False),
            ((5, 10), (0, 4), False),
            ((5, 5), (5, 5), True),
            ((-1, -1), (-1, -1), False),
            ((-1, -1), (0, 5), False),
        ]
        for stop_a, stop_b, overlaps in cases:
            for first, second in [(stop_a, stop_b), (stop_b, stop_a)]:
                with self.subTest(first=first, second=second):
                    expected = [(0, 1, 0)] if overlaps else []
                    self.assertEqual(find_conflicts([[first], [second]]), expected)

    def test_empty_single_train_and_unique_pairs(self):
        """Never compare a train with itself or duplicate a pair."""
        self.assertEqual(find_conflicts([]), [])
        self.assertEqual(find_conflicts([[]]), [])
        self.assertEqual(find_conflicts([[(0, 5)]]), [])
        self.assertCountEqual(
            find_conflicts([[(0, 5)], [(0, 5)], [(0, 5)]]),
            [(0, 1, 0), (0, 2, 0), (1, 2, 0)],
        )


class DelayTrainTests(unittest.TestCase):
    """Check directional propagation, skipped stations, and in-place updates."""

    def test_pdf_examples(self):
        """Reproduce both delay examples, including a skipped starting station."""
        schedule = [(2, 7), (12, 17), (22, 27)]
        self.assertIsNone(delay_train(schedule, 1, 5, "ltr"))
        self.assertEqual(schedule, [(2, 7), (17, 22), (27, 32)])
        schedule = [(2, 7), (17, 22), (-1, -1)]
        self.assertIsNone(delay_train(schedule, 2, 3, "rtl"))
        self.assertEqual(schedule, [(5, 10), (20, 25), (-1, -1)])

    def test_default_direction_and_skipped_intermediate_stop(self):
        """The default is ltr and a non-stop does not block further delays."""
        schedule = [(0, 5), (-1, -1), (20, 25)]
        alias = schedule
        delay_train(schedule, 0, 3)
        self.assertIs(schedule, alias)
        self.assertEqual(alias, [(3, 8), (-1, -1), (23, 28)])
        schedule = [(20, 25), (-1, -1), (0, 5)]
        delay_train(schedule, 2, 3, "rtl")
        self.assertEqual(schedule, [(23, 28), (-1, -1), (3, 8)])

    def test_directional_endpoints_and_all_skipped(self):
        """Delaying the final station affects only that station in either direction."""
        schedule = [(20, 25), (10, 15), (0, 5)]
        delay_train(schedule, 0, 2, "rtl")
        self.assertEqual(schedule, [(22, 27), (10, 15), (0, 5)])
        schedule = [(0, 5), (10, 15), (20, 25)]
        delay_train(schedule, 2, 2)
        self.assertEqual(schedule, [(0, 5), (10, 15), (22, 27)])
        schedule = [(-1, -1), (-1, -1)]
        delay_train(schedule, 0, 100)
        self.assertEqual(schedule, [(-1, -1), (-1, -1)])


class ResolveConflictsTests(unittest.TestCase):
    """Check treatment counting, tuple priority, and fresh conflict detection."""

    def test_pdf_first_example(self):
        """Reproduce the two treatments and final schedules in the first example."""
        schedules = [[(0, 5), (10, 15)], [(3, 8), (12, 17)]]
        directions = ["ltr", "ltr"]
        first_row = schedules[0]
        self.assertEqual(resolve_conflicts(schedules, directions, 5), 2)
        self.assertEqual(schedules, [[(10, 15), (20, 25)], [(3, 8), (12, 17)]])
        self.assertIs(schedules[0], first_row)
        self.assertEqual(directions, ["ltr", "ltr"])
        self.assertEqual(find_conflicts(schedules), [])

    def test_pdf_second_example(self):
        """Reproduce all ten treatments with mixed train directions."""
        schedules = [
            [(0, 5), (10, 15), (20, 25)],
            [(22, 27), (12, 17), (2, 7)],
            [(30, 35), (16, 18), (0, 3)],
        ]
        self.assertEqual(resolve_conflicts(schedules, ["ltr", "rtl", "rtl"], 5), 10)
        self.assertEqual(
            schedules,
            [
                [(0, 5), (35, 40), (45, 50)],
                [(47, 52), (27, 32), (7, 12)],
                [(30, 35), (16, 18), (0, 3)],
            ],
        )
        self.assertEqual(find_conflicts(schedules), [])

    def test_repeated_treatments_of_one_conflict(self):
        """Count each delay, not just distinct train/station triples."""
        schedules = [[(0, 5)], [(3, 8)]]
        self.assertEqual(resolve_conflicts(schedules, ["ltr", "ltr"], 5), 2)
        self.assertEqual(schedules, [[(10, 15)], [(3, 8)]])

    def test_lowest_station_priority_even_for_rtl(self):
        """Numerical station priority takes precedence over travel order."""
        schedules = [[(10, 12), (0, 2)], [(10, 12), (0, 2)]]
        self.assertEqual(resolve_conflicts(schedules, ["rtl", "rtl"], 3), 2)
        self.assertEqual(schedules, [[(16, 18), (3, 5)], [(10, 12), (0, 2)]])

    def test_new_conflict_after_delay_is_detected(self):
        """A delay can create a conflict with a previously uninvolved train."""
        schedules = [
            [(0, 0), (10, 10)],
            [(0, 1), (50, 50)],
            [(-1, -1), (15, 15)],
        ]
        self.assertEqual(resolve_conflicts(schedules, ["ltr", "ltr", "ltr"], 5), 2)
        self.assertEqual(schedules[0], [(5, 5), (20, 20)])
        self.assertEqual(find_conflicts(schedules), [])

    def test_conflict_detector_order_does_not_change_priority(self):
        """Still select the smallest tuple if the detector returns reversed order."""
        def reverse_conflicts(schedules):
            """Return the real conflicts in reverse order for this check."""
            return find_conflicts(schedules)[::-1]

        schedules = [[(10, 12), (0, 2)], [(10, 12), (0, 2)]]
        with patch.dict(resolve_conflicts.__globals__, {"find_conflicts": reverse_conflicts}):
            self.assertEqual(resolve_conflicts(schedules, ["rtl", "rtl"], 3), 2)
        self.assertEqual(schedules, [[(16, 18), (3, 5)], [(10, 12), (0, 2)]])

    def test_no_conflicts_requires_no_treatments(self):
        """Empty or already safe schedules return zero without changes."""
        self.assertEqual(resolve_conflicts([], [], 1), 0)
        schedules = [[(0, 1)], [(2, 3)]]
        self.assertEqual(resolve_conflicts(schedules, ["ltr", "rtl"], 1), 0)
        self.assertEqual(schedules, [[(0, 1)], [(2, 3)]])


class FindDirectTrainsTests(unittest.TestCase):
    """Check company searches against the supplied example and window boundaries."""

    def setUp(self):
        """Give every test its own copy of the PDF's company data."""
        self.company = {
            "station_names": [
                "Beer Sheva Center",
                "Tel Aviv Savidor Center",
                "Haifa Merkaz HaShmona",
            ],
            "schedules": [
                [(0, 5), (20, 25), (35, 40)],
                [(47, 52), (27, 32), (7, 12)],
                [(10, 15), (-1, -1), (45, 50)],
            ],
            "train_directions": ["ltr", "rtl", "ltr"],
            "base_ticket_prices": [60.0, 55.0, 40.0],
        }
        self.start = "Beer Sheva Center"
        self.destination = "Haifa Merkaz HaShmona"

    def test_pdf_example_and_no_mutation(self):
        """Reproduce both option dictionaries exactly and preserve company data."""
        original = deepcopy(self.company)
        options = find_direct_trains(self.company, self.start, self.destination, (0, 20))
        self.assertCountEqual(
            options,
            [
                {
                    "train_index": 0,
                    "departure_time": 5,
                    "arrival_time": 35,
                    "travel_time": 30,
                    "base_price": 60.0,
                },
                {
                    "train_index": 2,
                    "departure_time": 15,
                    "arrival_time": 45,
                    "travel_time": 30,
                    "base_price": 40.0,
                },
            ],
        )
        self.assertEqual(self.company, original)
        options[0]["base_price"] = 999.0
        self.assertEqual(self.company, original)

    def test_inclusive_window_endpoints(self):
        """Both window endpoints count, including a one-time-unit-value window."""
        for window, expected_indices in [
            ((5, 15), [0, 2]),
            ((5, 5), [0]),
            ((15, 15), [2]),
            ((6, 14), []),
            ((0, 0), []),
        ]:
            with self.subTest(window=window):
                options = find_direct_trains(
                    self.company, self.start, self.destination, window
                )
                self.assertCountEqual(
                    [option["train_index"] for option in options], expected_indices
                )

    def test_right_to_left_search(self):
        """Search the opposite direction using the actual origin's departure."""
        self.assertEqual(
            find_direct_trains(self.company, self.destination, self.start, (12, 12)),
            [
                {
                    "train_index": 1,
                    "departure_time": 12,
                    "arrival_time": 47,
                    "travel_time": 35,
                    "base_price": 55.0,
                }
            ],
        )

    def test_skipped_destination_and_same_station(self):
        """Exclude a train that skips the destination and reject identical endpoints."""
        options = find_direct_trains(
            self.company, self.start, "Tel Aviv Savidor Center", (0, 20)
        )
        self.assertEqual([option["train_index"] for option in options], [0])
        self.assertEqual(
            find_direct_trains(self.company, self.start, self.start, (0, 100)), []
        )

    def test_time_validation_and_zero_duration(self):
        """Reuse route validation, without discarding a valid zero-duration trip."""
        self.company["schedules"][0][2] = (4, 40)
        options = find_direct_trains(self.company, self.start, self.destination, (5, 5))
        self.assertEqual(options, [])
        self.company["schedules"][0][2] = (5, 40)
        options = find_direct_trains(self.company, self.start, self.destination, (5, 5))
        self.assertEqual(len(options), 1)
        self.assertEqual(options[0]["travel_time"], 0)

    def test_dictionary_keys_and_value_types(self):
        """Every option has exactly the required string keys and numeric types."""
        options = find_direct_trains(self.company, self.start, self.destination, (0, 20))
        for option in options:
            self.assertEqual(
                set(option),
                {"train_index", "departure_time", "arrival_time", "travel_time", "base_price"},
            )
            for key, value in option.items():
                self.assertIs(type(key), str)
                self.assertIs(type(value), float if key == "base_price" else int)

    def test_no_trains(self):
        """A company with no trains has no matching journeys."""
        self.company["schedules"] = []
        self.company["train_directions"] = []
        self.company["base_ticket_prices"] = []
        self.assertEqual(
            find_direct_trains(self.company, self.start, self.destination, (0, 20)), []
        )


if __name__ == "__main__":
    unittest.main()