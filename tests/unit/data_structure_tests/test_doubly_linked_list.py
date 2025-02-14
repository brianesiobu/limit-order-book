import pytest

from limit_order_book.doubly_linked_list import DoublyLinkedList
from limit_order_book.order import Order


@pytest.fixture
def sample_orders():
    return [
        Order(
            order_id=str(i),
            order_side="buy" if i % 2 == 0 else "sell",
            order_price=100.0 + i,
            order_quantity=10 * i,
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def doubly_linked_list():
    return DoublyLinkedList()


@pytest.fixture
def populated_list(sample_orders):
    dll = DoublyLinkedList()
    for order in sample_orders:
        dll.append(order)
    return dll


def test_is_empty_on_new_list(doubly_linked_list):
    assert doubly_linked_list.is_empty()


def test_is_empty_after_removals(populated_list, sample_orders):
    for _ in range(len(sample_orders)):
        populated_list.pop_left()
    assert populated_list.is_empty()


def test_append_to_doubly_linked_list(doubly_linked_list, sample_orders):
    node = doubly_linked_list.append(sample_orders[0])
    assert node.data == sample_orders[0]
    assert node.prev.data is None
    assert node.next.data is None
    assert not doubly_linked_list.is_empty()


def test_append_multiple_orders(doubly_linked_list, sample_orders):
    first_node = doubly_linked_list.append(sample_orders[0])
    second_node = doubly_linked_list.append(sample_orders[1])
    assert first_node.next == second_node
    assert second_node.prev == first_node
    assert second_node.next.data is None


def test_pop_left_single_element(doubly_linked_list, sample_orders):
    doubly_linked_list.append(sample_orders[0])
    popped_node = doubly_linked_list.pop_left()
    assert popped_node is not None
    assert popped_node.data == sample_orders[0]
    assert doubly_linked_list.is_empty()


def test_pop_left_multiple_elements(populated_list, sample_orders):
    for expected_order in sample_orders:
        popped_node = populated_list.pop_left()
        assert popped_node is not None
        assert popped_node.data == expected_order
    assert populated_list.is_empty()


def test_remove_first_node(doubly_linked_list, sample_orders):
    first_node = doubly_linked_list.append(sample_orders[0])
    second_node = doubly_linked_list.append(sample_orders[1])
    doubly_linked_list.remove(first_node)
    assert second_node.prev.data is None
    assert doubly_linked_list.pop_left().data == sample_orders[1]


def test_remove_middle_node(doubly_linked_list, sample_orders):
    first_node = doubly_linked_list.append(sample_orders[0])
    second_node = doubly_linked_list.append(sample_orders[1])
    third_node = doubly_linked_list.append(sample_orders[2])
    doubly_linked_list.remove(second_node)
    assert first_node.next == third_node
    assert third_node.prev == first_node
    assert doubly_linked_list.is_empty() is False


def test_remove_last_node(doubly_linked_list, sample_orders):
    first_node = doubly_linked_list.append(sample_orders[0])
    second_node = doubly_linked_list.append(sample_orders[1])
    doubly_linked_list.remove(second_node)
    assert first_node.next.data is None


def test_iterate_over_list(populated_list, sample_orders):
    extracted_orders = list(iter(populated_list))
    assert extracted_orders == sample_orders
