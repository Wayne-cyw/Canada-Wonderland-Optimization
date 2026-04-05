import json


def _load_json(filename: str) -> dict:
    """Load and return the contents of a JSON file as a dict."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def _reconstruct_path(parent: list, rides: list, mask: int, last: int) -> tuple:
    """
    Trace back through the parent table to reconstruct the ordered ride path.

    Args:
        parent (list): 2D table where parent[mask][i] = (prev_mask, prev_i).
        rides (list): The full list of candidate ride names.
        mask (int): Bitmask of the best final state.
        last (int): Index of the last ride visited in the best final state.

    Returns:
        tuple: Ride names in the order they were visited.

    Single ride — no parent pointer, just returns the one ride:

    >>> parent = [[None, None], [None, None], [None, None], [None, None]]
    >>> _reconstruct_path(parent, ["RideA", "RideB"], 0b01, 0)
    ('RideA',)

    Two rides — RideB (index 1) was reached from RideA (index 0):

    >>> parent = [[None, None], [None, None], [None, None], [None, (1, 0)]]
    >>> _reconstruct_path(parent, ["RideA", "RideB"], 0b11, 1)
    ('RideA', 'RideB')
    """
    path = []
    while mask:
        path.append(rides[last])
        entry = parent[mask][last]
        if entry is None:
            break
        mask, last = entry
    return tuple(reversed(path))


def find_optimal_path(rides: list, budget: int, *,
                      _travel_times: dict = None,
                      _wait_times: dict = None,
                      _durations: dict = None) -> tuple:
    """
    Find the optimal ordering of rides that maximises rides visited within the
    time budget, starting from the park Entrance.

    The total time to visit a ride from a prior location is:
        travel_time[from][ride] + wait_time[ride] + ride_duration[ride]

    Uses bitmask dynamic programming for an exact solution.
    State: dp[mask][i] = minimum time to have visited exactly the rides encoded
    in `mask`, ending at ride index i.
    Complexity: O(2^n * n^2) — practical for up to ~20 selected rides.

    Args:
        rides (list[str]): Ride names chosen by the user. Each name must exist
            as a key in travel_time.json, wait_time.json, and ride_duration.json.
        budget (int): Total time available in minutes.
        _travel_times (dict, optional): Overrides travel_time.json (for testing).
        _wait_times   (dict, optional): Overrides wait_time.json (for testing).
        _durations    (dict, optional): Overrides ride_duration.json (for testing).

    Returns:
        tuple[str]: Ride names in the optimal visit order. Returns an empty
            tuple if no single ride can be completed within the budget.

    --- Shared setup for all doctests ---

    >>> travel = {
    ...     "Entrance": {"RideA": 2, "RideB": 5},
    ...     "RideA":    {"RideB": 3},
    ...     "RideB":    {"RideA": 3},
    ... }
    >>> wait = {"RideA": 5,  "RideB": 10}
    >>> dur  = {"RideA": 2,  "RideB": 3}

    Both rides fit — RideA costs 9 min, RideA→RideB totals 25 min:

    >>> find_optimal_path(["RideA", "RideB"], 25, _travel_times=travel, _wait_times=wait, _durations=dur)
    ('RideA', 'RideB')

    Only one ride fits — RideA (9 min) beats RideB (18 min) on the tiebreaker:

    >>> find_optimal_path(["RideA", "RideB"], 20, _travel_times=travel, _wait_times=wait, _durations=dur)
    ('RideA',)

    Budget too small for any ride:

    >>> find_optimal_path(["RideA", "RideB"], 5, _travel_times=travel, _wait_times=wait, _durations=dur)
    ()

    Empty ride list:

    >>> find_optimal_path([], 60, _travel_times=travel, _wait_times=wait, _durations=dur)
    ()
    """
    travel_times = _travel_times if _travel_times is not None else _load_json('travel_time.json')
    wait_times   = _wait_times   if _wait_times   is not None else _load_json('wait_time.json')
    durations    = _durations    if _durations    is not None else _load_json('ride_duration.json')

    n           = len(rides)
    num_states  = 1 << n   # 2^n possible subsets of rides
    UNREACHABLE = float('inf')

    # Set up DP and parent tables                                         
    # dp[mask][i]     = min time to visit rides in `mask`, ending at i 
    # parent[mask][i] = (prev_mask, prev_i) for path reconstruction     

    dp     = [[UNREACHABLE] * n for _ in range(num_states)]
    parent = [[None]        * n for _ in range(num_states)]

    # Base case: travel from Entrance to each individual ride
    for i, ride in enumerate(rides):
        time_from_entrance = travel_times["Entrance"][ride] + wait_times[ride] + durations[ride]
        dp[1 << i][i] = time_from_entrance

    # Fill DP: extend each state by visiting one more unvisited ride 
    # Ascending mask order ensures sub-paths are settled before extending 
    for mask in range(1, num_states):
        for current_ride in range(n):

            current_not_in_mask = not (mask & (1 << current_ride))
            current_unreachable = dp[mask][current_ride] == UNREACHABLE
            if current_not_in_mask or current_unreachable:
                continue

            for next_ride in range(n):
                next_already_visited = mask & (1 << next_ride)
                if next_already_visited:
                    continue

                step_cost = (travel_times[rides[current_ride]][rides[next_ride]]
                             + wait_times[rides[next_ride]]
                             + durations[rides[next_ride]])
                new_time = dp[mask][current_ride] + step_cost
                new_mask = mask | (1 << next_ride)

                if new_time < dp[new_mask][next_ride]:
                    dp[new_mask][next_ride]     = new_time
                    parent[new_mask][next_ride] = (mask, current_ride)

    # Find best state: most rides within budget, shortest time on ties 
    best_mask = 0
    best_time = UNREACHABLE
    best_last = -1

    for mask in range(1, num_states):
        rides_in_this_mask = bin(mask).count('1')
        rides_in_best_mask = bin(best_mask).count('1')

        for last_ride in range(n):
            if not (mask & (1 << last_ride)):
                continue

            total_time = dp[mask][last_ride]
            if total_time > budget:
                continue

            visits_more_rides   = rides_in_this_mask > rides_in_best_mask
            ties_but_is_faster  = rides_in_this_mask == rides_in_best_mask and total_time < best_time
            if visits_more_rides or ties_but_is_faster:
                best_mask = mask
                best_time = total_time
                best_last = last_ride

    if best_mask == 0:
        return ()

    return _reconstruct_path(parent, rides, best_mask, best_last)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
