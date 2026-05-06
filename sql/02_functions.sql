DELIMITER //

-- Formats currency values and handles NULL inputs
DROP FUNCTION IF EXISTS fn_format_currency //
CREATE FUNCTION fn_format_currency(amount DECIMAL(15,2))
RETURNS VARCHAR(30)
DETERMINISTIC
BEGIN
    -- Returns '$ 0.00' when the value is NULL
    RETURN CONCAT('$ ', FORMAT(COALESCE(amount, 0), 2));
END //

-- Formats dates and handles NULL inputs
DROP FUNCTION IF EXISTS fn_format_date //
CREATE FUNCTION fn_format_date(d DATE)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    IF d IS NULL THEN
        RETURN 'N/A';
    END IF;

    RETURN DATE_FORMAT(d, '%b %d, %Y');
END //

DELIMITER ;