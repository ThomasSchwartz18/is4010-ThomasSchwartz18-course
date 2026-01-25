import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

import lab02


def test_sum_of_evens_basic():
    assert lab02.sum_of_evens([2, 4, 5]) == 6


def test_sum_of_evens_all_odd():
    assert lab02.sum_of_evens([1, 3, 5]) == 0


def test_sum_of_evens_empty():
    assert lab02.sum_of_evens([]) == 0


def test_sum_of_evens_mixed_signs():
    assert lab02.sum_of_evens([-2, -3, 4]) == 2


def test_get_names_of_adults_basic():
    users = [
        {"name": "Ada", "age": 18},
        {"name": "Linus", "age": 17},
        {"name": "Grace", "age": 20},
    ]
    assert lab02.get_names_of_adults(users) == ["Ada", "Grace"]


def test_get_names_of_adults_empty():
    assert lab02.get_names_of_adults([]) == []


def test_calculate_area_ints():
    assert lab02.calculate_area(5, 3) == 15


def test_calculate_area_floats():
    assert lab02.calculate_area(2.5, 4) == 10.0


def test_calculate_area_invalid():
    with pytest.raises(ValueError):
        lab02.calculate_area(0, 1)
    with pytest.raises(ValueError):
        lab02.calculate_area(1, -1)
