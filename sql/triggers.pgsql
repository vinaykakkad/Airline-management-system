-- Possible triggers to create:
-- 	- Sql does not support one-one, trigger to ensure one-one between many tables


-- If the flight is direct, no of stops should be zero and layover time should be zero
-- A trigger on flight to enforce these conditions
CREATE OR REPLACE FUNCTION flight_check_zeros() RETURNS TRIGGER AS $flight_check_zeros$
BEGIN
	IF NEW.flight_type = 'direct' THEN
		IF NEW.stops != 0 OR to_char(NEW.layover_time, 'HH24:MI:SS')  != '00:00:00' THEN
			RAISE exception 'In direct flights stops and layover time should be zero';
		END IF;
	END IF;
END;
$flight_check_zeros$
LANGUAGE plpgsql;

-- CREATE TRIGGER flight_check_zeros 
-- 	BEFORE INSERT OR UPDATE 
-- 	ON Flight 
-- 	FOR EACH ROW
-- 		EXECUTE FUNCTION flight_check_zeros()


-- If a passenger register, then he should have a passpert with the email connected to it
-- A trigger on account to enforce this
CREATE OR REPLACE FUNCTION account_check_email () RETURNS TRIGGER AS $account_check_email$
DECLARE
	r_passenger Passport%rowtype;
BEGIN
	IF NEW.type = 'passenger' THEN
		SELECT * FROM passport INTO r_passenger WHERE email = NEW.email;
		IF NOT FOUND THEN
			RAISE exception 'You should enter the email connected to your passport';
		END IF; 
	END IF;
END;
$account_check_email$
LANGUAGE plpgsql;

-- CREATE TRIGGER account_check_email 
-- 	BEFORE INSERT OR UPDATE 
-- 	ON Account
-- 	FOR EACH ROW
-- 		EXECUTE FUNCTION account_check_email()


-- Foreign keys related to types other than the account type should be null
-- A trigger on account to enforce this condition
CREATE OR REPLACE FUNCTION account_check_null () RETURNS TRIGGER AS $account_check_null$
BEGIN
	IF NEW.type = 'passenger' THEN
		IF NEW.employee_ssn != NULL THEN
			RAISE exception 'Foreign Key to employee_ssn should be null for passenger account';
		END IF; 
	END IF;
	IF NEW.type = 'empolyee' THEN
		IF NEW.passenger_id != NULL THEN
			RAISE exception 'Foreign Key to passenger_id should be null for employee account';
		END IF; 
	END IF;
END;
$account_check_null$
LANGUAGE plpgsql;

-- CREATE TRIGGER account_check_null 
-- 	BEFORE INSERT OR UPDATE 
-- 	ON Account
-- 	FOR EACH ROW
-- 		EXECUTE FUNCTION account_check_null()


CREATE OR REPLACE FUNCTION track_delayed_flight () RETURNS TRIGGER AS $track_delayed_flight$
DECLARE
	r_delayed Delayed_flights%rowtype;
BEGIN
	IF NEW.status = 'delayed' THEN
		SELECT * FROM Delayed_flights INTO r_delayed WHERE code = NEW.code;
		IF NOT FOUND THEN
			INSERT INTO Delayed_flights VALUES (NEW.code, CURRENT_TIMESTAMP);
		END IF;
	ELSE
		SELECT * FROM Delayed_flights INTO r_delayed WHERE code = NEW.code;
		IF FOUND THEN
			DELETE FROM Delayed_flights WHERE code=NEW.code;
		END IF;
	END IF;
END;
$track_delayed_flight$
LANGUAGE plpgsql;

-- CREATE TRIGGER track_delayed_flight 
-- 	BEFORE INSERT OR UPDATE 
-- 	ON Flight
-- 	FOR EACH ROW
-- 		EXECUTE FUNCTION track_delayed_flight()

CREATE OR REPLACE FUNCTION track_price_change () RETURNS TRIGGER AS $track_price_change$
BEGIN
	INSERT INTO Price_history VALUES (
		CURRENT_DATE, 
		OLD.source, 
		OLD.destination, 
		OLD.class,
		OLD.price,
		NEW.price	
	);
END;
$track_price_change$
LANGUAGE plpgsql;

CREATE TRIGGER track_price_change 
	BEFORE UPDATE 
	ON Price
	FOR EACH ROW
		EXECUTE FUNCTION track_price_change()