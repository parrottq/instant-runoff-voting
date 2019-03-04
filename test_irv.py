import pytest

import irv


def test_is_valid_vote():

    """
    Valid format or does it need processing

    Least important to most
    """

    is_valid = irv.is_valid_vote

    # No preferences are left
    assert is_valid([]) == False

    # Next vote is not greater than zero
    assert is_valid([0,2]) == False
    assert is_valid([0]) == False
    assert is_valid([4, 0]) == False
    assert is_valid([2, 0, 4]) == False
    assert is_valid([3, 5, 2]) == True

    # All types must be numbers
    assert is_valid([None,2]) == False
    assert is_valid([None]) == False
    assert is_valid([4, None]) == False
    assert is_valid([2, None, 4]) == False
    assert is_valid([3, 5, 2]) == True

def test_process_votes():
    process = irv.process_votes

    # Remove zeros and none numbers
    assert process([0, 4]) == [4]
    assert process([5, None, 6]) == [5, 6]
    assert process([4, 6, 2]) == [4, 6, 2]

def test_round_tally():
    tally = irv.round_tally

    assert tally([[2]] * 4 + [[5]] * 2) == ({2: 4, 5: 2}, 6)
    assert tally([[2, 4, 6]] * 1 + [[6, 4, 5]]* 2) == ({2: 1, 6: 2, 4: 0, 5: 0}, 3)
    assert tally([[1]]) == ({1: 1}, 1)

    # Votes that are not in any first choise
    assert tally([[1, 2], [3, 1, 2], [3, 2]]) == ({1:1, 2: 0, 3: 2}, 3)

def test_lowest_candidate():
    lowest = irv.lowest_candidate

    assert lowest({1: 4, 2: 2, 3: 5}) == [2]
    assert lowest({1: 4, 2: 4, 3: 5}) == [1, 2]
    assert lowest({1: 4, 2: 4}) == [1, 2]


def test_majority_present():
    maj = irv.majority_present

    assert maj({1: 2, 2: 2}, 6) == False
    assert maj({1: 3, 2: 1}, 4) == 1
    assert maj({1: 3}, 5) == 1
    assert maj({1: 1}, 9) == False


def test_remove_candidate():
    rem = irv.remove_candidate

    assert rem(1, [[1, 2], [2, 1], [3, 4, 4]]) == [[2], [2], [3, 4, 4]]


def test_election():
    election = irv.election


    assert election([[1]]*3 + [[3]]*2) == (1, [{1: 3, 3: 2}])
    assert election([
        [2, 1, 4],
        [2, 1, 4],
        [3, 1],
        [3, 1],
        [1, 2]
        ]) == (2, [{1: 1, 2: 2, 3: 2, 4: 0}, {1: 1, 2: 2, 3: 2}, {2: 3, 3: 2}])

    assert election([
        [3, 1],
        [2],
        [2],
        [2],
        [1],
        [1]
        ]) == (2, [{1: 2, 2: 3, 3: 1}, {1: 3, 2: 3}, {2: 3}])

    assert election([
        [1],
        [1],
        [1],
        [1],
        [2],
        [3],
        [4]
        ]) == (1, [{1: 4, 2: 1, 3: 1, 4: 1}])

def test_colume_sperator():
    sep = irv.colume_seperator

    def dummy():
        yield ["1", "2", "3"]
        yield ["2", "3", "4"]

    assert [
            {"a": "1", "b": "2"},
            {"a": "2", "b": "3"}
            ] == list(sep(["a", "b"], ["a", "b", "c"], dummy()))
