CREATE TABLE IF NOT EXISTS users (
    fullname text NOT NULL,
    email text NOT NULL,
    username text NOT NULL PRIMARY KEY,
    password text NOT NULL
);

CREATE TABLE IF NOT EXISTS hotels (
    id SERIAL NOT NULL PRIMARY KEY ,
    email text NOT NULL,
    cost numeric NOT NULL,
    category text NOT NULL,
    room_type text NOT NULL,
    no_of_guests int NOT NULL,
    check_in_date date NOT NULL,
    check_out_date date NOT NULL,
    username text REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS flights (
    id SERIAL NOT NULL PRIMARY KEY ,
    email text NOT NULL,
    flight_cost numeric NOT NULL,
    trip_type text NOT NULL,
    class_type text NOT NULL,
    departure_d date NOT NULL,
    return_d date NOT NULL,
    passengers int NOT NULL,
    source text NOT NULL,
    destination text NOT NULL,
    username text REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS destinations (
    id SERIAL NOT NULL PRIMARY KEY ,
    email text NOT NULL,
    package_name text NOT NULL,
    place text NOT NULL,
    numOfDays int NOT NULL,
    estimated_cost numeric NOT NULL,
    username text REFERENCES users(username)      
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL NOT NULL PRIMARY KEY ,
    fullname text NOT NULL,
    email text NOT NULL,
    passengers int NOT NULL,
    package_name text NOT NULL,
    place text NOT NULL,
    numOfDays int NOT NULL,
    booking_date date NOT NULL,
    booking_time time NOT NULL,
    category text NOT NULL,
    room_type text NOT NULL,
    no_of_guests int NOT NULL,
    check_in_date date NOT NULL,
    check_out_date date NOT NULL,
    trip_type text NOT NULL,
    class_type text NOT NULL,
    departure_d date NOT NULL,
    return_d date NOT NULL,
    source text NOT NULL,
    destination text NOT NULL,
    total_cost numeric NOT NULL,
    username text REFERENCES users(username)
);

INSERT INTO users (fullname, email, username, password) VALUES ('The Explorer', 'theexplorer@tourx.com', 'root', 'root');