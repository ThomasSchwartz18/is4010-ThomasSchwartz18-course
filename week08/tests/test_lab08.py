"""
Tests for FavoritesManager in lab08.

All tests use pytest's tmp_path fixture so no real favorites.json is
read or written during the test run.
"""

import json
import pytest
from lab08 import FavoritesManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_manager(tmp_path, initial=None):
    """Create a FavoritesManager backed by a temp file."""
    filepath = tmp_path / "favorites.json"
    if initial is not None:
        filepath.write_text(json.dumps(initial), encoding="utf-8")
    return FavoritesManager(filepath=filepath), filepath


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_add_favorite(tmp_path):
    mgr, _ = make_manager(tmp_path)
    result = mgr.add("home", "Cincinnati, OH")
    assert result is True
    assert mgr.get_location("home") == "Cincinnati, OH"


def test_add_duplicate_returns_false(tmp_path):
    mgr, _ = make_manager(tmp_path)
    mgr.add("home", "Cincinnati, OH")
    result = mgr.add("home", "Columbus, OH")
    assert result is False
    # Original value should be unchanged
    assert mgr.get_location("home") == "Cincinnati, OH"


def test_remove_favorite(tmp_path):
    mgr, _ = make_manager(tmp_path)
    mgr.add("work", "Columbus, OH")
    result = mgr.remove("work")
    assert result is True
    assert mgr.get_location("work") is None


def test_remove_nonexistent_returns_false(tmp_path):
    mgr, _ = make_manager(tmp_path)
    result = mgr.remove("nowhere")
    assert result is False


def test_list_all_empty(tmp_path):
    mgr, _ = make_manager(tmp_path)
    assert mgr.list_all() == {}


def test_list_all(tmp_path):
    mgr, _ = make_manager(tmp_path)
    mgr.add("home", "Cincinnati, OH")
    mgr.add("work", "Columbus, OH")
    result = mgr.list_all()
    assert result == {"home": "Cincinnati, OH", "work": "Columbus, OH"}


def test_get_location(tmp_path):
    mgr, _ = make_manager(tmp_path)
    mgr.add("nyc", "New York, NY")
    assert mgr.get_location("nyc") == "New York, NY"


def test_get_location_not_found(tmp_path):
    mgr, _ = make_manager(tmp_path)
    assert mgr.get_location("unknown") is None


def test_case_insensitive_add_and_lookup(tmp_path):
    mgr, _ = make_manager(tmp_path)
    mgr.add("Home", "Cincinnati, OH")
    # All of these should resolve to the same entry
    assert mgr.get_location("home") == "Cincinnati, OH"
    assert mgr.get_location("HOME") == "Cincinnati, OH"
    assert mgr.get_location("HoMe") == "Cincinnati, OH"


def test_case_insensitive_duplicate(tmp_path):
    mgr, _ = make_manager(tmp_path)
    mgr.add("home", "Cincinnati, OH")
    # Adding with different case should be treated as duplicate
    result = mgr.add("HOME", "Somewhere Else")
    assert result is False


def test_persistence_across_instances(tmp_path):
    mgr1, filepath = make_manager(tmp_path)
    mgr1.add("home", "Cincinnati, OH")
    mgr1.add("work", "Columbus, OH")

    # New instance reading the same file
    mgr2 = FavoritesManager(filepath=filepath)
    assert mgr2.get_location("home") == "Cincinnati, OH"
    assert mgr2.get_location("work") == "Columbus, OH"


def test_corrupted_json_file(tmp_path):
    filepath = tmp_path / "favorites.json"
    filepath.write_text("not valid json {{{{", encoding="utf-8")
    # Should not raise, should start with empty favorites
    mgr = FavoritesManager(filepath=filepath)
    assert mgr.list_all() == {}


def test_missing_file(tmp_path):
    filepath = tmp_path / "nonexistent.json"
    # File does not exist — should start empty without raising
    mgr = FavoritesManager(filepath=filepath)
    assert mgr.list_all() == {}
