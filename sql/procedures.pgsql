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


CREATE OR REPLACE PROCEDURE book_ticket(
	a_email account.email%type,
	t_source ticket.source%type,
	t_destination ticket.destination%type,
	t_class ticket.class%type,
	t_date ticket.travelling_date%type,
	t_seat ticket.seat_number%type,
	t_code ticket.flight_code%type
) as $$
DECLARE
	parrent_passenger RECORD;
BEGIN
	SELECT * INTO parrent_passenger
	FROM passenger
	WHERE email = a_email;

	IF parrent_passenger IS NOT NULL THEN
		INSERT INTO ticket(source, destination, class, booking_date, travelling_date, seat_number, passenger_number, flight_code) 
		VALUES(t_source, t_destination, t_class, CURRENT_DATE, t_date, t_seat, parrent_passenger.passport_number, t_code);
	ELSE
		RAISE exception 'Email not found';
	END IF;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE cancel_ticket(t_number cancelled_tickets.ticket_number%type)
AS $$
DECLARE
	surcharge bigint;
BEGIN
	surcharge := calculate_surcharge(t_number);

	INSERT INTO cancelled_tickets VALUES (
		t_number,
		CURRENT_DATE,
		surcharge
	);
END;
$$
LANGUAGE plpgsql;