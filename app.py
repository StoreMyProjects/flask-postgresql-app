import datetime
import re
from functools import wraps

import pdfkit
from flask import Flask, make_response, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from createsql import createsql, get_db

app = Flask(__name__)
app.register_blueprint(createsql)
app.config.from_pyfile("config.py")

# try:
#     redis_client = app.config.get("SESSION_REDIS")
#     if redis_client:
#         redis_client.ping()
#         print("Redis connection successful")
#     else:
#         print("Redis connection skipped: SESSION_REDIS not configured")
# except Exception as exc:
#     print(f"Redis connection failed: {exc}")

Session(app)

EMAIL_PATTERN = re.compile(r"^[a-z0-9]+[._]?[a-z0-9]+@[a-z0-9.-]+\.[a-z]{2,3}$", re.IGNORECASE)
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#&!])[A-Za-z\d@$#&!]{6,12}$")


def valid_email(value):
    return bool(value and EMAIL_PATTERN.fullmatch(value))


def valid_password(value):
    return bool(value and PASSWORD_PATTERN.fullmatch(value))


def login_required(view_func):
    @wraps(view_func)
    def secure_function(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return secure_function


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/healthy')
def healthy():
    return "OK", 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        fullname = (request.form.get('fullname') or '').strip()
        email = (request.form.get('email') or '').strip()
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''
        confirm = request.form.get('confirm') or ''

        if not all([fullname, email, username, password, confirm]):
            return render_template("register.html", error="Please complete all fields!")

        if not valid_email(email):
            return render_template("register.html", error="Please enter a valid email!")

        if not valid_password(password):
            return render_template("register.html", error="Please enter a valid password!")

        if password != confirm:
            return render_template("register.html", error="Password and confirm password don't match!")

        try:
            conn = get_db()
            if conn is None:
                return render_template("register.html", error="Database is unavailable. Please try again later.")

            db = conn.cursor()
            db.execute(
                "INSERT INTO users (fullname, email, username, password) VALUES (%s, %s, %s, %s)",
                (fullname, email, username, generate_password_hash(password)),
            )
            conn.commit()
            return render_template("login.html", msg="You are registered successfully!")
        except Exception:
            if conn:
                conn.rollback()
            return render_template("register.html", error="Found user with same username! Please try another username or go for login!")

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get('username') or '').strip()
        passwd = request.form.get('password') or ''

        try:
            conn = get_db()
            if conn is None:
                return render_template("login.html", error="Database is unavailable. Please try again later.")

            db = conn.cursor()
            db.execute("SELECT fullname, email, username, password FROM users WHERE username = %s", (username,))
            user = db.fetchone()

            if user and username == user[2] and check_password_hash(user[3], passwd):
                session["LoggedIn"] = True
                session["fullname"] = user[0]
                session["username"] = username
                session["email"] = user[1]
                return redirect(url_for("profile"))
        except Exception:
            return render_template("login.html", error="Unable to authenticate right now. Please try again.")

        return render_template("login.html", error="Invalid credentials! Please enter valid username or password!")

    return render_template("login.html")


@app.route("/check")
@login_required
def check():
    return str(session.get("username"))


PACKAGE_DETAILS = {
    'Spain': {'place': 'Barcelona', 'num_of_days': 10, 'estimated_cost': 220000},
    'India': {'place': 'Goa', 'num_of_days': 10, 'estimated_cost': 153000},
    'Switzerland': {'place': 'Zurich', 'num_of_days': 10, 'estimated_cost': 117500},
    'Belgium': {'place': 'Dinant', 'num_of_days': 8, 'estimated_cost': 213000},
    'Italy': {'place': 'Venice', 'num_of_days': 8, 'estimated_cost': 118000},
    'Australia': {'place': 'Sydney', 'num_of_days': 8, 'estimated_cost': 210000},
    'Ireland': {'place': 'Dublin', 'num_of_days': 8, 'estimated_cost': 119000},
    'New Zealand': {'place': 'Mount Cook', 'num_of_days': 8, 'estimated_cost': 217000},
    'Canada': {'place': 'Big Muddy Valley', 'num_of_days': 5, 'estimated_cost': 187100},
    'Venezuela': {'place': 'Angel Falls', 'num_of_days': 5, 'estimated_cost': 115000},
    'Arizona': {'place': 'Tucson', 'num_of_days': 5, 'estimated_cost': 215000},
    'Norway': {'place': 'Bergen', 'num_of_days': 10, 'estimated_cost': 210000},
    'Myanmar': {'place': 'Shwedagon Pagoda', 'num_of_days': 8, 'estimated_cost': 211000},
    'Namibia': {'place': 'Namibia', 'num_of_days': 8, 'estimated_cost': 117300},
    'French Polynesia': {'place': 'Skeleton Coast', 'num_of_days': 5, 'estimated_cost': 215700},
    'Iceland': {'place': 'Skogafoss', 'num_of_days': 10, 'estimated_cost': 218200},
    'Greece': {'place': 'Athens', 'num_of_days': 9, 'estimated_cost': 214800},
    'China': {'place': 'Beijing', 'num_of_days': 6, 'estimated_cost': 115900},
    'Germany': {'place': 'Berlin', 'num_of_days': 5, 'estimated_cost': 116500},
    'Chile': {'place': 'Easter Island', 'num_of_days': 8, 'estimated_cost': 119000},
}


def get_today_values():
    now = datetime.datetime.now()
    return now.strftime("%x"), now.strftime("%X")


@app.route('/destinations', methods=['GET', 'POST'])
@login_required
def destinations():
    if request.method == "POST":
        selected_package = request.form.get('selected_package')
        if not selected_package:
            return render_template("destinations.html", msg='Please select a package!')

        package = PACKAGE_DETAILS.get(selected_package)
        if package is None:
            return render_template("destinations.html", msg='Selected package is invalid!')

        place = package['place']
        num_of_days = package['num_of_days']
        estimated_cost = package['estimated_cost']

        try:
            conn = get_db()
            if conn is None:
                return render_template("destinations.html", msg='Database is unavailable. Please try again later.')

            db = conn.cursor()
            db.execute(
                "INSERT INTO destinations (email, package_name, place, numOfDays, estimated_cost, username) VALUES (%s, %s, %s, %s, %s, %s)",
                (session['email'], selected_package, place, num_of_days, estimated_cost, session['username']),
            )
            conn.commit()
            return render_template('hotels.html', msg='Package added successfully!')
        except Exception:
            if conn:
                conn.rollback()
            return render_template("destinations.html", msg='Something went wrong while adding package!')

    return render_template("destinations.html")


@app.route('/hotels', methods=['GET', 'POST'])
@login_required
def hotels():
    if request.method == "POST":
        cost = request.form.get('cost')
        category = request.form.get('category')
        room_type = request.form.get('room_type')
        no_of_guests = request.form.get('noOfGuests')
        check_in_date = request.form.get('checkIn')
        check_out_date = request.form.get('checkOut')

        try:
            check_in = datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
            check_out = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
        except ValueError:
            return render_template("hotels.html", msg='Please provide valid check-in and check-out dates!')

        if check_in >= check_out:
            return render_template("hotels.html", msg='Check-in date must be before Check-out date!')

        try:
            conn = get_db()
            if conn is None:
                return render_template("hotels.html", msg='Database is unavailable. Please try again later.')

            db = conn.cursor()
            db.execute(
                "INSERT INTO hotels (email, cost, category, room_type, no_of_guests, check_in_date, check_out_date, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (session["email"], cost, category, room_type, abs(int(no_of_guests)), check_in_date, check_out_date, session["username"]),
            )
            conn.commit()
            return render_template('flights.html', msg='Hotel room booked successfully!')
        except Exception:
            if conn:
                conn.rollback()
            return render_template("hotels.html", msg='Something went wrong while booking hotel room!')

    return render_template("hotels.html")


@app.route('/flights', methods=['GET', 'POST'])
@login_required
def flights():
    if request.method == "POST":
        flight_cost = request.form.get('cost')
        trip_type = request.form.get('trip_type')
        class_type = request.form.get('class_type')
        departure_d = request.form.get('departure')
        return_d = request.form.get('return')
        passengers = request.form.get('passengers')
        source = request.form.get('source')
        destination = request.form.get('destination')

        try:
            if trip_type == "Round Trip":
                departure_date = datetime.datetime.strptime(departure_d, '%Y-%m-%d')
                return_date = datetime.datetime.strptime(return_d, '%Y-%m-%d')
                if departure_date >= return_date:
                    return render_template("hotels.html", msg='Departure date must be before Return date!')

            conn = get_db()
            if conn is None:
                return render_template("flights.html", msg='Database is unavailable. Please try again later.')

            db = conn.cursor()
            db.execute(
                "INSERT INTO flights (email, flight_cost, trip_type, class_type, departure_d, return_d, passengers, source, destination, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (session['email'], flight_cost, trip_type, class_type, departure_d, return_d, abs(int(passengers)), source, destination, session['username']),
            )
            conn.commit()
            return redirect(url_for('payment'))
        except Exception:
            if 'conn' in locals() and conn:
                conn.rollback()
            return render_template('flights.html', msg='Something went wrong while booking flight!')

    return render_template("flights.html")


@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == "GET":
        try:
            conn = get_db()
            if conn is None:
                return render_template("payment.html", msg='Database is unavailable. Please try again later.')

            db = conn.cursor()
            db.execute(
                "SELECT d.package_name, d.place, d.numOfDays, d.estimated_cost, h.cost, h.category, h.room_type, h.no_of_guests, h.check_in_date, h.check_out_date, f.flight_cost, f.trip_type, f.class_type, f.departure_d, f.return_d, f.passengers, f.source, f.destination FROM destinations d LEFT JOIN hotels h ON h.username = d.username LEFT JOIN flights f ON f.username = d.username WHERE d.username = %s ORDER BY d.id DESC LIMIT 1",
                (session['username'],),
            )
            summary = db.fetchone()

            if not summary:
                return render_template("payment.html", msg='No travel summary found. Please complete booking steps first.')

            package_name, place, no_of_days, dest_pack, hotel_cost, category, room_type, no_of_guests, check_in_date, check_out_date, flight_cost, trip_type, class_type, departure_d, return_d, passengers, source, destination = summary
            date_now, time_now = get_today_values()

            if trip_type == "Round Trip":
                flight_cost = float(flight_cost) * 2
            else:
                flight_cost = float(flight_cost)

            total_amount = (int(dest_pack) * int(no_of_guests)) + (int(hotel_cost) * int(no_of_guests)) + (int(flight_cost) * int(passengers))

            db.execute(
                "INSERT INTO bookings (fullname, email, passengers, package_name, place, numOfDays, booking_date, booking_time, category, room_type, no_of_guests, check_in_date, check_out_date, trip_type, class_type, departure_d, return_d, source, destination, total_cost, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (session['fullname'], session['email'], passengers, package_name, place, no_of_days, date_now, time_now, category, room_type, no_of_guests, check_in_date, check_out_date, trip_type, class_type, departure_d, return_d, source, destination, total_amount, session['username']),
            )
            conn.commit()
            return render_template("payment.html", total_amount=total_amount)
        except Exception:
            if 'conn' in locals() and conn:
                conn.rollback()
            return render_template("payment.html", msg='Something went wrong while booking!')

    return redirect(url_for('bill'))


@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookingdetails():
    if request.method == "GET":
        try:
            conn = get_db()
            if conn is None:
                return render_template("bookings.html", msg='Database is unavailable. Please try again later.')

            db = conn.cursor()
            if session['username'] == "root":
                db.execute("SELECT * FROM bookings")
            else:
                db.execute("SELECT * FROM bookings WHERE username = %s", (session['username'],))
            rows = db.fetchall()
            return render_template("bookings.html", rows=rows)
        except Exception:
            return render_template("bookings.html", msg='No Bookings yet!')

    return render_template("home.html")


@app.route('/delete_booking', methods=['GET', 'POST'])
def delete_booking():
    if request.method == "POST":
        booking_id = request.form.get('booking_id')
    else:
        booking_id = request.args.get('booking_id')

    try:
        conn = get_db()
        if conn is None:
            return render_template("bookings.html", msg='Database is unavailable. Please try again later.')

        db = conn.cursor()
        db.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        db.execute("DELETE FROM flights WHERE id = %s", (booking_id,))
        db.execute("DELETE FROM hotels WHERE id = %s", (booking_id,))
        db.execute("DELETE FROM destinations WHERE id = %s", (booking_id,))
        conn.commit()
        return redirect("/bookings")
    except Exception:
        if 'conn' in locals() and conn:
            conn.rollback()
        return render_template("bookings.html", msg='No Bookings found with this id!')


@app.route('/bill')
@login_required
def bill():
    if request.method == 'GET':
        try:
            conn = get_db()
            if conn is None:
                return render_template("home.html", msg='Database is unavailable. Please try again later.')

            db = conn.cursor()
            db.execute(
                "SELECT package_name, estimated_cost FROM destinations WHERE username = %s ORDER BY id DESC LIMIT 1",
                (session['username'],),
            )
            dest_row = db.fetchone()
            db.execute(
                "SELECT cost, no_of_guests FROM hotels WHERE username = %s ORDER BY id DESC LIMIT 1",
                (session['username'],),
            )
            hotel_row = db.fetchone()
            db.execute(
                "SELECT flight_cost, passengers, trip_type FROM flights WHERE username = %s ORDER BY id DESC LIMIT 1",
                (session['username'],),
            )
            flight_row = db.fetchone()
            db.execute(
                "SELECT id, booking_date, booking_time FROM bookings WHERE username = %s ORDER BY id DESC LIMIT 1",
                (session['username'],),
            )
            booking_row = db.fetchone()

            if not all([dest_row, hotel_row, flight_row, booking_row]):
                return render_template("home.html", msg='No booking record found.')

            package_name, dest_pack = dest_row
            hotel_cost, no_of_guests = hotel_row
            flight_cost, passengers, trip_type = flight_row
            booking_id, booking_date, booking_time = booking_row

            if trip_type == "Round Trip":
                flight_cost = float(flight_cost) * 2
            else:
                flight_cost = float(flight_cost)

            total_amount = (int(dest_pack) * int(no_of_guests)) + (int(hotel_cost) * int(no_of_guests)) + (int(flight_cost) * int(passengers))

            return render_template(
                "billing.html",
                total_amount=total_amount,
                package_name=package_name,
                dest_pack=dest_pack,
                hotel_cost=hotel_cost,
                flight_cost=flight_cost,
                booking_id=booking_id,
                booking_date=booking_date,
                booking_time=booking_time,
            )
        except Exception:
            return render_template("home.html", msg='Unable to load your billing details.')

    return render_template("home.html")


@app.route('/pdf')
@login_required
def pdf():
    try:
        conn = get_db()
        if conn is None:
            return render_template("home.html", msg='Database is unavailable. Please try again later.')

        db = conn.cursor()
        db.execute("SELECT package_name, estimated_cost FROM destinations WHERE username = %s ORDER BY id DESC LIMIT 1", (session['username'],))
        dest_row = db.fetchone()
        db.execute("SELECT cost, no_of_guests FROM hotels WHERE username = %s ORDER BY id DESC LIMIT 1", (session['username'],))
        hotel_row = db.fetchone()
        db.execute("SELECT flight_cost, passengers, trip_type FROM flights WHERE username = %s ORDER BY id DESC LIMIT 1", (session['username'],))
        flight_row = db.fetchone()
        db.execute("SELECT id, booking_date, booking_time FROM bookings WHERE username = %s ORDER BY id DESC LIMIT 1", (session['username'],))
        booking_row = db.fetchone()

        if not all([dest_row, hotel_row, flight_row, booking_row]):
            return render_template("home.html", msg='No booking record found.')

        package_name, dest_pack = dest_row
        hotel_cost, no_of_guests = hotel_row
        flight_cost, passengers, trip_type = flight_row
        booking_id, booking_date, booking_time = booking_row

        if trip_type == "Round Trip":
            flight_cost = float(flight_cost) * 2
        else:
            flight_cost = float(flight_cost)

        total_amount = (int(dest_pack) * int(no_of_guests)) + (int(hotel_cost) * int(no_of_guests)) + (int(flight_cost) * int(passengers))

        html = render_template(
            "billing.html",
            package_name=package_name,
            booking_id=booking_id,
            booking_date=booking_date,
            booking_time=booking_time,
            total_amount=total_amount,
            flight_cost=flight_cost,
            hotel_cost=hotel_cost,
            dest_pack=dest_pack,
        )
        pdf_data = pdfkit.from_string(html, False)
        response = make_response(pdf_data)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=bill.pdf"
        return response
    except Exception:
        return render_template("home.html", msg='Unable to generate the invoice PDF.')


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG', False))