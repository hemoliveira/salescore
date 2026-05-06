from core.database import DatabaseManager


def setup_module():
    DatabaseManager.init_pool()


def test_connection():
    row = DatabaseManager.fetch_one("SELECT 1 AS ok")
    assert row is not None
    assert row["ok"] == 1


def test_fetch_all():
    rows = DatabaseManager.fetch_all("SELECT 1 AS num UNION SELECT 2")
    assert len(rows) == 2


def test_insert_update_delete():
    # INSERT
    new_id = DatabaseManager.execute_insert(
        "INSERT INTO tb_customers (name, city) VALUES (%s, %s)",
        ("Teste Pytest", "SC"),
    )
    assert new_id > 0

    created = DatabaseManager.fetch_one(
        "SELECT name, city, deleted_at FROM tb_customers WHERE customer_id = %s",
        (new_id,),
    )
    assert created is not None
    assert created["name"] == "Teste Pytest"
    assert created["city"] == "SC"
    assert created["deleted_at"] is None

    # UPDATE
    updated = DatabaseManager.execute_update(
        """
        UPDATE tb_customers
        SET city = %s
        WHERE customer_id = %s
        """,
        ("SP", new_id),
    )
    assert updated == 1

    updated_row = DatabaseManager.fetch_one(
        "SELECT city FROM tb_customers WHERE customer_id = %s",
        (new_id,),
    )
    assert updated_row is not None
    assert updated_row["city"] == "SP"

    # SOFT DELETE
    deleted = DatabaseManager.execute_delete(
        """
        UPDATE tb_customers
        SET deleted_at = NOW()
        WHERE customer_id = %s
        """,
        (new_id,),
    )
    assert deleted == 1

    deleted_row = DatabaseManager.fetch_one(
        "SELECT deleted_at FROM tb_customers WHERE customer_id = %s",
        (new_id,),
    )
    assert deleted_row is not None
    assert deleted_row["deleted_at"] is not None
