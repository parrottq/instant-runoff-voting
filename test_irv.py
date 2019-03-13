import pytest

import irv


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


    assert election([[1]]*3 + [[3]]*2) == (1, [{1: 3, 3: 2}, {1: 3}])
    assert election([
        [2, 1, 4],
        [2, 1, 4],
        [3, 1],
        [3, 1],
        [1, 2]
        ]) == (2, [{1: 1, 2: 2, 3: 2, 4: 0}, {1: 1, 2: 2, 3: 2}, {2: 3, 3: 2}, {2: 3}])

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
        ]) == (1, [{1: 4, 2: 1, 3: 1, 4: 1}, {1: 4}])

def test_colume_sperator():
    sep = irv.colume_seperator

    def dummy():
        yield ["1", "2", "3"]
        yield ["2", "3", "4"]

    assert [
            {"a": "1", "b": "2"},
            {"a": "2", "b": "3"}
            ] == list(sep(["a", "b"], ["a", "b", "c"], dummy()))

def test_format_ballot():
    fballot = irv.format_ballot

    assert fballot({"a": "", "b": "", "c": ""}) == []
    assert fballot({"a": "1", "b": "2", "c": "3"}) == ["a", "b", "c"]
    assert fballot({"a": "", "b": "2", "c": "3"}) == ["b", "c"]
    assert fballot({"a": "letters"}) == []
    assert fballot({"a": "2", "b": "", "c": "4"}) == ["a", "c"]

def test_generate_sanket():
    san = irv.generate_sankey

    assert sorted(san(["a", [
        {"a": 4, "b": 3, "c": 2},
        {"a": 5, "b": 4},
        {"a": 5}]]
        ).split('\n')) == sorted("a (1) [4] a (2)\nb (1) [3] b (2)\nc (1) [1] a (2)\nc (1) [1] b (2)\na (2) [5] a (3)".split('\n'))

    assert sorted(san(["a", [
        {"a": 4, "b": 3, "c": 2},
        {"a": 5, "b": 3},
        {"a": 5}]]
        ).split('\n')) == sorted("a (1) [4] a (2)\nb (1) [3] b (2)\nc (1) [1] a (2)\na (2) [5] a (3)".split('\n'))

    assert sorted(san(["a", [
        {"a": 4, "b": 3, "c": 2, "d": 3},
        {"a": 5, "b": 4, "d": 3},
        {"a": 7, "b": 5},
        {"a": 9}]]
        ).split('\n')) == sorted(
                """a (1) [4] a (2)\nb (1) [3] b (2)\nc (1) [1] a (2)\nc (1) [1] b (2)\nd (1) [3] d (2)
a (2) [5] a (3)\nb (2) [4] b (3)\nd (2) [2] a (3)\nd (2) [1] b (3)\na (3) [7] a (4)\nb (3) [2] a (4)""".split('\n'))
