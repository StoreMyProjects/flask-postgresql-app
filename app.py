from flask import Flask, render_template, request, url_for, redirect, session, make_response, g, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2, pdfkit
import re, datetime
from createsql import createsql

app = Flask(__name__)

app.register_blueprint(createsql)
app.config.from_pyfile("config.py")

Session(app)

# conn = psycopg2.connect(dbname='flaskdb', user='postgres', password='123456789', host='flaskdb.ce2bgribc0sr.ap-south-1.rds.amazonaws.com', port=5432)
# db=conn.cursor()

def get_db():
    # Create a connection to the database
    conn = psycopg2.connect(
        dbname='flaskdb',
        user='postgres',
        password='123456789',
        host='flaskdb.ce2bgribc0sr.ap-south-1.rds.amazonaws.com',
        port='5432'
    )

    return conn

dt = datetime.datetime.now()
date_now = dt.strftime("%x")
time_now = dt.strftime("%X")

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        email_re = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        mat = re.search(email_re, email)

        pass_re = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#&!])[A-Za-z\d@$#&!]{6,12}$"
        patt = re.compile(pass_re)
        matc = re.search(patt, password)

        if not mat:
            error = "Please enter a Valid Email!"
            return render_template("register.html", error = error)
        elif not matc:
            error = "Please enter a Valid Password!"
            return render_template("register.html", error = error)
        elif password != confirm:
            error = "password and confirm password don't match!"
            return render_template("register.html", error = error)
        else:
            try:
                passwd = generate_password_hash(password)
                conn = get_db()
                db = conn.cursor()
                db.execute("insert into users values(%s,%s,%s,%s)", (name, email, username, passwd))
                conn.commit()
                msg = "you are registered successfully!"
                return render_template("login.html", msg = msg)
            # except(Exception, psycopg2.Error) as error:
            except:
                conn.rollback()
                error = "Found user with same username! Please try another username or go for login!"
                return render_template("register.html", error = error)
    return render_template("register.html")


@app.route('/login', methods=["GET", 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        passwd = request.form.get('password')
        conn = get_db()
        db = conn.cursor()
        db.execute("select * from users where username = %s", (username,))
        users = db.fetchall()
        for user in users:
            # print(x)
            if username == user[2] and check_password_hash(user[3], passwd):
                # print("user found")
                name = user[0]
                email = user[1]
                session["LoggedIn"] = True
                session['name'] = name
                session['username'] = username
                session['email'] = email
                return redirect(url_for("profile"))
            else:
                # print("Invalid credentials")
                error = "Invalid credentials! Please enter valid username or password!"
                return render_template("login.html", error = error)
        else:
            error = "Invalid credentials! Please enter valid username or password!"
            return render_template("login.html", error = error)
    return render_template("login.html")


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    if request.method == "POST":
        if request.form.get("selected_package") == "Spain":
            package_name = "Spain Package"
            place = "Barcelona"
            num_of_days = 10
            estimated_cost = 220000

        elif request.form.get("selected_package") == "India":
            package_name = "India Package"
            place = "Goa"
            num_of_days = 10
            estimated_cost = 153000

        elif request.form.get("selected_package") == "Switzerland":
            package_name = "Switzerland Package"
            place = "Zurich"
            num_of_days = 10
            estimated_cost = 117500

        elif request.form.get("selected_package") == "Belgium":
            package_name = "Belgium Package"
            place = "Dinant"
            num_of_days = 8
            estimated_cost = 213000

        elif request.form.get("selected_package") == "Italy":
            package_name = "Italy Package"
            place = "Venice"
            num_of_days = 8
            estimated_cost = 118000

        elif request.form.get("selected_package") == "Australia":
            package_name = "Australia Package"
            place = "Sydney"
            num_of_days = 8
            estimated_cost = 210000

        elif request.form.get("selected_package") == "Ireland":
            package_name = "Ireland Package"
            place = "Dublin"
            num_of_days = 8
            estimated_cost = 119000

        elif request.form.get("selected_package") == "New Zealand":
            package_name = "New Zealand Package"
            place = "Mount Cook"
            num_of_days = 8
            estimated_cost = 217000

        elif request.form.get("selected_package") == "Canada":
            package_name = "Canada Package"
            place = "Big Muddy Valley"
            num_of_days = 5
            estimated_cost = 187100

        elif request.form.get("selected_package") == "Venezuela":
            package_name = "Venezuela Package"
            place = "Angel Falls"
            num_of_days = 5
            estimated_cost = 115000

        elif request.form.get("selected_package") == "Arizona":
            package_name = "Arizona Package"
            place = "Tucson"
            num_of_days = 5
            estimated_cost = 215000

        elif request.form.get("selected_package") == "Norway":
            package_name = "Norway Package"
            place = "Bergen"
            num_of_days = 10
            estimated_cost = 210000

        elif request.form.get("selected_package") == "Myanmar":
            package_name = "Myanmar Package"
            place = "Shwedagon Pagoda"
            num_of_days = 8
            estimated_cost = 211000

        elif request.form.get("selected_package") == "Namibia":
            package_name = "Namibia Package"
            place = "Namibia"
            num_of_days = 8
            estimated_cost = 117300

        elif request.form.get("selected_package") == "French Polynesia":
            package_name = "French Polynesia Package"
            place = "Skeleton Coast"
            num_of_days = 5
            estimated_cost = 215700

        elif request.form.get("selected_package") == "Iceland":
            package_name = "Iceland Package"
            place = "Skogafoss"
            num_of_days = 10
            estimated_cost = 218200

        elif request.form.get("selected_package") == "Greece":
            package_name = "Greece Package"
            place = "Athens"
            num_of_days = 9
            estimated_cost = 214800

        elif request.form.get("selected_package") == "China":
            package_name = "China Package"
            place = "Beijing"
            num_of_days = 6
            estimated_cost = 115900

        elif request.form.get("selected_package") == "Germany":
            package_name = "Germany Package"
            place = "Berlin"
            num_of_days = 5
            estimated_cost = 116500

        else:
            package_name = "Chile Package"
            place = "Easter Island"
            num_of_days = 8
            estimated_cost = 119000

        try:
            conn = get_db()
            db = conn.cursor()
            db.execute("Insert into destinations values(DEFAULT ,%s,%s,%s,%s,%s,%s)",( session['email'], package_name, place, num_of_days, estimated_cost, session['username'] ))
            conn.commit()       
            msg = "package added successfully!"
            return render_template('hotels.html', msg = msg)
        # except(Exception, psycopg2.Error) as msg:
        except:
            msg = "Something went wrong while adding package!"
            # print(msg)
            return render_template("destinations.html", msg = msg)

    return render_template("destinations.html")


@app.route('/hotels', methods=['GET','POST'])
def hotels():
    if request.method == "POST":
        cost = request.form.get('cost')
        category = request.form.get('category')
        room_type = request.form.get('room_type')
        no_of_guests = request.form.get('noOfGuests')
        check_in_date = request.form.get('checkIn')
        check_out_date = request.form.get('checkOut')
        # no_of_days = request.form.get('noOfDays')

        check_in = tuple(check_in_date.split('-'))
        check_out = tuple(check_out_date.split('-'))

        year = int(check_in[0])
        month = int(check_in[1])
        day = int(check_in[2])

        year1 = int(check_out[0])
        month1 = int(check_out[1])
        day1 = int(check_out[2])
        
        checkInDate = datetime.date(year,month,day)
        checkOutDate = datetime.date(year1,month1,day1)

        if checkInDate < checkOutDate:
            try:
                conn = get_db()
                db = conn.cursor()
                db.execute("insert into hotels values(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s)",(session["email"], cost, category, room_type, abs(int(no_of_guests)), check_in_date, check_out_date, session["username"]))
                conn.commit()
                msg = "hotel room booked successfully!"
                return render_template('flights.html', msg = msg)
            # except(Exception, psycopg2.Error) as error:
            except:
                msg = "Something went wrong while booking hotel room!"
                # msg = "No available hotel rooms in this category ! Please try with another category!"
                return render_template("hotels.html", msg = msg)
        else:
            msg = "Check-in date must be before Check-out date!"
            return render_template("hotels.html", msg=msg)
    return render_template("hotels.html")


@app.route('/flights', methods=['GET','POST'])
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

        if trip_type == "Round Trip":
            departure_date = tuple(departure_d.split('-'))
            return_date = tuple(return_d.split('-'))

            year = int(departure_date[0])
            month = int(departure_date[1])
            day = int(departure_date[2])

            year1 = int(return_date[0])
            month1 = int(return_date[1])
            day1 = int(return_date[2])
            
            checkInDate = datetime.date(year,month,day)
            checkOutDate = datetime.date(year1,month1,day1)

            if checkInDate < checkOutDate:
                try:
                    conn = get_db()
                    db = conn.cursor()
                    db.execute("insert into flights values(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(session['email'], flight_cost, trip_type, class_type, departure_d, return_d, abs(int(passengers)), source, destination, session['username']))
                    conn.commit()
                    return redirect(url_for('payment'))
                # except(Exception, psycopg2.Error) as error:
                except:
                    msg = "Something went wrong while booking flight!"
                    # msg = f"No flights available to {destination} on {departure_d}. Please try another date."
                    return render_template('flights.html', msg= msg)
            else:
                msg = "Departure date must be before Return date!"
                return render_template("hotels.html", msg=msg)
        else:
            try:
                conn = get_db()
                db = conn.cursor()
                db.execute("insert into flights values(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(session['email'], flight_cost, trip_type, class_type, departure_d, return_d, passengers, source, destination, session['username']))
                conn.commit()
                return redirect(url_for('payment'))
            # except(Exception, psycopg2.Error) as error:
            except:
                msg = "Something went wrong while booking flight!"
                # msg = f"No flights available to {destination} on {departure_d}. Please try another date."
                return render_template('flights.html', msg= msg)
    return render_template("flights.html")

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    if request.method == "GET":
        conn = get_db()
        db = conn.cursor()
        db.execute("select * from destinations inner join users on users.username=destinations.username and users.username = %s", (session['username'],))
        dest_row = db.fetchall()
        db.execute("select * from hotels inner join users on users.username=hotels.username and users.username = %s", (session['username'],))
        hotel_row = db.fetchall()
        db.execute("select * from flights inner join users on users.username=flights.username and users.username = %s", (session['username'],))
        flight_row = db.fetchall()
        for i in dest_row:
            package_name = i[2]
            place = i[3]
            no_of_days = i[4]
            dest_pack = i[5]

        for j in hotel_row:
            hotel_cost = j[2]
            category = j[3]   
            room_type = j[4]
            no_of_guests = j[5]
            check_in_date = j[6]
            check_out_date = j[7]
            # no_of_days = j[8]

        for k in flight_row:
            flight_cost = k[2]
            trip_type = k[3]
            class_type = k[4]
            departure_d = k[5]
            return_d = k[6]
            passengers = k[7]
            source = k[8]
            destination = k[9]

        if trip_type == "Round Trip":
            flight_cost *= 2
        else:
            flight_cost = flight_cost

        total_amount = (int(dest_pack) * no_of_guests) + (int(hotel_cost) * no_of_guests) + (int(flight_cost) * passengers)
        
        try:
            db.execute("insert into bookings values(DEFAULT, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(session['name'], session['email'], passengers, package_name, place, no_of_days, date_now, time_now, category, room_type, no_of_guests, check_in_date, check_out_date, trip_type, class_type, departure_d, return_d, source, destination, total_amount, session['username']))
            conn.commit()
        # except(Exception, psycopg2.Error) as error:
        except:
            msg = "Something went wrong while booking!"
            return render_template("payment.html", msg = msg)

        return render_template("payment.html", total_amount = total_amount)

    return redirect(url_for('bill'))


@app.route('/bookings', methods=['GET', 'POST'])
def bookingdetails():
    if request.method == "GET":
        try:
            conn = get_db()
            db = conn.cursor()
            db.execute("select * from bookings inner join users on users.username=bookings.username and users.username = %s", (session['username'],))
            rows = db.fetchall()
            for row in rows:
                print(row)
            return render_template("bookings.html", rows=rows)
        # except(Exception, psycopg2.Error) as error:
        except:
            msg = "No Bookings yet!"
            return render_template("bookings.html", msg = msg)
    return render_template("home.html")


@app.route('/bill')
def bill():
    if request.method == 'GET':
        conn = get_db()
        db = conn.cursor()
        db.execute("select package_name, estimated_cost from destinations inner join users on users.username=destinations.username and users.username = %s", (session['username'],))
        dest_row = db.fetchall()
        db.execute("select cost, no_of_guests from hotels inner join users on users.username=hotels.username and users.username = %s", (session['username'],))
        hotel_row = db.fetchall()
        db.execute("select flight_cost, passengers, trip_type from flights inner join users on users.username=flights.username and users.username = %s", (session['username'],))
        flight_row = db.fetchall()
        db.execute("select id, booking_date, booking_time from bookings inner join users on users.username=bookings.username and users.username = %s", (session['username'],))
        booking_row = db.fetchall()
        for i in dest_row:
            package_name = i[0]
            dest_pack = i[1]
        for j in hotel_row:
            hotel_cost = j[0]
            no_of_guests = j[1]
        for k in flight_row:
            flight_cost = k[0]
            passengers = k[1]
            trip_type = k[2]
        for b in booking_row:
            booking_id = b[0]
            booking_date = b[1]
            booking_time = b[2]
            
        if trip_type == "Round Trip":
            flight_cost *= 2
        else:
            flight_cost = flight_cost
        
        total_amount = (int(dest_pack) * no_of_guests) + (int(hotel_cost) * no_of_guests) + (int(flight_cost) * passengers)

        return render_template("billing.html", total_amount=total_amount, package_name=package_name, dest_pack=dest_pack, hotel_cost=hotel_cost, flight_cost=flight_cost, booking_id=booking_id, booking_date=booking_date, booking_time=booking_time)
        
    return render_template("home.html")


@app.route('/pdf')
def pdf():
    conn = get_db()
    db = conn.cursor()
    db.execute("select package_name, estimated_cost from destinations inner join users on users.username=destinations.username and users.username = %s", (session['username'],))
    dest_row = db.fetchall()
    db.execute("select cost, no_of_guests from hotels inner join users on users.username=hotels.username and users.username = %s", (session['username'],))
    hotel_row = db.fetchall()
    db.execute("select flight_cost, passengers, trip_type from flights inner join users on users.username=flights.username and users.username = %s", (session['username'],))
    flight_row = db.fetchall()
    db.execute("select id, booking_date, booking_time from bookings inner join users on users.username=bookings.username and users.username = %s", (session['username'],))
    booking_row = db.fetchall()
    for i in dest_row:
        package_name = i[0]
        dest_pack = i[1]
    for j in hotel_row:
        hotel_cost = j[0]
        no_of_guests = j[1]
    for k in flight_row:
        flight_cost = k[0]
        passengers = k[1]
        trip_type = k[2]
    for b in booking_row:
        booking_id = b[0]
        booking_date = b[1]
        booking_time = b[2]
        
    if trip_type == "Round Trip":
        flight_cost *= 2
    else:
        flight_cost = flight_cost
    
    total_amount = (int(dest_pack) * no_of_guests) + (int(hotel_cost) * no_of_guests) + (int(flight_cost) * passengers)
    
    html = render_template("billing.html", package_name=package_name, booking_id=booking_id, booking_date=booking_date, booking_time=booking_time, total_amount=total_amount, flight_cost=flight_cost, hotel_cost=hotel_cost, dest_pack=dest_pack)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=bill.pdf"
    return response


@app.route('/profile')
def profile():
    return render_template("profile.html")    


@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')