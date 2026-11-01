"""Part 2, Question E: repeatedly delay trains until no conflicts remain.

Approach:
1. Reuse Question C to find the current conflicts.
2. Select min(conflicts): Python compares integer tuples from left to right,
   exactly matching the required train A, train B, then station priority.
3. Reuse Question D to delay train A in its own direction, by exactly delay.
4. Count this one treatment and scan all schedules again before choosing again.

Inputs: schedules, matching directions, and a positive integer delay.
Output: the number of delay operations; schedules are changed in-place.
Example: trains [(0, 5)] and [(3, 8)] with delay 5 need two treatments:
the first train becomes [(5, 10)], then [(10, 15)], so the answer is 2.
One treatment can clear several conflicts, or fail to clear the selected one.
The imports share earlier answers; the combined submission has no imports.
"""

from part_2.question_c_find_conflicts import find_conflicts
from part_2.question_d_delay_train import delay_train


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