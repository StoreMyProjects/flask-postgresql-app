from flask import Blueprint, jsonify
import psycopg2

createsql = Blueprint('createsql', __name__)

@createsql.route('/connect')
def get_db():
    try:
        # Create a connection to the database
        conn = psycopg2.connect(
            dbname="dbname",
            user='your_user',
            password="your_password",
            host='your_db_hostname',
            port='5432'
        )
        return conn
    
    except psycopg2.Error as e:
        # If an error occurs during connection, return None or handle appropriately
        print("Database connection error:", e)
        return None

@createsql.route('/createdb')
def create_database():
    try:
        conn = get_db()
        if conn is None:
            return jsonify({'error': 'Failed to connect to the database'})
        conn.autocommit = True  # Disable transactions for database creation
        cur = conn.cursor()

        # Create a new database
        cur.execute("CREATE DATABASE flaskdb")
        cur.close()
        conn.close()
        return jsonify({'message': 'Database created successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)})

@createsql.route('/createtable')
def create_table():
    try:
        conn = get_db()
        if conn is None:
            # If connection failed, return an error response
            return jsonify({'error': 'Failed to connect to the database'})

        conn.autocommit = True 
        cur= conn.cursor()

        # Create required tables
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                name text NOT NULL,
                email text NOT NULL,
                username text NOT NULL PRIMARY KEY,
                password text NOT NULL
            )
        ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS hotels (
                    id SERIAL NOT NULL PRIMARY KEY ,
                    email text NOT NULL,
                    cost numeric NOT NULL,
                    category text NOT NULL,
                    room_type text NOT NULL,
                    no_of_guests int NOT NULL,
                    check_in_date date NOT NULL,
                    check_out_date date NOT NULL,
                    username text REFERENCES users(username)
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS flights (
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

        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS destinations (
                    id SERIAL NOT NULL PRIMARY KEY ,
                    email text NOT NULL,
                    package_name text NOT NULL,
                    place text NOT NULL,
                    numOfDays int NOT NULL,
                    estimated_cost numeric NOT NULL,
                    username text REFERENCES users(username)      
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id SERIAL NOT NULL PRIMARY KEY ,
                    name text NOT NULL,
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
        )''')

        cur.close()
        conn.close()

        return jsonify({'message': 'Table created successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)})


@createsql.route("/deletetable")
def deletetables():
    try:
        conn = get_db()
        if conn is None:
            # If connection failed, return an error response
            return jsonify({'error': 'Failed to connect to the database'})

        conn.autocommit = True  # Disable transactions for database creation
        cur = conn.cursor()

        # delete all tables    
        cur.execute("DROP TABLE bookings")

        cur.execute("DROP TABLE destinations")

        cur.execute("DROP TABLE flights")

        cur.execute("DROP TABLE hotels")

        cur.execute("DROP TABLE users")

        cur.close()
        conn.close()

        return jsonify({'message': 'Table deleted successfully!'})

    except Exception as e:
        return jsonify(f"Error deleting tables: {e}")
