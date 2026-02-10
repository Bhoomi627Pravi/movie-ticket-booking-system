
CREATE DATABASE IF NOT EXISTS movie_db;
USE movie_db;

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    vip_price DECIMAL(10,2) NOT NULL,
    normal_price DECIMAL(10,2) NOT NULL,
    vip_seats INT NOT NULL,
    normal_seats INT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    movie_id INT NOT NULL,
    seat_type ENUM('VIP','Normal') NOT NULL,
    seats_booked INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
INSERT INTO movies (title, vip_price, normal_price, vip_seats, normal_seats)
VALUES 
('Avengers: Endgame', 500, 300, 10, 50),
('Inception', 400, 250, 5, 30),
('Joker', 450, 270, 8, 40),
('Thor', 400, 250, 10, 40),
('Black Panther', 450, 300, 8, 35),
('Matrix', 500, 350, 12, 50),
('Spider-Man', 450, 300, 12, 40),
('Frozen 2', 350, 200, 5, 30),
('Avatar', 550, 350, 10, 50),
('The Batman', 500, 300, 8, 40);

