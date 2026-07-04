from typing import Any

from core.database import DatabaseManager
from core.logger import Logger
from models.order import Order
from models.order_item import OrderItem

logger = Logger.get_logger(__name__)


class OrderRepository:
    TABLE = "tb_orders"
    PK = "order_id"

    def create(self, order: Order) -> int:
        """
        Create a new order with its items and return the generated order ID.
        """
        if not order.items:
            raise ValueError("Order must contain at least one item")

        conn = None
        cursor = None

        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            sql_customer = """
                SELECT 1
                FROM tb_customers
                WHERE customer_id = %s
                  AND deleted_at IS NULL
            """
            cursor.execute(sql_customer, (order.customer_id,))
            customer_row = cursor.fetchone()

            if not customer_row:
                raise ValueError(f"Customer {order.customer_id} not found or inactive")

            sql_order = f"""
                INSERT INTO {self.TABLE} (customer_id, order_date)
                VALUES (%s, %s)
                RETURNING order_id
            """
            cursor.execute(sql_order, (order.customer_id, order.order_date))
            row = cursor.fetchone()
            order_id = row["order_id"]


            sql_product = """
                SELECT price
                FROM tb_products
                WHERE product_id = %s
                  AND deleted_at IS NULL
            """

            sql_item = """
                INSERT INTO tb_order_items (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    total
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            for item in order.items:
                if item.product_id is None or item.product_id <= 0:
                    raise ValueError("Item must have a valid product_id")

                if item.quantity <= 0:
                    raise ValueError("Quantity must be greater than zero")

                cursor.execute(sql_product, (item.product_id,))
                product_row = cursor.fetchone()

                if not product_row:
                    raise ValueError(f"Product {item.product_id} not found or inactive")

                unit_price = product_row["price"]
                total = unit_price * item.quantity

                cursor.execute(
                    sql_item,
                    (
                        order_id,
                        item.product_id,
                        item.quantity,
                        unit_price,
                        total,
                    ),
                )

                item.order_id = order_id
                item.unit_price = unit_price
                item.total = total

            conn.commit()
            order.order_id = order_id
            return order_id

        except Exception:
            if conn:
                conn.rollback()
            logger.exception("Failed to create order")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                DatabaseManager.release_connection(conn)

    def find_all(self) -> list[Order]:
        """
        Return all active orders with their active items.
        """
        query = """
            SELECT
                o.order_id,
                o.customer_id,
                o.order_date,
                o.created_at,
                o.updated_at,
                o.deleted_at,
                i.item_id,
                i.product_id,
                i.quantity,
                i.unit_price,
                i.total,
                i.created_at AS item_created_at,
                i.updated_at AS item_updated_at,
                i.deleted_at AS item_deleted_at
            FROM tb_orders o
            LEFT JOIN tb_order_items i
                ON o.order_id = i.order_id
               AND i.deleted_at IS NULL
            WHERE o.deleted_at IS NULL
            ORDER BY o.order_id, i.item_id
        """

        rows = DatabaseManager.fetch_all(query)
        return self._map_orders_with_items(rows)

    def find_by_id(self, order_id: int) -> Order | None:
        """
        Return one active order with its active items, or None if not found.
        """
        self._validate_order_id(order_id)

        query = """
            SELECT
                o.order_id,
                o.customer_id,
                o.order_date,
                o.created_at,
                o.updated_at,
                o.deleted_at,
                i.item_id,
                i.product_id,
                i.quantity,
                i.unit_price,
                i.total,
                i.created_at AS item_created_at,
                i.updated_at AS item_updated_at,
                i.deleted_at AS item_deleted_at
            FROM tb_orders o
            LEFT JOIN tb_order_items i
                ON o.order_id = i.order_id
               AND i.deleted_at IS NULL
            WHERE o.order_id = %s
              AND o.deleted_at IS NULL
            ORDER BY i.item_id
        """

        rows = DatabaseManager.fetch_all(query, (order_id,))
        orders = self._map_orders_with_items(rows)
        return orders[0] if orders else None

    def delete(self, order_id: int) -> bool:
        """
        Soft-delete an order and its items.
        """
        self._validate_order_id(order_id)

        conn = None
        cursor = None

        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            sql_items = """
                UPDATE tb_order_items
                SET deleted_at = NOW(),
                    updated_at = NOW()
                WHERE order_id = %s
                  AND deleted_at IS NULL
            """
            cursor.execute(sql_items, (order_id,))

            sql_order = f"""
                UPDATE {self.TABLE}
                SET deleted_at = NOW(),
                    updated_at = NOW()
                WHERE {self.PK} = %s
                  AND deleted_at IS NULL
            """
            cursor.execute(sql_order, (order_id,))
            affected_orders = cursor.rowcount

            conn.commit()
            return affected_orders > 0

        except Exception:
            if conn:
                conn.rollback()
            logger.exception("Failed to delete order %s", order_id)
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                DatabaseManager.release_connection(conn)

    @staticmethod
    def _map_orders_with_items(rows: list[dict[str, Any]]) -> list[Order]:
        """
        Convert joined order/item rows into Order objects with nested items.
        """
        orders_by_id: dict[int, Order] = {}

        for row in rows:
            order_id = row["order_id"]

            if order_id not in orders_by_id:
                orders_by_id[order_id] = Order(
                    order_id=row["order_id"],
                    customer_id=row["customer_id"],
                    order_date=row["order_date"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    deleted_at=row["deleted_at"],
                )

            if row.get("item_id") is not None:
                item = OrderItem(
                    item_id=row["item_id"],
                    order_id=row["order_id"],
                    product_id=row["product_id"],
                    quantity=row["quantity"],
                    unit_price=row["unit_price"],
                    total=row["total"],
                    created_at=row["item_created_at"],
                    updated_at=row["item_updated_at"],
                    deleted_at=row["item_deleted_at"],
                )
                orders_by_id[order_id].add_item(item)

        return list(orders_by_id.values())

    @staticmethod
    def _validate_order_id(order_id: int | None) -> None:
        if order_id is None:
            raise ValueError("order_id is required.")

        if order_id <= 0:
            raise ValueError("order_id must be greater than zero.")

    @staticmethod
    def _validate_item_id(item_id: int | None) -> None:
        if item_id is None:
            raise ValueError("item_id is required.")

        if item_id <= 0:
            raise ValueError("item_id must be greater than zero.")

    def update(self, order: Order) -> bool:
        """
        Update an existing order header.
        """
        self._validate_order_id(order.order_id)

        query = f"""
            UPDATE {self.TABLE}
            SET customer_id = %s,
                order_date = %s,
                updated_at = NOW()
            WHERE {self.PK} = %s
              AND deleted_at IS NULL
        """

        affected_rows = DatabaseManager.execute_update(
            query,
            (
                order.customer_id,
                order.order_date,
                order.order_id,
            ),
        )

        return affected_rows > 0

    def add_item(self, order_id: int, item: OrderItem) -> int:
        """
        Add a new item to an existing active order.
        """
        self._validate_order_id(order_id)

        conn = None
        cursor = None

        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 1
                FROM tb_orders
                WHERE order_id = %s
                  AND deleted_at IS NULL
                """,
                (order_id,),
            )

            if not cursor.fetchone():
                raise ValueError(f"Order {order_id} not found or inactive")

            cursor.execute(
                """
                SELECT price
                FROM tb_products
                WHERE product_id = %s
                  AND deleted_at IS NULL
                """,
                (item.product_id,),
            )

            product_row = cursor.fetchone()

            if not product_row:
                raise ValueError(f"Product {item.product_id} not found or inactive")

            unit_price = product_row["price"]
            total = unit_price * item.quantity

            cursor.execute(
                """
                INSERT INTO tb_order_items (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    total
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING item_id
                """,
                (
                    order_id,
                    item.product_id,
                    item.quantity,
                    unit_price,
                    total,
                ),
            )

            row = cursor.fetchone()
            item_id = int(row["item_id"] if row else 0)

            cursor.execute(
                """
                UPDATE tb_orders
                SET updated_at = NOW()
                WHERE order_id = %s
                """,
                (order_id,),
            )

            conn.commit()

            item.item_id = item_id
            item.order_id = order_id
            item.unit_price = unit_price
            item.total = total

            return item_id

        except Exception:
            if conn:
                conn.rollback()
            logger.exception("Failed to add item to order %s", order_id)
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                DatabaseManager.release_connection(conn)

    def remove_item(self, order_id: int, item_id: int) -> bool:
        """
        Soft-delete one item from an active order.
        """
        self._validate_order_id(order_id)
        self._validate_item_id(item_id)

        conn = None
        cursor = None

        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE tb_order_items
                SET deleted_at = NOW(),
                    updated_at = NOW()
                WHERE item_id = %s
                  AND order_id = %s
                  AND deleted_at IS NULL
                """,
                (item_id, order_id),
            )

            affected_rows = cursor.rowcount

            cursor.execute(
                """
                UPDATE tb_orders
                SET updated_at = NOW()
                WHERE order_id = %s
                  AND deleted_at IS NULL
                """,
                (order_id,),
            )

            conn.commit()
            return affected_rows > 0

        except Exception:
            if conn:
                conn.rollback()
            logger.exception(
                "Failed to remove item %s from order %s", item_id, order_id
            )
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                DatabaseManager.release_connection(conn)
