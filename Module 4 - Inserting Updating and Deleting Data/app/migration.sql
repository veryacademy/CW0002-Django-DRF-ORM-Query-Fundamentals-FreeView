BEGIN;

--
-- Create model PromotionEvent
--
CREATE TABLE
    "inventory_promotionevent" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" varchar(50) NOT NULL UNIQUE,
        "start_date" datetime NOT NULL,
        "end_date" datetime NOT NULL,
        "price_reduction" integer NOT NULL
    );

--
-- Create model User
--
CREATE TABLE
    "inventory_user" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "username" varchar(50) NOT NULL UNIQUE,
        "email" varchar(255) NOT NULL UNIQUE,
        "password" varchar(60) NOT NULL
    );

--
-- Create model Category
--
CREATE TABLE
    "inventory_category" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" varchar(50) NOT NULL UNIQUE,
        "slug" varchar(55) NOT NULL UNIQUE,
        "is_active" bool NOT NULL,
        "level" smallint NOT NULL,
        "parent_id" bigint NULL REFERENCES "inventory_category" ("id") DEFERRABLE INITIALLY DEFERRED
    );

--
-- Create model Product
--
CREATE TABLE
    "inventory_product" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" varchar(50) NOT NULL UNIQUE,
        "slug" varchar(55) NOT NULL UNIQUE,
        "description" text NULL,
        "is_digital" bool NOT NULL,
        "is_active" bool NOT NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NULL,
        "price" decimal NOT NULL,
        "category_id" bigint NOT NULL REFERENCES "inventory_category" ("id") DEFERRABLE INITIALLY DEFERRED
    );

--
-- Create model StockManagement
--
CREATE TABLE
    "inventory_stockmanagement" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "quantity" integer NOT NULL,
        "last_checked_at" datetime NOT NULL,
        "product_id" bigint NOT NULL UNIQUE REFERENCES "inventory_product" ("id") DEFERRABLE INITIALLY DEFERRED
    );

--
-- Create model Order
--
CREATE TABLE
    "inventory_order" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL,
        "user_id" bigint NOT NULL REFERENCES "inventory_user" ("id") DEFERRABLE INITIALLY DEFERRED
    );

--
-- Create model OrderProduct
--
CREATE TABLE
    "inventory_orderproduct" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "quantity" integer NOT NULL,
        "order_id" bigint NOT NULL REFERENCES "inventory_order" ("id") DEFERRABLE INITIALLY DEFERRED,
        "product_id" bigint NOT NULL REFERENCES "inventory_product" ("id") DEFERRABLE INITIALLY DEFERRED
    );

--
-- Create model ProductPromotionEvent
--
CREATE TABLE
    "inventory_productpromotionevent" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "product_id" bigint NOT NULL REFERENCES "inventory_product" ("id") DEFERRABLE INITIALLY DEFERRED,
        "promotion_event_id" bigint NOT NULL REFERENCES "inventory_promotionevent" ("id") DEFERRABLE INITIALLY DEFERRED
    );

COMMIT;