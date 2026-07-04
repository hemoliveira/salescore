-- Postgres compatible functions script for Neon

-- Formats currency values and handles NULL inputs
CREATE OR REPLACE FUNCTION fn_format_currency(amount DECIMAL(15,2))
RETURNS VARCHAR(30) AS $$
BEGIN
    RETURN '$ ' || to_char(COALESCE(amount, 0.00), 'FM999,999,999.00');
END;
$$ LANGUAGE plpgsql;

-- Formats dates and handles NULL inputs
CREATE OR REPLACE FUNCTION fn_format_date(d DATE)
RETURNS VARCHAR(20) AS $$
BEGIN
    IF d IS NULL THEN
        RETURN 'N/A';
    END IF;

    RETURN to_char(d, 'Mon DD, YYYY');
END;
$$ LANGUAGE plpgsql;