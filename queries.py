create_table_trip_query = """
CREATE TABLE IF NOT EXISTS trip (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(255),
    trip_total DECIMAL(6,2),
    tips DECIMAL(5,2),
    payment_type VARCHAR(255)
)
"""
create_table_dim_location = """
CREATE TABLE IF NOT EXISTS Dim_location (
    location_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pickup_location VARCHAR(255),
    dropoff_location VARCHAR(255)
)
"""
create_table_dim_time = """
CREATE TABLE IF NOT EXISTS Dim_time (
    time_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    trip_start_timestamp DATETIME,
    trip_end_timestamp DATETIME,
    trip_seconds INT
)
"""
create_table_dim_payment = """
CREATE TABLE IF NOT EXISTS Dim_payment (
    payment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    payment_type VARCHAR(255),
    trip_total FLOAT,
    fare FLOAT,
    tips FLOAT,
    tolls FLOAT,
    extras FLOAT
)
"""
create_table_dim_taxi = """
CREATE TABLE IF NOT EXISTS Dim_taxi (
    taxi_id VARCHAR(255) PRIMARY KEY,
    company VARCHAR(255)
)
"""
create_table_dim_trips = """
CREATE TABLE IF NOT EXISTS Trips (
    unique_key VARCHAR(255) NOT NULL PRIMARY KEY,
    taxi_id VARCHAR(255) NOT NULL,
    time_id INT,
    location_id INT,
    payment_id INT,
    trip_miles FLOAT,
    CONSTRAINT FK_taxi_trip FOREIGN KEY (taxi_id) REFERENCES Dim_taxi(taxi_id),
    CONSTRAINT FK_time_trip FOREIGN KEY (time_id) REFERENCES Dim_time(time_id),
    CONSTRAINT FK_location_trip FOREIGN KEY (location_id) REFERENCES Dim_location(location_id),
    CONSTRAINT FK_payment_trip FOREIGN KEY (payment_id) REFERENCES Dim_payment(payment_id)
)
"""


#### Inserts
insert_dim_location_query = """
INSERT INTO Dim_location (pickup_location, dropoff_location)
VALUES ( %s, %s )
"""
insert_dim_time_query = """
INSERT INTO Dim_time (trip_start_timestamp, trip_end_timestamp, trip_seconds)
VALUES ( %s, %s, %s )
"""
insert_dim_payment_query = """
INSERT INTO Dim_payment (payment_type, trip_total, fare, tips, tolls, extras)
VALUES ( %s, %s, %s, %s ,%s, %s )
"""
insert_dim_taxi_query = """
INSERT INTO Dim_taxi (taxi_id, company)
VALUES ( %s, %s )
"""
insert_trips_query = """
INSERT INTO Trips (unique_key, taxi_id, time_id, location_id, payment_id, trip_miles)
VALUES ( %s, %s, %s, %s, %s, %s )
"""