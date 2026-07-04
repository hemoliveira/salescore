-- =============================================================
-- Script : 00_create_database.sql
-- Purpose: Create the sales_core database and its dedicated role
-- =============================================================

CREATE DATABASE sales_core
    ENCODING    = 'UTF8'
    LC_COLLATE  = 'en_US.UTF-8'
    LC_CTYPE    = 'en_US.UTF-8'
    TEMPLATE    = template0;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'salescore_app') THEN
        CREATE ROLE salescore_app
            LOGIN
            PASSWORD 'salescore_pass'
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE;
        RAISE NOTICE 'Role salescore_app created.';
    ELSE
        RAISE NOTICE 'Role salescore_app already exists — skipped.';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE sales_core TO salescore_app;

GRANT USAGE ON SCHEMA public TO salescore_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO salescore_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO salescore_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO salescore_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO salescore_app;
