Movie Ticket Booking System 

A Python-based Command Line Interface (CLI) application that allows users to book movie tickets, managed via a MySQL database.

Features

Movie Management:View and search for movies in the database.
Seat Types:Support for both VIP and Normal seating.
Automatic Discounts:10% discount automatically applied when booking 5 or more tickets.
Booking Management:View personal bookings or cancel existing ones.
Admin Access:Ability to add new movies to the system directly through the app.

Tech Stack

Language:Python 3.x
Database:MySQL
Library:`mysql-connector-python`

 How to Setup

 1. Database Configuration
* Open your MySQL Workbench.
* Run the SQL commands provided in the `database_setup.sql` file (or the SQL code in your repository) to create the `movie_db` database and tables.
 2. Environment Setup
* Install the MySQL connector for Python:
  ```bash
  pip install mysql-connector-python
