CREATE OR REPLACE PROCEDURE add_account(
	acc_email Account.email%type, 
	acc_pass Account.password%type,
	acc_type Account.type%type
) as $$
DECLARE
	parent_record RECORD;
BEGIN
	IF acc_type = 'employee' THEN
		SELECT * INTO parent_record
		FROM Employee
		WHERE email = acc_email;

		IF parent_record IS NOT NULL THEN
			INSERT INTO Account(email, password, type, employee_ssn) VALUES(acc_email, acc_pass, acc_type, parent_record.ssn);
		ELSE
			RAISE exception 'You should use the email connected with your SSN for registration';
		END IF;
	ELSE
		SELECT * INTO parent_record
		FROM Passenger
		WHERE email = acc_email;

		IF parent_record IS NOT NULL THEN
			INSERT INTO Account(email, password, type, passenger_number) VALUES(acc_email, acc_pass, acc_type, parent_record.passport_number);
		ELSE
			RAISE exception 'You should use the email connected with your passport for registration';
		END IF;
	END IF;
END;
$$
LANGUAGE plpgsql;