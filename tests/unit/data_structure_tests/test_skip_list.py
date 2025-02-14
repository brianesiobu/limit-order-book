import pytest

from limit_order_book.skip_list import SkipList


@pytest.fixture
def skip_list():
    return SkipList()


def test_insert_and_search_existing_key(skip_list):
    node = skip_list.insert(10, "ten")
    assert node is not None
    assert node.key == 10
    assert node.value == "ten"

    found = skip_list.search(10)
    assert found is not None
    assert found.key == 10
    assert found.value == "ten"


def test_search_non_existent_key(skip_list):
    assert skip_list.search(42) is None


def test_insert_duplicate_keys(skip_list):
    skip_list.insert(5, "old_value")
    skip_list.insert(5, "new_value")
    found = skip_list.search(5)
    assert found is not None
    assert found.value == "new_value"


def test_delete_existing_key(skip_list):
    skip_list.insert(20, "twenty")
    assert skip_list.search(20) is not None
    assert skip_list.delete(20) is True
    assert skip_list.search(20) is None


def test_delete_non_existent_key(skip_list):
    assert skip_list.delete(99) is False


def test_get_min_on_empty_list(skip_list):
    assert skip_list.get_min() is None


def test_get_min_after_insertions(skip_list):
    skip_list.insert(50, "fifty")
    skip_list.insert(10, "ten")
    skip_list.insert(30, "thirty")
    min_node = skip_list.get_min()
    assert min_node is not None
    assert min_node.key == 10
    assert min_node.value == "ten"


def test_get_min_after_deleting_minimum(skip_list):
    skip_list.insert(2, "two")
    skip_list.insert(10, "ten")
    skip_list.insert(5, "five")
    assert skip_list.get_min().key == 2
    skip_list.delete(2)
    assert skip_list.get_min().key == 5


def test_random_level_is_valid(skip_list):
    for _ in range(100):
        level = skip_list.random_level()
        assert isinstance(level, int)
        assert level >= 0


def test_complex_inserts_and_deletes(skip_list):
    keys = [
        380,
        905,
        258,
        318,
        218,
        238,
        321,
        784,
        799,
        67,
        808,
        132,
        300,
        840,
        703,
    ]
    for key in keys:
        skip_list.insert(key, f"value_{key}")
    for key in keys:
        assert skip_list.search(key) is not None
    for key in keys:
        assert skip_list.delete(key) is True
        assert skip_list.search(key) is None
    assert skip_list.get_min() is None
