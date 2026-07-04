from core.database import DatabaseManager
from models.product import Product


class ProductRepository:
    TABLE = "tb_products"
    VIEW = "vw_active_products"
    PK = "product_id"

    def create(self, product: Product) -> int:
        """
        Insert a new product and return the generated ID.
        """
        query = f"""
            INSERT INTO {self.TABLE} (name, category, price)
            VALUES (%s, %s, %s)
            RETURNING product_id
        """

        new_id = DatabaseManager.execute_insert(
            query,
            (
                product.name,
                product.category,
                product.price,
            ),
        )

        product.product_id = new_id
        return new_id

    def find_all(self) -> list[Product]:
        """
        Return all active products.
        """
        query = f"""
            SELECT *
            FROM {self.VIEW}
            ORDER BY name
        """

        rows = DatabaseManager.fetch_all(query)
        return [Product.from_dict(row) for row in rows]

    def find_by_id(self, product_id: int) -> Product | None:
        """
        Return one active product by ID, or None if not found.
        """
        self._validate_product_id(product_id)

        query = f"""
            SELECT *
            FROM {self.VIEW}
            WHERE {self.PK} = %s
        """

        row = DatabaseManager.fetch_one(query, (product_id,))
        return Product.from_dict(row) if row else None

    def update(self, product: Product) -> bool:
        """
        Update an existing product.
        """
        self._validate_product_id(product.product_id)

        query = f"""
            UPDATE {self.TABLE}
            SET name = %s,
                category = %s,
                price = %s,
                updated_at = NOW()
            WHERE {self.PK} = %s
              AND deleted_at IS NULL
        """

        affected_rows = DatabaseManager.execute_update(
            query,
            (
                product.name,
                product.category,
                product.price,
                product.product_id,
            ),
        )
        return affected_rows > 0

    def delete(self, product_id: int) -> bool:
        """
        Soft delete a product by setting deleted_at.
        """
        self._validate_product_id(product_id)

        query = f"""
            UPDATE {self.TABLE}
            SET deleted_at = NOW(),
                updated_at = NOW()
            WHERE {self.PK} = %s
              AND deleted_at IS NULL
        """

        affected_rows = DatabaseManager.execute_update(query, (product_id,))
        return affected_rows > 0

    @staticmethod
    def _validate_product_id(product_id: int | None) -> None:
        if product_id is None:
            raise ValueError("product_id is required.")

        if product_id <= 0:
            raise ValueError("product_id must be greater than zero.")
