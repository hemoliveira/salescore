DELIMITER //

-- Audit customers on insert
DROP TRIGGER IF EXISTS trg_customers_insert //
CREATE TRIGGER trg_customers_insert
AFTER INSERT ON tb_customers
FOR EACH ROW
BEGIN
    INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
    VALUES ('tb_customers', 'INSERT', NEW.customer_id, 'system_integration');
END //

-- Audit customers on update or soft delete
DROP TRIGGER IF EXISTS trg_customers_update //
CREATE TRIGGER trg_customers_update
AFTER UPDATE ON tb_customers
FOR EACH ROW
BEGIN
    IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_customers', 'SOFT_DELETE', NEW.customer_id, 'system_integration');
    ELSE
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_customers', 'UPDATE', NEW.customer_id, 'system_integration');
    END IF;
END //

-- Audit products on insert
DROP TRIGGER IF EXISTS trg_products_insert //
CREATE TRIGGER trg_products_insert
AFTER INSERT ON tb_products
FOR EACH ROW
BEGIN
    INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
    VALUES ('tb_products', 'INSERT', NEW.product_id, 'system_integration');
END //

-- Audit products on update or soft delete
DROP TRIGGER IF EXISTS trg_products_update //
CREATE TRIGGER trg_products_update
AFTER UPDATE ON tb_products
FOR EACH ROW
BEGIN
    IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_products', 'SOFT_DELETE', NEW.product_id, 'system_integration');
    ELSE
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_products', 'UPDATE', NEW.product_id, 'system_integration');
    END IF;
END //

-- Audit orders on insert
DROP TRIGGER IF EXISTS trg_orders_insert //
CREATE TRIGGER trg_orders_insert
AFTER INSERT ON tb_orders
FOR EACH ROW
BEGIN
    INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
    VALUES ('tb_orders', 'INSERT', NEW.order_id, 'system_integration');
END //

-- Audit orders on update or soft delete
DROP TRIGGER IF EXISTS trg_orders_update //
CREATE TRIGGER trg_orders_update
AFTER UPDATE ON tb_orders
FOR EACH ROW
BEGIN
    IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_orders', 'SOFT_DELETE', NEW.order_id, 'system_integration');
    ELSE
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_orders', 'UPDATE', NEW.order_id, 'system_integration');
    END IF;
END //

-- Audit order items on insert
DROP TRIGGER IF EXISTS trg_order_items_insert //
CREATE TRIGGER trg_order_items_insert
AFTER INSERT ON tb_order_items
FOR EACH ROW
BEGIN
    INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
    VALUES ('tb_order_items', 'INSERT', NEW.item_id, 'system_integration');
END //

-- Audit order items on update or soft delete
DROP TRIGGER IF EXISTS trg_order_items_update //
CREATE TRIGGER trg_order_items_update
AFTER UPDATE ON tb_order_items
FOR EACH ROW
BEGIN
    IF OLD.deleted_at IS NULL AND NEW.deleted_at IS NOT NULL THEN
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_order_items', 'SOFT_DELETE', NEW.item_id, 'system_integration');
    ELSE
        INSERT INTO tb_audit_log (table_name, action_name, record_id, user_context)
        VALUES ('tb_order_items', 'UPDATE', NEW.item_id, 'system_integration');
    END IF;
END //

DELIMITER ;