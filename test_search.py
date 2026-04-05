import pytest
from search import find_optimal_path, _reconstruct_path


# --------------------------------------------------------------------------- #
# Shared test fixtures                                                         #
# --------------------------------------------------------------------------- #

@pytest.fixture
def two_rides():
    """
    Minimal two-ride dataset.

    Costs from Entrance:
        RideA: walk=2 + wait=5 + ride=2  =  9 min
        RideB: walk=5 + wait=10 + ride=3 = 18 min

    Costs for full paths:
        RideA → RideB: 9 + (3+10+3) = 25 min
        RideB → RideA: 18 + (3+5+2) = 28 min
    """
    travel = {
        "Entrance": {"RideA": 2, "RideB": 5},
        "RideA":    {"RideB": 3},
        "RideB":    {"RideA": 3},
    }
    wait = {"RideA": 5,  "RideB": 10}
    dur  = {"RideA": 2,  "RideB": 3}
    return travel, wait, dur


@pytest.fixture
def three_rides():
    """
    Three-ride dataset designed so the optimal path differs from a greedy choice.

    Costs from Entrance:
        RideA: 2+5+2   =  9 min  (cheapest first stop)
        RideB: 5+10+3  = 18 min
        RideC: 4+8+1   = 13 min

    All 3-ride paths (sorted by total time):
        RideC → RideA → RideB: 13 + 9  + 16 = 38 min  ← global optimum
        RideA → RideC → RideB:  9 + 11 + 19 = 39 min  ← what greedy picks
        RideB → RideA → RideC: 18 + 10 + 11 = 39 min
        RideA → RideB → RideC:  9 + 16 + 15 = 40 min
        RideC → RideB → RideA: 13 + 19 + 10 = 42 min
        RideB → RideC → RideA: 18 + 15 +  9 = 42 min

    Best 2-ride path: RideA → RideC = 9 + 11 = 20 min
    """
    travel = {
        "Entrance": {"RideA": 2, "RideB": 5,  "RideC": 4},
        "RideA":    {"RideB": 3, "RideC": 2},
        "RideB":    {"RideA": 3, "RideC": 6},
        "RideC":    {"RideA": 2, "RideB": 6},
    }
    wait = {"RideA": 5, "RideB": 10, "RideC": 8}
    dur  = {"RideA": 2, "RideB": 3,  "RideC": 1}
    return travel, wait, dur


# --------------------------------------------------------------------------- #
# Tests for _reconstruct_path                                                  #
# --------------------------------------------------------------------------- #

class TestReconstructPath:

    def test_single_ride(self):
        # mask=0b01 means only RideA (index 0) visited, no parent
        parent = [[None, None], [None, None], [None, None], [None, None]]
        result = _reconstruct_path(parent, ["RideA", "RideB"], 0b01, 0)
        assert result == ("RideA",)

    def test_two_rides(self):
        # mask=0b11: RideB (index 1) was reached from mask=0b01, index 0 (RideA)
        parent = [[None, None], [None, None], [None, None], [None, (1, 0)]]
        result = _reconstruct_path(parent, ["RideA", "RideB"], 0b11, 1)
        assert result == ("RideA", "RideB")

    def test_three_rides(self):
        # Path: RideA → RideB → RideC  (indices 0 → 1 → 2)
        # mask=0b001 (1): RideA first, no parent
        # mask=0b011 (3): RideB reached from (mask=1, index=0)
        # mask=0b111 (7): RideC reached from (mask=3, index=1)
        parent = [
            [None, None, None],  # mask 0
            [None, None, None],  # mask 1 — RideA first, parent is None
            [None, None, None],  # mask 2
            [None, (1, 0), None],# mask 3 — RideB reached from (mask=1, RideA)
            [None, None, None],  # mask 4
            [None, None, None],  # mask 5
            [None, None, None],  # mask 6
            [None, None, (3, 1)],# mask 7 — RideC reached from (mask=3, RideB)
        ]
        result = _reconstruct_path(parent, ["RideA", "RideB", "RideC"], 0b111, 2)
        assert result == ("RideA", "RideB", "RideC")

    def test_returns_tuple(self):
        parent = [[None, None], [None, None], [None, None], [None, None]]
        result = _reconstruct_path(parent, ["RideA", "RideB"], 0b01, 0)
        assert isinstance(result, tuple)


# --------------------------------------------------------------------------- #
# Tests for find_optimal_path                                                  #
# --------------------------------------------------------------------------- #

class TestFindOptimalPath:

    # --- Edge cases ---

    def test_empty_ride_list_returns_empty(self, two_rides):
        travel, wait, dur = two_rides
        result = find_optimal_path([], 60, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ()

    def test_budget_too_small_for_any_ride(self, two_rides):
        travel, wait, dur = two_rides
        # Cheapest ride (RideA) costs 9 min; budget of 8 fits nothing
        result = find_optimal_path(["RideA", "RideB"], 8, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ()

    def test_returns_tuple(self, two_rides):
        travel, wait, dur = two_rides
        result = find_optimal_path(["RideA"], 60, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert isinstance(result, tuple)

    # --- Single ride ---

    def test_single_ride_fits(self, two_rides):
        travel, wait, dur = two_rides
        result = find_optimal_path(["RideA"], 60, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ("RideA",)

    def test_single_ride_exact_budget(self, two_rides):
        # Budget exactly equals cost of RideA (9 min)
        travel, wait, dur = two_rides
        result = find_optimal_path(["RideA"], 9, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ("RideA",)

    def test_single_ride_one_under_budget(self, two_rides):
        # Budget one minute short of RideA (9 min)
        travel, wait, dur = two_rides
        result = find_optimal_path(["RideA"], 8, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ()

    # --- Two rides: visit count ---

    def test_both_rides_fit(self, two_rides):
        travel, wait, dur = two_rides
        # RideA→RideB = 25 min; budget of 25 fits both
        result = find_optimal_path(["RideA", "RideB"], 25, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert len(result) == 2
        assert set(result) == {"RideA", "RideB"}

    def test_only_one_ride_fits(self, two_rides):
        travel, wait, dur = two_rides
        # Budget 20: both single rides fit (9 and 18) but no pair fits (25+)
        result = find_optimal_path(["RideA", "RideB"], 20, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert len(result) == 1

    # --- Two rides: tiebreaker (shortest time wins) ---

    def test_tiebreaker_picks_shorter_path(self, two_rides):
        travel, wait, dur = two_rides
        # Budget 20: both RideA (9 min) and RideB (18 min) visit exactly 1 ride.
        # RideA is cheaper so it should be chosen.
        result = find_optimal_path(["RideA", "RideB"], 20, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ("RideA",)

    # --- Three rides: optimality ---

    def test_all_three_rides_fit(self, three_rides):
        travel, wait, dur = three_rides
        # Best 3-ride path costs 38 min
        result = find_optimal_path(["RideA", "RideB", "RideC"], 38, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert len(result) == 3
        assert set(result) == {"RideA", "RideB", "RideC"}

    def test_optimal_beats_greedy(self, three_rides):
        """
        Greedy (always pick cheapest next ride) gives RideA→RideC→RideB = 39 min,
        which misses the budget of 38. The DP finds RideC→RideA→RideB = 38 min,
        fitting all 3 rides.
        """
        travel, wait, dur = three_rides
        result = find_optimal_path(["RideA", "RideB", "RideC"], 38, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert len(result) == 3

    def test_two_rides_when_three_dont_fit(self, three_rides):
        travel, wait, dur = three_rides
        # Budget 37: best 3-ride path (38 min) is just over; best 2-ride is RideA→RideC (20 min)
        result = find_optimal_path(["RideA", "RideB", "RideC"], 37, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert len(result) == 2

    def test_correct_order_three_rides(self, three_rides):
        travel, wait, dur = three_rides
        # The globally optimal 3-ride path is RideC→RideA→RideB (38 min)
        result = find_optimal_path(["RideA", "RideB", "RideC"], 38, _travel_times=travel, _wait_times=wait, _durations=dur)
        assert result == ("RideC", "RideA", "RideB")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
