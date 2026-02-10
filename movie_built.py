import mysql.connector as sql

# ---------- DATABASE CONNECTION ----------
def get_connection():
    return sql.connect(
        host="localhost",
        user="root",
        password="root",
        database="movie_db",
        auth_plugin="mysql_native_password"
    )

# ---------- VIEW ALL MOVIES ----------
def view_movies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    print("\nID | Movie | VIP Price | Normal Price | VIP Seats | Normal Seats")
    print("-" * 70)
    for m in movies:
        print(f"{m[0]} | {m[1]} | ₹{m[2]} | ₹{m[3]} | {m[4]} | {m[5]}")
    conn.close()

# ---------- SEARCH MOVIES ----------
def search_movies():
    conn = get_connection()
    cur = conn.cursor()
    keyword = input("Enter movie name to search: ").strip()
    cur.execute("SELECT * FROM movies WHERE title LIKE %s", (f"%{keyword}%",))
    movies = cur.fetchall()
    if not movies:
        print("No movies found!")
    else:
        print("\nID | Movie | VIP Price | Normal Price | VIP Seats | Normal Seats")
        print("-" * 70)
        for m in movies:
            print(f"{m[0]} | {m[1]} | ₹{m[2]} | ₹{m[3]} | {m[4]} | {m[5]}")
    conn.close()

# ---------- SHOW AVAILABLE SEATS ----------
def show_seats():
    conn = get_connection()
    cur = conn.cursor()
    try:
        movie_id = int(input("Enter Movie ID to check seats: "))
    except ValueError:
        print("Invalid input!")
        return
    cur.execute("SELECT title, vip_seats, normal_seats FROM movies WHERE id=%s", (movie_id,))
    movie = cur.fetchone()
    if movie:
        print(f"\n{movie[0]} - VIP Seats: {movie[1]}, Normal Seats: {movie[2]}")
    else:
        print("Movie not found!")
    conn.close()

# ---------- CALCULATE DISCOUNT ----------
def calculate_discount(price, tickets):
    if tickets >= 5:
        print("10% discount applied for booking 5 or more tickets!")
        return price * 0.9
    return price

# ---------- BOOK TICKET ----------
def book_ticket():
    conn = get_connection()
    cur = conn.cursor()
    view_movies()

    try:
        movie_id = int(input("\nEnter Movie ID to book: "))
        seat_type = input("Seat type (VIP/Normal): ").strip().lower()
        tickets = int(input("Number of tickets: "))
        customer_name = input("Enter your name: ").strip()
    except ValueError:
        print("Invalid input!")
        return

    cur.execute("SELECT title, vip_price, normal_price, vip_seats, normal_seats FROM movies WHERE id=%s", (movie_id,))
    movie = cur.fetchone()
    if not movie:
        print("Movie not found!")
        return

    title, vip_price, normal_price, vip_seats, normal_seats = movie

    if seat_type == "vip":
        if tickets > vip_seats:
            print(f"Only {vip_seats} VIP seats available!")
            return
        price = tickets * vip_price
        price = calculate_discount(price, tickets)
        cur.execute("UPDATE movies SET vip_seats = vip_seats - %s WHERE id=%s", (tickets, movie_id))
    elif seat_type == "normal":
        if tickets > normal_seats:
            print(f"Only {normal_seats} Normal seats available!")
            return
        price = tickets * normal_price
        price = calculate_discount(price, tickets)
        cur.execute("UPDATE movies SET normal_seats = normal_seats - %s WHERE id=%s", (tickets, movie_id))
    else:
        print("Invalid seat type!")
        return

    cur.execute(
        "INSERT INTO bookings (customer_name, movie_id, seat_type, seats_booked, total_price) VALUES (%s, %s, %s, %s, %s)",
        (customer_name, movie_id, seat_type.capitalize(), tickets, price)
    )

    conn.commit()
    print(f"\nBooking successful! Total Price: ₹{price}")
    conn.close()

# ---------- VIEW ALL BOOKINGS ----------
def view_bookings():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, b.customer_name, m.title, b.seat_type, b.seats_booked, b.total_price
        FROM bookings b
        JOIN movies m ON b.movie_id = m.id
    """)
    bookings = cur.fetchall()
    if not bookings:
        print("No bookings found.")
    else:
        print("\nBooking ID | Customer | Movie | Seat Type | Tickets | Total Price")
        print("-" * 70)
        for b in bookings:
            print(f"{b[0]} | {b[1]} | {b[2]} | {b[3]} | {b[4]} | ₹{b[5]}")
    conn.close()

# ---------- VIEW CUSTOMER BOOKINGS ----------
def view_customer_bookings():
    conn = get_connection()
    cur = conn.cursor()
    name = input("Enter your name to view bookings: ").strip()
    cur.execute("""
        SELECT b.booking_id, m.title, b.seat_type, b.seats_booked, b.total_price
        FROM bookings b
        JOIN movies m ON b.movie_id = m.id
        WHERE b.customer_name=%s
    """, (name,))
    bookings = cur.fetchall()
    if not bookings:
        print("No bookings found for", name)
    else:
        print("\nBooking ID | Movie | Seat Type | Tickets | Total Price")
        print("-" * 60)
        for b in bookings:
            print(f"{b[0]} | {b[1]} | {b[2]} | {b[3]} | ₹{b[4]}")
    conn.close()

# ---------- CANCEL BOOKING ----------
def cancel_booking():
    conn = get_connection()
    cur = conn.cursor()
    try:
        bid = int(input("Enter Booking ID to cancel: "))
    except ValueError:
        print("Invalid Booking ID!")
        return

    cur.execute("SELECT movie_id, seat_type, seats_booked FROM bookings WHERE booking_id=%s", (bid,))
    booking = cur.fetchone()
    if not booking:
        print("Booking not found!")
        return

    movie_id, seat_type, seats = booking
    if seat_type.lower() == "vip":
        cur.execute("UPDATE movies SET vip_seats = vip_seats + %s WHERE id=%s", (seats, movie_id))
    else:
        cur.execute("UPDATE movies SET normal_seats = normal_seats + %s WHERE id=%s", (seats, movie_id))

    cur.execute("DELETE FROM bookings WHERE booking_id=%s", (bid,))
    conn.commit()
    conn.close()
    print("Booking cancelled successfully!")

# ---------- ADD MOVIE (ADMIN) ----------
def add_movie():
    conn = get_connection()
    cur = conn.cursor()
    title = input("Movie Title: ").strip()
    try:
        vip_price = float(input("VIP Price: "))
        normal_price = float(input("Normal Price: "))
        vip_seats = int(input("VIP Seats: "))
        normal_seats = int(input("Normal Seats: "))
    except ValueError:
        print("Invalid input!")
        return

    cur.execute(
        "INSERT INTO movies (title, vip_price, normal_price, vip_seats, normal_seats) VALUES (%s,%s,%s,%s,%s)",
        (title, vip_price, normal_price, vip_seats, normal_seats)
    )
    conn.commit()
    conn.close()
    print("Movie added successfully!")

# ---------- MAIN MENU ----------
while True:
    print("""
===== Advanced Movie Ticket Booking System =====
1. View Movies
2. Search Movies
3. Book Ticket
4. Show Seats
5. View All Bookings
6. View My Bookings
7. Cancel Booking
8. Add Movie (Admin)
9. Exit
""")
    choice = input("Enter choice: ").strip()
    if choice == "1":
        view_movies()
    elif choice == "2":
        search_movies()
    elif choice == "3":
        book_ticket()
    elif choice == "4":
        show_seats()
    elif choice == "5":
        view_bookings()
    elif choice == "6":
        view_customer_bookings()
    elif choice == "7":
        cancel_booking()
    elif choice == "8":
        add_movie()
    elif choice == "9":
        print("Thank you! Enjoy your movie")
        break
    else:
        print("Invalid choice!")
