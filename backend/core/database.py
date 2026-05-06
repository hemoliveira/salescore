from mysql.connector import Error, MySQLConnection
from mysql.connector.types import MySQLConvertibleType
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

from typing import Any, Sequence, TypeAlias, cast

from core.settings import get_settings
from core.logger import Logger

logger = Logger.get_logger(__name__)

QueryParams: TypeAlias = (
    Sequence[MySQLConvertibleType] | dict[str, MySQLConvertibleType] | None
)


class DatabaseManager:
    _pool: MySQLConnectionPool | None = None

    @classmethod
    def init_pool(cls, pool_size: int = 5) -> None:
        """
        Initializes the MySQL connection pool.
        Must be called once at application startup.
        """
        if cls._pool is not None:
            return

        if pool_size <= 0:
            raise ValueError("pool_size must be greater than zero")

        try:
            settings = get_settings()
            cls._pool = MySQLConnectionPool(
                pool_name="app_pool",
                pool_size=pool_size,
                host=settings.db_host,
                user=settings.db_user,
                password=settings.db_pass.get_secret_value(),
                database=settings.db_name,
                port=settings.db_port,
                charset="utf8mb4",
                use_unicode=True,
                connection_timeout=10,
                autocommit=False,
            )
            logger.info("Connection pool initialized with size %s", pool_size)
        except Error as e:
            logger.exception("Failed to initialize MySQL pool")
            raise RuntimeError("Database pool initialization failed") from e

    @classmethod
    def get_connection(cls) -> PooledMySQLConnection:
        """
        Retrieves a connection from the pool.
        """
        if cls._pool is None:
            cls.init_pool()

        if cls._pool is None:
            raise RuntimeError("Database pool is not initialized")

        try:
            return cls._pool.get_connection()
        except Error as e:
            logger.exception("Could not get connection from pool")
            raise RuntimeError("Database connection error") from e

    @classmethod
    def close_pool(cls) -> None:
        """
        Closes idle connections in the pool.
        Should be called during application shutdown.
        """
        if cls._pool is None:
            return

        try:
            closed_connections = cls._pool._remove_connections()
            logger.info(
                "Database connection pool closed (%s connections)",
                closed_connections,
            )
        finally:
            cls._pool = None

    @staticmethod
    def _execute_write(
        query: str,
        params: QueryParams = None,
        *,
        operation: str,
        return_lastrowid: bool = False,
        conn: MySQLConnection | None = None,
    ) -> int:
        """
        Executes INSERT, UPDATE, or DELETE statements.

        If conn is provided, the caller controls commit/rollback.
        If conn is not provided, this method manages the transaction itself.
        """
        own_connection = conn is None
        connection = conn or DatabaseManager.get_connection()
        cursor = connection.cursor()

        try:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            if own_connection:
                connection.commit()

            if return_lastrowid:
                return int(cursor.lastrowid or 0)
            return int(cursor.rowcount)

        except Error as e:
            if own_connection:
                connection.rollback()
            logger.exception("%s operation failed", operation)
            raise RuntimeError(f"Database {operation} error") from e

        finally:
            cursor.close()
            if own_connection:
                connection.close()

    @staticmethod
    def _execute_read(
        query: str,
        params: QueryParams = None,
        *,
        fetch_one: bool = False,
        conn: MySQLConnection | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """
        Executes SELECT statements and returns dictionary-based results.

        If conn is provided, it reuses the existing connection.
        """
        own_connection = conn is None
        connection = conn or DatabaseManager.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            result = cursor.fetchone() if fetch_one else cursor.fetchall()

            return (
                cast(dict[str, Any] | None, result)
                if fetch_one
                else cast(list[dict[str, Any]], result)
            )

        except Error as e:
            logger.exception("Read operation failed")
            raise RuntimeError("Database read error") from e

        finally:
            cursor.close()
            if own_connection:
                connection.close()

    @staticmethod
    def execute_insert(
        query: str,
        params: QueryParams = None,
        conn: MySQLConnection | None = None,
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
        conn: MySQLConnection | None = None,
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
        conn: MySQLConnection | None = None,
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
        conn: MySQLConnection | None = None,
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
        conn: MySQLConnection | None = None,
    ) -> dict[str, Any] | None:
        result = DatabaseManager._execute_read(
            query,
            params,
            fetch_one=True,
            conn=conn,
        )
        return result if isinstance(result, dict) else None
