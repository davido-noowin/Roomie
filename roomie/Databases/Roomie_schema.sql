DROP DATABASE IF EXISTS Roomie;
CREATE DATABASE Roomie;
USE roomie;

# Entities
CREATE TABLE Student(
	name_first VARCHAR(50),
    name_last VARCHAR(50),
    name_middle VARCHAR(50) DEFAULT '',
    email VARCHAR(30) PRIMARY KEY
);

CREATE TABLE roomsBooked(
	 email VARCHAR(30) NOT NULL,
     room_booked VARCHAR(20),
     date_booked datetime NOT NULL,
     FOREIGN KEY (email) REFERENCES Student(email),
     PRIMARY KEY (email, room_booked)
);


CREATE TABLE Room(
	room_id VARCHAR(20) PRIMARY KEY,
    location VARCHAR(50) NOT NULL,
    room_size int,
    room_number int,
    image VARCHAR(100),
    room_desc VARCHAR(999)
);


CREATE TABLE RoomAccomodations(
	room_id VARCHAR(20),
    accomodation VARCHAR(20) NOT NULL,
    PRIMARY KEY (room_id, accomodation),
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
);
    



    