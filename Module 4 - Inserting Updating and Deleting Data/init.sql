-- Create all tables
CREATE TABLE inventory_category (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES inventory_category(id) ON DELETE RESTRICT,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(55) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    level SMALLINT NOT NULL DEFAULT 0
);

CREATE TABLE inventory_promotionevent (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    price_reduction INTEGER NOT NULL
);

CREATE TABLE inventory_product (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES inventory_category(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(55) NOT NULL UNIQUE,
    description TEXT,
    is_digital BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE inventory_productpromotionevent (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES inventory_product(id) ON DELETE CASCADE,
    promotion_event_id INTEGER NOT NULL REFERENCES inventory_promotionevent(id) ON DELETE CASCADE
);

CREATE TABLE inventory_stockmanagement (
    id SERIAL PRIMARY KEY,
    product_id INTEGER UNIQUE REFERENCES inventory_product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    last_checked_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE inventory_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL
);

CREATE TABLE inventory_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES inventory_user(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE inventory_orderproduct (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES inventory_order(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES inventory_product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL
);

-- Load data into tables
COPY inventory_category (id, parent_id, name, slug, is_active, level)
FROM '/data/category.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_promotionevent (id, name, start_date, end_date, price_reduction)
FROM '/data/promotionevent.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_product (id, category_id, name, slug, description, is_digital, is_active, created_at, updated_at, price)
FROM '/data/product.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_productpromotionevent (id, product_id, promotion_event_id)
FROM '/data/productpromotionevent.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_stockmanagement (id, product_id, quantity, last_checked_at)
FROM '/data/stockmanagement.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_user (id, username, email, password)
FROM '/data/user.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_order (id, user_id, created_at, updated_at)
FROM '/data/order.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_orderproduct (id, order_id, product_id, quantity)
FROM '/data/orderproduct.csv'
DELIMITER ','
CSV HEADER;