-- There are more than one cities or state with same name.
-- But the combination of city and state uniquely identifies the country.
CREATE TABLE IF NOT EXISTS Country(
	city text,
	state text,
	country text,
	PRIMARY KEY(city, state)
);


CREATE TABLE IF NOT EXISTS Airport (
	name text PRIMARY KEY,
	city text NOT NULL,
	state name NOT NULL,
	FOREIGN KEY(city, state) REFERENCES Country ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Airline (
	id text PRIMARY KEY,
	name text NOT NULL,
	three_digit_code text NOT NULL
);


CREATE TABLE IF NOT EXISTS Contains (
	airport_name text REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	airline_id text REFERENCES Airline(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(airport_name, airline_id)
);


CREATE TYPE job_types as ENUM (
	'Administration',
	'Engineer',
	'Traffic_Monitor',
	'Airport_Authotiy'
);

CREATE TABLE IF NOT EXISTS Salary (
	job_type job_types PRIMARY KEY,
	amount int NOT NULL
);


CREATE TYPE gender as ENUM (
	'male',
	'female',
	'rather not say'
);

-- Create a trigger to check job-type other fields null idea
CREATE TABLE IF NOT EXISTS Employee (
	ssn int PRIMARY KEY,
	first_name text NOT NULL,
	last_name text NOT NULL,
	address text NOT NULL,
	phone int NOT NULL,
	age int NOT NULL,
	sex gender NOT NULL,
	job_type job_types NOT NULL,
	admin_type text,
	engineer_type text,
	monitor_shift text,
	authority_position text,
	airport_name text NOT NULL REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TYPE flight_types as ENUM (
	'connectig',
	'direct'
);

CREATE TYPE status_types as ENUM (
	'early',
	'on-time',
	'delay'
);

-- Trigger to check the fields that needs to be null
CREATE TABLE IF NOT EXISTS Flight (
	code text PRIMARY KEY,
	source text NOT NULL REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	destination text NOT NULL REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	arrival time NOT NULL, 
	departure time NOT NULL,
	status status_types NOT NULL,
	duration time NOT NULL,
	flight_type flight_types NOT NULL,
	layover_time time,
	stops int,
	airline_id text NOT NULL REFERENCES Airline(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Passport (
	number text PRIMARY KEY,
	first_name text NOT NULL,
	last_name text NOT NULL,
	address text NOT NULL,
	phone int NOT NULL,
	age int NOT NULL,
	sex gender NOT NULL
);


CREATE TABLE IF NOT EXISTS Passenger (
	id text PRIMARY KEY,
	passport_number text NOT NULL REFERENCES Passport(number) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Serves (
	employee_ssn int NOT NULL REFERENCES Employee(ssn) ON DELETE CASCADE ON UPDATE CASCADE,
	passenger_id text NOT NULL REFERENCES Passenger(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(employee_ssn, passenger_id)
);


CREATE TYPE class_types as ENUM(
	'first',
	'buisness',
	'economy'
);

-- Source, destination and class determines the price of the ticket
CREATE TABLE IF NOT EXISTS Price (
	source text REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	destination text REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	class class_types NOT NULL,
	prince int NOT NULL,
	PRIMARY KEY(source, destination, class)
);


CREATE TABLE IF NOT EXISTS Ticket (
	number int PRIMARY KEY,
	source text NOT NULL,
	destination text NOT NULL, 
	class class_types NOT NULL,
	booking_date date NOT NULL,
	travelling_date date NOT NULL,
	seat_number int NOT NULL,
	passenger_id text NOT NULL REFERENCES Passenger(id) ON DELETE CASCADE ON UPDATE CASCADE,
	flight_code text NOT NULL REFERENCES Flight(code) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (source, destination, class) REFERENCES Price
);

-- Trigger to check if the current date is before the travelling date\
CREATE TABLE IF NOT EXISTS Cancelled_tickets (
	ticket_number int PRIMARY KEY REFERENCES Ticket(number) ON DELETE CASCADE ON UPDATE CASCADE,
	cancellation_date date NOT NULL,
	surcharge int NOT NULL
);


CREATE TYPE account_types as ENUM (
	'admin',
	'employee',
	'passenger'
);

CREATE TABLE IF NOT EXISTS Account (
	email text PRIMARY KEY CHECK (email ~ '^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$'),
	password text NOT NULL,
	type account_types NOT NULL,
	passenger_id text REFERENCES Passenger(id) ON DELETE CASCADE ON UPDATE CASCADE,
	employee_ssn int REFERENCES Employee(ssn) ON DELETE CASCADE ON UPDATE CASCADE
);