from typing import Any
from core.database import DatabaseManager


class DashboardRepository:
    def get_monthly_dashboard(self) -> dict[str, Any]:
        """
        Executes the monthly dashboard stored procedure and returns combined KPIs.
        """
        conn = DatabaseManager.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            # PostgreSQL calls procedure with cursors and fetches from them
            cursor.execute("CALL prc_monthly_dashboard('cur_summary', 'cur_categories', 'cur_top_customer')")

            cursor.execute("FETCH ALL FROM cur_summary")
            summary_rows = cursor.fetchall()

            cursor.execute("FETCH ALL FROM cur_categories")
            categories = cursor.fetchall()

            cursor.execute("FETCH ALL FROM cur_top_customer")
            customer_rows = cursor.fetchall()

            conn.commit()

            summary = {"monthly_revenue": "$ 0.00", "total_orders": 0}
            if summary_rows:
                summary = summary_rows[0]

            top_customer = None
            if customer_rows:
                top_customer = customer_rows[0]

            return {
                "summary": summary,
                "categories": categories,
                "top_customer": top_customer,
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            # Connection from pool must be returned
            DatabaseManager._pool.putconn(conn)

