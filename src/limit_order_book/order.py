from decimal import Decimal


class Order:
    __slots__ = ("order_id", "order_side", "order_price", "order_quantity")

    def __init__(
        self,
        order_id,
        order_side,
        order_price,
        order_quantity,
    ) -> None:
        self.order_id = order_id
        self.order_side = order_side
        self.order_price = Decimal(order_price)
        self.order_quantity = order_quantity

    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return (
            self.order_id == other.order_id
            and self.order_side == other.order_side
            and self.order_price == other.order_price
            and self.order_quantity == other.order_quantity
        )
