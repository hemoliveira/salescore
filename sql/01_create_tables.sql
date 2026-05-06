CREATE DATABASE IF NOT EXISTS company_sales_db;
USE company_sales_db;

CREATE TABLE IF NOT EXISTS tb_customers (
    customer_id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    CONSTRAINT pk_customers PRIMARY KEY (customer_id),

    INDEX idx_cust_lookup (customer_id, deleted_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tb_products (
    product_id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    CONSTRAINT pk_products PRIMARY KEY (product_id),
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT uq_product_name UNIQUE (name),

    INDEX idx_prod_lookup (product_id, deleted_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tb_orders (
    order_id INT AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
        REFERENCES tb_customers(customer_id),

    INDEX idx_orders_active (order_id, deleted_at),
    INDEX idx_orders_date (order_date),
    INDEX idx_orders_customer_date (customer_id, order_date)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tb_order_items (
    item_id INT AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    CONSTRAINT pk_order_items PRIMARY KEY (item_id),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id)
        REFERENCES tb_orders(order_id),
    CONSTRAINT fk_items_product FOREIGN KEY (product_id)
        REFERENCES tb_products(product_id),
    CONSTRAINT chk_qty_positive CHECK (quantity > 0),
    CONSTRAINT chk_unit_price_positive CHECK (unit_price >= 0),
    CONSTRAINT chk_total_positive CHECK (total >= 0),

    INDEX idx_order_items_order (order_id, deleted_at),
    INDEX idx_order_items_product (product_id, deleted_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tb_audit_log (
    audit_id INT AUTO_INCREMENT,
    table_name VARCHAR(50) NOT NULL,
    action_name VARCHAR(30) NOT NULL,
    record_id INT NOT NULL,
    user_context VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_audit_log PRIMARY KEY (audit_id),

    INDEX idx_audit_table_name (table_name),
    INDEX idx_audit_created_at (created_at)
) ENGINE=InnoDB;