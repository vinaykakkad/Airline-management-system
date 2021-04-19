-- There are more than one cities or state with same name.
-- But the combination of city and state uniquely identifies the country.
CREATE TABLE IF NOT EXISTS Country(
	city text,
	state text,
	country text NOT NULL,
	PRIMARY KEY(city, state)
);


CREATE TABLE IF NOT EXISTS Airport (
	name text PRIMARY KEY,
	city text NOT NULL,
	state text NOT NULL,
	FOREIGN KEY(city, state) REFERENCES Country ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Airline (
	id varchar(3) PRIMARY KEY,
	name text NOT NULL,
	three_digit_code char(3) NOT NULL
);


CREATE TABLE IF NOT EXISTS Contains (
	airport_name text REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	airline_id varchar(3) REFERENCES Airline(id) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(airport_name, airline_id)
);


CREATE TYPE job_types as ENUM (
	'Administration',
	'Engineer',
	'Traffic_Monitor',
	'Airport_Authority'
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
	email text NOT NULL UNIQUE CHECK (email ~ '^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$'),
	address text NOT NULL,
	phone char(10) NOT NULL CHECK(phone not like '%[^0-9]%'),
	birthdate date NOT NULL,
	sex gender NOT NULL,
	job_type job_types NOT NULL REFERENCES Salary ON DELETE CASCADE ON UPDATE CASCADE,
	airport_name text NOT NULL REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Administration (
	ssn int PRIMARY KEY REFERENCES Employee ON DELETE CASCADE ON UPDATE CASCADE,
	type text NOT NULL
);

CREATE TABLE IF NOT EXISTS Engineer (
	ssn int PRIMARY KEY REFERENCES Employee ON DELETE CASCADE ON UPDATE CASCADE,
	type text NOT NULL
);

CREATE TABLE IF NOT EXISTS Traffic_monitor (
	ssn int PRIMARY KEY REFERENCES Employee ON DELETE CASCADE ON UPDATE CASCADE,
	shift text NOT NULL
);

CREATE TABLE IF NOT EXISTS Airport_Authority (
	ssn int PRIMARY KEY REFERENCES Employee ON DELETE CASCADE ON UPDATE CASCADE,
	position text NOT NULL
);


CREATE TYPE flight_types as ENUM (
	'connectig',
	'direct'
);

CREATE TYPE status_types as ENUM (
	'on-time',
	'delay'
);

-- Trigger to check the fields that needs to be 0
CREATE TABLE IF NOT EXISTS Flight (
	code char(6) PRIMARY KEY,
	source text NOT NULL REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	destination text NOT NULL REFERENCES Airport(name) ON DELETE CASCADE ON UPDATE CASCADE,
	arrival time NOT NULL, 
	departure time NOT NULL,
	status status_types NOT NULL,
	duration time NOT NULL,
	flight_type flight_types NOT NULL,
	layover_time time,
	stops int,
	airline_id varchar(3) NOT NULL REFERENCES Airline(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Passenger (
	passport_number text PRIMARY KEY,
	first_name text NOT NULL,
	last_name text NOT NULL,
	email text NOT NULL UNIQUE CHECK (email ~ '^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$'),
	address text NOT NULL,
	phone char(10) NOT NULL CHECK(phone not like '%[^0-9]%'),
	birthdate date NOT NULL,
	sex gender NOT NULL
);


CREATE TABLE IF NOT EXISTS Serves (
	employee_ssn int NOT NULL REFERENCES Employee(ssn) ON DELETE CASCADE ON UPDATE CASCADE,
	passenger_number text NOT NULL REFERENCES Passenger(passport_number) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(employee_ssn, passenger_number)
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
	price int NOT NULL,
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
	passenger_number text NOT NULL REFERENCES Passenger(passport_number) ON DELETE CASCADE ON UPDATE CASCADE,
	flight_code char(6) NOT NULL REFERENCES Flight(code) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (source, destination, class) REFERENCES Price ON DELETE CASCADE ON UPDATE CASCADE
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

-- 2 Triggers check if email exists, and for checking null
CREATE TABLE IF NOT EXISTS Account (
	email text PRIMARY KEY CHECK (email ~ '^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$'),
	password text NOT NULL,
	type account_types NOT NULL,
	passenger_number text REFERENCES Passenger(passport_number) ON DELETE CASCADE ON UPDATE CASCADE,
	employee_ssn int REFERENCES Employee(ssn) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Price_history (
	changed_on date NOT NULL,
	source text NOT NULL,
	destination text NOT NULL, 
	class class_types NOT NULL,
	old_price int NOT NULL,
	new_price int NOT NULL,
	FOREIGN KEY (source, destination, class) REFERENCES Price ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (changed_on, source, destination, class)	
);


CREATE TABLE IF NOT EXISTS Delayed_flights (
	code char(6) PRIMARY KEY REFERENCES Flight,
	report_time timestamp	
);