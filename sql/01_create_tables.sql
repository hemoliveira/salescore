
CREATE TABLE IF NOT EXISTS tb_customers (
    customer_id SERIAL,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,

    CONSTRAINT pk_customers PRIMARY KEY (customer_id)
);
CREATE INDEX IF NOT EXISTS idx_cust_lookup ON tb_customers (customer_id, deleted_at);

CREATE TABLE IF NOT EXISTS tb_products (
    product_id SERIAL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,

    CONSTRAINT pk_products PRIMARY KEY (product_id),
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT uq_product_name UNIQUE (name)
);
CREATE INDEX IF NOT EXISTS idx_prod_lookup ON tb_products (product_id, deleted_at);

CREATE TABLE IF NOT EXISTS tb_orders (
    order_id SERIAL,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,

    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
        REFERENCES tb_customers(customer_id)
);
CREATE INDEX IF NOT EXISTS idx_orders_active ON tb_orders (order_id, deleted_at);
CREATE INDEX IF NOT EXISTS idx_orders_date ON tb_orders (order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON tb_orders (customer_id, order_date);

CREATE TABLE IF NOT EXISTS tb_order_items (
    item_id SERIAL,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,

    CONSTRAINT pk_order_items PRIMARY KEY (item_id),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id)
        REFERENCES tb_orders(order_id),
    CONSTRAINT fk_items_product FOREIGN KEY (product_id)
        REFERENCES tb_products(product_id),
    CONSTRAINT chk_qty_positive CHECK (quantity > 0),
    CONSTRAINT chk_unit_price_positive CHECK (unit_price >= 0),
    CONSTRAINT chk_total_positive CHECK (total >= 0)
);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON tb_order_items (order_id, deleted_at);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON tb_order_items (product_id, deleted_at);

CREATE TABLE IF NOT EXISTS tb_audit_log (
    audit_id SERIAL,
    table_name VARCHAR(50) NOT NULL,
    action_name VARCHAR(30) NOT NULL,
    record_id INT NOT NULL,
    user_context VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_audit_log PRIMARY KEY (audit_id)
);
CREATE INDEX IF NOT EXISTS idx_audit_table_name ON tb_audit_log (table_name);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON tb_audit_log (created_at);