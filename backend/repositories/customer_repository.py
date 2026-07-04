from core.database import DatabaseManager
from models.customer import Customer


class CustomerRepository:
    TABLE = "tb_customers"
    VIEW = "vw_active_customers"
    PK = "customer_id"

    def create(self, customer: Customer) -> int:
        """
        Returns the generated ID.
        """
        query = f"""
            INSERT INTO {self.TABLE} (name, city)
            VALUES (%s, %s)
            RETURNING customer_id
        """

        new_id = DatabaseManager.execute_insert(
            query,
            (customer.name, customer.city),
        )

        customer.customer_id = new_id
        return new_id

    def find_all(self) -> list[Customer]:
        """
        Returns all active customers.
        """
        query = f"""
            SELECT *
            FROM {self.VIEW}
            ORDER BY name
        """
        rows = DatabaseManager.fetch_all(query)
        return [Customer.from_dict(row) for row in rows]

    def find_by_id(self, customer_id: int) -> Customer | None:
        """
        Returns one active customer by ID, or None if not found.
        """
        self._validate_customer_id(customer_id)

        query = f"""
            SELECT *
            FROM {self.VIEW}
            WHERE {self.PK} = %s
        """
        row = DatabaseManager.fetch_one(query, (customer_id,))
        return Customer.from_dict(row) if row else None

    def update(self, customer: Customer) -> bool:
        """
        Updates an existing customer.
        """
        self._validate_customer_id(customer.customer_id)

        query = f"""
            UPDATE {self.TABLE}
            SET name = %s,
                city = %s,
                updated_at = NOW()
            WHERE {self.PK} = %s
              AND deleted_at IS NULL
        """

        affected_rows = DatabaseManager.execute_update(
            query,
            (customer.name, customer.city, customer.customer_id),
        )
        return affected_rows > 0

    def delete(self, customer_id: int) -> bool:
        """
        Soft deletes a customer by setting deleted_at.
        """
        self._validate_customer_id(customer_id)

        query = f"""
            UPDATE {self.TABLE}
            SET deleted_at = NOW(),
                updated_at = NOW()
            WHERE {self.PK} = %s
              AND deleted_at IS NULL
        """

        affected_rows = DatabaseManager.execute_update(query, (customer_id,))
        return affected_rows > 0

    @staticmethod
    def _validate_customer_id(customer_id: int | None) -> None:
        if customer_id is None:
            raise ValueError("customer_id is required.")

        if customer_id <= 0:
            raise ValueError("customer_id must be greater than zero.")
