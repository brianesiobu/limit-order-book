from limit_order_book.doubly_linked_list import DoublyLinkedList
from limit_order_book.order import Order
from limit_order_book.skip_list import SkipList


class PriceLevel:
    __slots__ = ("price", "queue")

    def __init__(self, price) -> None:
        self.price = price
        self.queue = DoublyLinkedList()


class LimitOrderBook:
    def __init__(self) -> None:
        self.sell_orders = SkipList()
        self.buy_orders = SkipList()
        self.active_orders = {}
        self.filled_orders = set()

    def place_order(
        self,
        order_id,
        order_side,
        order_price,
        order_quantity,
    ):
        """
        Parameters
        ----------
        order_id : str
            A unique identifier for the order.
        order_side : {'buy', 'sell'}
            The side of the order.
        order_price : Decimal
            The price at which the order is placed.
        order_quantity : int
            The quantity of the asset to be bought or sold.

        Returns
        -------
        list of tuple
            A list of matched orders, where each tuple contains:
            (buy_order_id, sell_order_id, quantity, price).
            - If no matches occur, an empty list is returned.
            - If matches occur, each tuple represents a transaction between a buy and sell order.
        """

        order = Order(order_id, order_side, order_price, order_quantity)
        matches = []

        if order.order_side == "buy":
            while order.order_quantity > 0:
                # 1) Find lowest price level in skip list.
                best_sell_order_node = self.sell_orders.get_min()
                if not best_sell_order_node:
                    break
                best_sell_order_price = best_sell_order_node.value.price
                # 2) Check if a match is possible.
                if order.order_price >= best_sell_order_price:
                    price_level = best_sell_order_node.value
                    if price_level.queue.is_empty():
                        self.sell_orders.delete(best_sell_order_price)
                        continue
                    # 3) Process first order in doubly linked list at lowest price level.
                    resting_node = price_level.queue.head.next
                    resting_order = resting_node.data
                    matched_quantity = min(order.order_quantity, resting_order.order_quantity)
                    order.order_quantity -= matched_quantity
                    resting_order.order_quantity -= matched_quantity
                    matches.append(
                        (
                            order_id,
                            resting_order.order_id,
                            matched_quantity,
                            best_sell_order_price,
                        )
                    )
                    # 4) If match was a full match update auxiliary structures.
                    if resting_order.order_quantity == 0:
                        price_level.queue.remove(resting_node)
                        self.active_orders.pop(resting_order.order_id, None)
                        self.filled_orders.add(resting_order.order_id)
                    if price_level.queue.is_empty():
                        self.sell_orders.delete(best_sell_order_price)
                else:
                    break
            # 5) If the match was partial then the remaining
            # part of the order joins buy orders either on a new price level
            # or at then end of the queue of an existing price level.
            if order.order_quantity > 0:
                key = -order.order_price
                node = self.buy_orders.search(key)
                if not node:
                    price_level = PriceLevel(order.order_price)
                    node = self.buy_orders.insert(key, price_level)
                else:
                    price_level = node.value
                order_node = price_level.queue.append(order)
                self.active_orders[order_id] = ("buy", key, node, order_node)
            else:
                self.filled_orders.add(order_id)
            return matches

        # 6) This part is analogous to "buy logic"
        elif order.order_side == "sell":
            while order.order_quantity > 0:
                best_buy_order_node = self.buy_orders.get_min()
                if not best_buy_order_node:
                    break
                best_buy_order_price = -best_buy_order_node.key
                if order.order_price <= best_buy_order_price:
                    price_level = best_buy_order_node.value
                    if price_level.queue.is_empty():
                        self.buy_orders.delete(best_buy_order_node.key)
                        continue
                    resting_node = price_level.queue.head.next
                    resting_order = resting_node.data
                    matched_quantity = min(order.order_quantity, resting_order.order_quantity)
                    order.order_quantity -= matched_quantity
                    resting_order.order_quantity -= matched_quantity
                    matches.append(
                        (
                            resting_order.order_id,
                            order_id,
                            matched_quantity,
                            best_buy_order_price,
                        )
                    )
                    if resting_order.order_quantity == 0:
                        price_level.queue.remove(resting_node)
                        self.active_orders.pop(resting_order.order_id, None)
                        self.filled_orders.add(resting_order.order_id)
                    if price_level.queue.is_empty():
                        self.buy_orders.delete(best_buy_order_node.key)
                else:
                    break
            if order.order_quantity > 0:
                key = order.order_price
                node = self.sell_orders.search(key)
                if not node:
                    price_level = PriceLevel(order.order_price)
                    node = self.sell_orders.insert(key, price_level)
                else:
                    price_level = node.value
                order_node = price_level.queue.append(order)
                self.active_orders[order_id] = ("sell", key, node, order_node)
            else:
                self.filled_orders.add(order_id)
            return matches

    def cancel_order(self, order_id):
        """
        Cancels an order by order id.

        Parameters
        ----------
        order_id : str
            The unique identifier of the order to be canceled.

        Returns
        -------
        bool
            True if the order was successfully canceled, False if the order was not found or filled.
        """

        if order_id in self.filled_orders:
            return False

        if order_id not in self.active_orders:
            return False

        side, key, price_level_node, order_node = self.active_orders[order_id]
        price_level_node.value.queue.remove(order_node)
        del self.active_orders[order_id]

        if price_level_node.value.queue.is_empty():
            if side == "buy":
                self.buy_orders.delete(key)
            else:
                self.sell_orders.delete(key)

        return True
