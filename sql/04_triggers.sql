-- Postgres compatible triggers script for Neon

-- 1. Helper function to update updated_at automatically on row updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Bind the helper function to update updated_at for all core tables
CREATE TRIGGER trg_customers_updated_at
    BEFORE UPDATE ON tb_customers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_products_updated_at
    BEFORE UPDATE ON tb_products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_orders_updated_at
    BEFORE UPDATE ON tb_orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_order_items_updated_at
    BEFORE UPDATE ON tb_order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- 2. Audit logs functions and triggers
-- Customers Audit
CREATE OR REPLACE FUNCTION log_customers_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_customers', 'INSERT', NEW.customer_id, 'system_integration');
    ELSIF (TG_OP = 'UPDATE') THEN
        IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_customers', 'SOFT_DELETE', NEW.customer_id, 'system_integration');
        ELSE
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_customers', 'UPDATE', NEW.customer_id, 'system_integration');
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_customers_audit
    AFTER INSERT OR UPDATE ON tb_customers
    FOR EACH ROW
    EXECUTE FUNCTION log_customers_audit();


-- Products Audit
CREATE OR REPLACE FUNCTION log_products_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_products', 'INSERT', NEW.product_id, 'system_integration');
    ELSIF (TG_OP = 'UPDATE') THEN
        IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_products', 'SOFT_DELETE', NEW.product_id, 'system_integration');
        ELSE
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_products', 'UPDATE', NEW.product_id, 'system_integration');
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_products_audit
    AFTER INSERT OR UPDATE ON tb_products
    FOR EACH ROW
    EXECUTE FUNCTION log_products_audit();


-- Orders Audit
CREATE OR REPLACE FUNCTION log_orders_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_orders', 'INSERT', NEW.order_id, 'system_integration');
    ELSIF (TG_OP = 'UPDATE') THEN
        IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_orders', 'SOFT_DELETE', NEW.order_id, 'system_integration');
        ELSE
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_orders', 'UPDATE', NEW.order_id, 'system_integration');
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_audit
    AFTER INSERT OR UPDATE ON tb_orders
    FOR EACH ROW
    EXECUTE FUNCTION log_orders_audit();


-- Order Items Audit
CREATE OR REPLACE FUNCTION log_order_items_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_order_items', 'INSERT', NEW.item_id, 'system_integration');
    ELSIF (TG_OP = 'UPDATE') THEN
        IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_order_items', 'SOFT_DELETE', NEW.item_id, 'system_integration');
        ELSE
            INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
            VALUES ('tb_order_items', 'UPDATE', NEW.item_id, 'system_integration');
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_items_audit
    AFTER INSERT OR UPDATE ON tb_order_items
    FOR EACH ROW
    EXECUTE FUNCTION log_order_items_audit();