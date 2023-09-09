from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, make_response, g, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2, pdfkit
import re, datetime

createsql = Blueprint('createsql', __name__)

@createsql.route('/connect')
def get_db():
    if 'db' not in g:
        # Replace these values with your own RDS database information
        dbname = 'flaskdb'
        user = 'postgres'
        password = '123456789'
        host = 'flaskdb.ce2bgribc0sr.ap-south-1.rds.amazonaws.com'
        port = '5432'  # Default PostgreSQL port


        # Create a connection to the database
        g.db = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    return g.db

@createsql.teardown_app_request
def close_db(error):
    if 'db' in g:
        g.db.close()

@createsql.route('/createdb')
def create_database():
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            host='flaskdb.ce2bgribc0sr.ap-south-1.rds.amazonaws.com',
            port=5432,
            user='postgres',
            password=123456789
        )
        conn.autocommit = True  # Disable transactions for database creation
        cur = conn.cursor()

        # Create a new database
        cur.execute("CREATE DATABASE flaskdb")
        cur.close()
        conn.close()

        return True

    except Exception as e:
        print(f"Error creating database: {e}")
        return False

@createsql.route('/createtable')
def create_table():
    try:
        conn = get_db()
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

        conn.commit()

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
        conn.commit()

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
        conn.commit()

        cur.execute('''CREATE TABLE IF NOT EXISTS destinations (
                    id SERIAL NOT NULL PRIMARY KEY ,
                    email text NOT NULL,
                    package_name text NOT NULL,
                    place text NOT NULL,
                    numOfDays int NOT NULL,
                    estimated_cost numeric NOT NULL,
                    username text REFERENCES users(username)      
        )''')
        conn.commit()

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
        conn.commit()

        conn.close()

        return jsonify({'message': 'Table created successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)})


@createsql.route("/deletetable")
def deletetables():
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            host='flaskdb.ce2bgribc0sr.ap-south-1.rds.amazonaws.com',
            port=5432,
            user='postgres',
            password=123456789
        )
        conn.autocommit = True  # Disable transactions for database creation
        cur = conn.cursor()

        # Create a new database
        cur.execute("DROP TABLE users")
        conn.commit()
        cur.execute("DROP TABLE hotels")
        conn.commit()
        cur.execute("DROP TABLE flights")
        conn.commit()
        cur.execute("DROP TABLE destinations")
        conn.commit()
        cur.execute("DROP TABLE bookings")
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Table deleted successfully!'})

    except Exception as e:
        return jsonify(f"Error deleting tables: {e}")
