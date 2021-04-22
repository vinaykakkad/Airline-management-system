CREATE OR REPLACE FUNCTION get_job_type(e_email employee.email%type)
RETURNS text
AS
$$
DECLARE
   employee_record RECORD;
BEGIN
   SELECT * INTO employee_record
		FROM Employee
		WHERE email = e_email;

	IF employee_record IS NOT NULL THEN
		RETURN employee_record.job_type;
	ELSE
		RAISE exception 'No such employee exists!!';
		RETURN 'Error';
	END IF;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_customer_flights(p_email account.email%type)
RETURNS TABLE (
	ticket_number bigint,
	source text,
	destination text,
	class class_types,
	travelling_date date,
	seat_number text,
	flight_code char(6),
	status status_types
)
AS
$$
BEGIN
	RETURN QUERY
		SELECT 
			ticket.number,  
			ticket.source,
			ticket.destination,
			ticket.class,
			ticket.travelling_date,
			ticket.seat_number,
			ticket.flight_code,
			flight.status
		FROM ticket 
		INNER JOIN flight ON ticket.flight_code = flight.code 
		INNER JOIN Account ON account.passenger_number = ticket.passenger_number
		WHERE (
			account.email = p_email AND
			ticket.number NOT IN ( 
				select cancelled_tickets.ticket_number 
				from cancelled_tickets
			)	
		);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION calculate_surcharge(t_number cancelled_tickets.ticket_number%type)
RETURNS bigint
AS
$$
DECLARE
	parent_ticket RECORD;
	price_record RECORD;
BEGIN
	SELECT * INTO parent_ticket
	FROM Ticket
	WHERE number = t_number;

	IF parent_ticket ISNULL THEN
		RAISE exception 'Please check the ticket number';
		RETURN 0;
	ELSE
		SELECT * INTO price_record
		FROM Price
		WHERE (
			source = parent_ticket.source AND
			destination = parent_ticket.destination AND
			class = parent_ticket.class
		);

		IF price_record ISNULL THEN
			RAISE exception 'Internal Error!!';
			RETURN 0;
		ELSE
			RETURN (price_record.price / 4)::bigint;
		END IF;
	END IF;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION filter_flight(
	f_source flight.source%type,
	f_destination flight.destination%type
)
RETURNS TABLE (
	code char(6),
	source text,
	destination text,
	arrival time,
	departure time,
	status status_types,
	duration time,
	flight_type flight_types,
	layover_time time,
	stops int,
	airline_id varchar(3)	
)
AS
$$
BEGIN
	RETURN QUERY 
		SELECT * FROM flight
		WHERE (
			flight.source = f_source AND
			flight.destination = f_destination
		);
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION flight_history_filter(p_email account.email%type, filter text)
RETURNS TABLE (
	ticket_number bigint,
	source text,
	destination text,
	class class_types,
	travelling_date date,
	seat_number text,
	flight_code char(6),
	status status_types
)
AS
$$
BEGIN
	IF filter = 'upcoming' THEN
		RETURN QUERY
			SELECT * FROM get_customer_flights(p_email)
			WHERE get_customer_flights.travelling_date >= CURRENT_DATE;
	ELSE
		RETURN QUERY
			SELECT * FROM get_customer_flights(p_email)
			WHERE get_customer_flights.travelling_date < CURRENT_DATE;
	END IF;
END;
$$
LANGUAGE plpgsql;