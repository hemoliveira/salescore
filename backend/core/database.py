import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from typing import Any, Sequence, TypeAlias

from core.settings import get_settings
from core.logger import Logger

logger = Logger.get_logger(__name__)

QueryParams: TypeAlias = (
    Sequence[Any] | dict[str, Any] | None
)


class DatabaseManager:
    _pool: ConnectionPool | None = None

    @classmethod
    def init_pool(cls, pool_size: int = 5, min_size: int = 1) -> None:
        """
        Initializes the PostgreSQL connection pool.
        Must be called once at application startup.
        """
        if cls._pool is not None:
            return

        if pool_size <= 0:
            raise ValueError("pool_size must be greater than zero")

        try:
            settings = get_settings()
            cls._pool = ConnectionPool(
                conninfo=settings.database_url.get_secret_value(),
                min_size=min_size,
                max_size=pool_size,
                # Opened lazily (in the background) instead of blocking startup
                # on `min_size` synchronous connections - shortens cold start.
                open=False,
                kwargs={"row_factory": dict_row, "connect_timeout": 10}
            )
            cls._pool.open(wait=False)
            logger.info("PostgreSQL connection pool initialized.")
        except Exception as e:
            logger.exception("Failed to initialize PostgreSQL pool")
            raise RuntimeError("Database pool initialization failed") from e

    @classmethod
    def get_connection(cls) -> psycopg.Connection:
        """
        Retrieves a connection from the pool.
        """
        if cls._pool is None:
            cls.init_pool()

        if cls._pool is None:
            raise RuntimeError("Database pool is not initialized")

        try:
            return cls._pool.getconn()
        except Exception as e:
            logger.exception("Could not get connection from pool")
            raise RuntimeError("Database connection error") from e

    @classmethod
    def release_connection(cls, connection: psycopg.Connection) -> None:
        """
        Returns a connection obtained via get_connection() back to the pool.
        """
        if cls._pool is not None:
            cls._pool.putconn(connection)

    @classmethod
    def close_pool(cls) -> None:
        """
        Closes the database connection pool.
        """
        if cls._pool is None:
            return

        try:
            cls._pool.close()
            logger.info("Database connection pool closed.")
        except Exception as e:
            logger.warning("Could not explicitly close database connection pool: %s", e)
        finally:
            cls._pool = None

    @staticmethod
    def _execute_write(
        query: str,
        params: QueryParams = None,
        *,
        operation: str,
        return_lastrowid: bool = False,
        conn: psycopg.Connection | None = None,
    ) -> int:
        own_connection = conn is None
        connection = conn or DatabaseManager.get_connection()
        cursor = None

        try:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            last_id = 0
            if return_lastrowid:
                row = cursor.fetchone()
                if row:
                    last_id = int(list(row.values())[0])

            if own_connection:
                connection.commit()

            if return_lastrowid:
                return last_id
            return int(cursor.rowcount)

        except Exception as e:
            if own_connection:
                connection.rollback()
            logger.exception("%s operation failed", operation)
            raise RuntimeError(f"Database {operation} error") from e

        finally:
            if cursor is not None:
                cursor.close()
            if own_connection and DatabaseManager._pool is not None:
                DatabaseManager._pool.putconn(connection)

    @staticmethod
    def _execute_read(
        query: str,
        params: QueryParams = None,
        *,
        fetch_one: bool = False,
        conn: psycopg.Connection | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        own_connection = conn is None
        connection = conn or DatabaseManager.get_connection()
        cursor = None

        try:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            return result

        except Exception as e:
            logger.exception("Read operation failed")
            raise RuntimeError("Database read error") from e

        finally:
            if cursor is not None:
                cursor.close()
            if own_connection and DatabaseManager._pool is not None:
                DatabaseManager._pool.putconn(connection)

    @staticmethod
    def execute_insert(
        query: str,
        params: QueryParams = None,
        conn: psycopg.Connection | None = None,
    ) -> int:
        return DatabaseManager._execute_write(
            query,
            params,
            operation="INSERT",
            return_lastrowid=True,
            conn=conn,
        )

    @staticmethod
    def execute_update(
        query: str,
        params: QueryParams = None,
        conn: psycopg.Connection | None = None,
    ) -> int:
        return DatabaseManager._execute_write(
            query,
            params,
            operation="UPDATE",
            conn=conn,
        )

    @staticmethod
    def execute_delete(
        query: str,
        params: QueryParams = None,
        conn: psycopg.Connection | None = None,
    ) -> int:
        return DatabaseManager._execute_write(
            query,
            params,
            operation="DELETE",
            conn=conn,
        )

    @staticmethod
    def fetch_all(
        query: str,
        params: QueryParams = None,
        conn: psycopg.Connection | None = None,
    ) -> list[dict[str, Any]]:
        result = DatabaseManager._execute_read(
            query,
            params,
            fetch_one=False,
            conn=conn,
        )
        return result if isinstance(result, list) else []

    @staticmethod
    def fetch_one(
        query: str,
        params: QueryParams = None,
        conn: psycopg.Connection | None = None,
    ) -> dict[str, Any] | None:
        result = DatabaseManager._execute_read(
            query,
            params,
            fetch_one=True,
            conn=conn,
        )
        return result if isinstance(result, dict) else None
