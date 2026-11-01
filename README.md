# Homework 1: Train Schedules

Solutions to all **nine functions** specified in the supplied 15-page PDF.
Each question has its own Python file, with an approach explanation at the top,
a function docstring, and comments explaining the important decisions.

## Start Here

Read the questions in the order below. You only need Python 3.8 or newer;
there are no packages to install. Run commands from this project's root folder.

| PDF Question | Explained Answer | Function |
| --- | --- | --- |
| Part 1 A | [part_1/question_a_ticket_price.py](part_1/question_a_ticket_price.py) | `calculate_ticket_price` |
| Part 1 B | [part_1/question_b_direct_route.py](part_1/question_b_direct_route.py) | `is_direct_route` |
| Part 1 C | [part_1/question_c_travel_time.py](part_1/question_c_travel_time.py) | `calculate_travel_time` |
| Part 2 A | [part_2/question_a_initialize_station.py](part_2/question_a_initialize_station.py) | `initialize_station` |
| Part 2 B | [part_2/question_b_split_schedule.py](part_2/question_b_split_schedule.py) | `split_schedule` |
| Part 2 C | [part_2/question_c_find_conflicts.py](part_2/question_c_find_conflicts.py) | `find_conflicts` |
| Part 2 D | [part_2/question_d_delay_train.py](part_2/question_d_delay_train.py) | `delay_train` |
| Part 2 E | [part_2/question_e_resolve_conflicts.py](part_2/question_e_resolve_conflicts.py) | `resolve_conflicts` |
| Part 3 A | [part_3/question_a_find_direct_trains.py](part_3/question_a_find_direct_trains.py) | `find_direct_trains` |

The review answers use a few imports to share earlier functions instead of copying
their logic. Because imports are not on the PDF's allowed-command list, the
**combined homework version** is [submission/HW1.py](submission/HW1.py). It contains
the same nine implementations, explanations, and comments, but **no imports**.
The review folders, tests, and build tool are study/development files, not part of
that submission file. The PDF does not specify a required submission filename.

## Understand the Data

- A **station index** is its position in the list, counting from zero.
- One stop is a **tuple**, `(arrival, departure)`, such as `(9, 10)`.
- `(-1, -1)` means the train does not stop at that station.
- One train's schedule is a **list of stop tuples**, in station-index order.
- The company schedules form a **list of those lists**, one row per train.
- `ltr` means visiting increasing station indices; `rtl` means decreasing ones.
- Times are abstract integer units, not hours or clock readings.
- A **dictionary** stores named values, such as a company's `"schedules"` list.

For example:

```python
schedule = [(0, 5), (-1, -1), (35, 40)]
```

This train stops at station 0, skips station 1, and stops at station 2. If its
direction is `ltr`, a journey from station 0 to station 2 takes `35 - 5 = 30`
time units. Skipping the middle station does not prevent a direct journey.

## Try an Answer

Start Python from the project root:

```powershell
python
```

Then enter:

```python
from part_1.question_a_ticket_price import calculate_ticket_price
from part_1.question_c_travel_time import calculate_travel_time
from part_2.question_a_initialize_station import initialize_station

print(calculate_ticket_price(50, 70, True))
# 25.0: the senior discount is larger than the student discount.

print(calculate_travel_time([(0, 5), (-1, -1), (35, 40)], "ltr", 0, 2))
# 30: destination arrival minus origin departure.

schedules = [[(0, 5), (10, 15)]]
initialize_station(schedules, 1)
print(schedules)
# [[(0, 5), (-1, -1), (10, 15)]]
```

The answer files define functions. Running a file by itself is not meant to print
results; import and call its function, or use the tests below. Import from the
project root so the shared answers can be found.

**In-place** means a function edits the list you supplied. For example,
`initialize_station` changes `schedules` directly and returns `None`. Do not write
`schedules = initialize_station(schedules, 1)`, since that would replace your
variable with `None`. `resolve_conflicts` also changes schedules, but returns an
integer treatment count.

## Tricky Rules

- Only the biggest ticket discount applies; discounts are not added together.
- Negative station indices are invalid, despite Python normally allowing them.
- A destination arrival equal to origin departure is a valid zero-time journey.
- Splitting uses station indices, not travel order, even for an `rtl` train.
- Conflict intervals include both endpoints. `(5, 10)` conflicts with `(10, 12)`.
- Delay skips `(-1, -1)` without stopping its propagation to later stops.
- Resolution always chooses the smallest `(train_a, train_b, station)` tuple.
- After every delay, recompute conflicts; old results may no longer be correct.
- Departure windows include both boundaries and refer to departure, not arrival.
- Part 3 returns the train's base price, not a passenger's discounted price.

For `resolve_conflicts`, the returned count is the number of **delay operations**,
consistent with both PDF examples. One conflict may require multiple delays:

| Treatment | Train 0 Stop | Train 1 Stop | Still Conflicting? |
| --- | --- | --- | --- |
| Before treatment | `(0, 5)` | `(3, 8)` | Yes |
| After delay of 5 | `(5, 10)` | `(3, 8)` | Yes |
| After another delay of 5 | `(10, 15)` | `(3, 8)` | No |

The answer is `2`, although only one train-pair/station triple was involved.

## Run the Checks

```powershell
python -m unittest discover -s tests -v
```

[tests/test_homework.py](tests/test_homework.py) checks every PDF example, age and
index boundaries, skipped stops, directions, in-place changes, conflict priority,
and the exact output dictionaries. Each test has a descriptive name and docstring.

[tests/test_submission.py](tests/test_submission.py) checks that the combined file
matches the review answers, contains all nine documented functions, uses only
permitted constructs, and passes the same behavioral tests again.

To focus on one question, for example ticket pricing:

```powershell
python -m unittest discover -s tests -p test_homework.py -k TicketPrice -v
```

## After Editing

Edit the individual question file, then regenerate the combined version and test:

```powershell
python tools/build_submission.py
python -m unittest discover -s tests -v
```

[tools/build_submission.py](tools/build_submission.py) preserves implementation
comments, converts each question's header to section comments, and removes only
the study imports. It is not homework code and does not have the exercise's
command restrictions.

The introduction mentions planning for passenger groups, but the supplied PDF
ends with Part 3 A on page 15. No additional group-planning function is specified,
so this solution implements the nine actual function specifications only.