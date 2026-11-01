"""Part 2, Question C: find trains occupying the same station at the same time.

Approach:
1. Visit each train pair once, always with the smaller index first.
2. Compare their stops at each station; skip (-1, -1) entries.
3. Treat each stop as a closed interval [arrival, departure]. Two intervals
   overlap when each arrival is no later than the other train's departure.
4. Append (first_train_index, second_train_index, station_index) on overlap.

Input: the company's schedules. Output: a list of conflict tuples.
Example: [[(5, 10)], [(10, 12)]] produces [(0, 1, 0)]; equality counts.
Directions do not matter. The input is not changed and no pair is duplicated.
"""


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