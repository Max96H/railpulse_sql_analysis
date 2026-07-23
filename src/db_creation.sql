-- Turn on foreign key enforcement in SQLite
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS calendar_dates;
DROP TABLE IF EXISTS calendar;
-- DROP TABLE IF EXISTS feed_info;
DROP TABLE IF EXISTS stops;
DROP TABLE IF EXISTS stop_times;
DROP TABLE IF EXISTS transfers;
DROP TABLE IF EXISTS trips;
-- DROP TABLE IF EXISTS routes;

-- Create 'calendar_dates' table
CREATE TABLE IF NOT EXISTS calendar_dates (
    date              TEXT NOT NULL,
    exception_type    INTEGER NOT NULL,
    service_id        TEXT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES calendar (service_id)
);

-- Create 'calendar' table 
CREATE TABLE IF NOT EXISTS calendar (
    end_date      INTEGER NOT NULL,
    friday        INTEGER NOT NULL,
    monday        INTEGER NOT NULL,
    saturday      INTEGER NOT NULL,
    service_id    TEXT PRIMARY KEY,
    start_date    INTEGER NOT NULL,
    sunday        INTEGER NOT NULL,
    thursday      INTEGER NOT NULL,
    tuesday       INTEGER NOT NULL,
    wednesday     INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS stops (
    location_type        INTEGER NOT NULL,
    parent_station       TEXT,
    platform_code        TEXT,
    stop_code            REAL,
    stop_desc            TEXT NOT NULL,
    stop_id              TEXT PRIMARY KEY,
    stop_lat             REAL NOT NULL,
    stop_lon             REAL NOT NULL,
    stop_name            TEXT NOT NULL,
    stop_url             TEXT,
    wheelchair_boarding  INTEGER,
    zone_id              TEXT
);


CREATE TABLE IF NOT EXISTS stop_times (
    arrival_time         TEXT NOT NULL,
    departure_time       TEXT NOT NULL,
    drop_off_type        INTEGER NOT NULL,
    pickup_type          INTEGER NOT NULL,
    shape_dist_traveled  REAL,
    stop_headsign        TEXT,
    stop_id              TEXT,
    stop_sequence        INTEGER NOT NULL,
    trip_id              TEXT,
    FOREIGN KEY (stop_id) REFERENCES stops (stop_id),
    FOREIGN KEY (trip_id) REFERENCES trips (trip_id)

);

CREATE TABLE IF NOT EXISTS trips (
    bikes_allowed         REAL,
    block_id              INTEGER NOT NULL,
    direction_id          INTEGER,
    route_id              TEXT NOT NULL,
    service_id            TEXT NOT NULL,
    shape_id              REAL,
    trip_headsign         TEXT NOT NULL,
    trip_id               TEXT PRIMARY KEY,
    trip_short_name       INTEGER NOT NULL,
    wheelchair_accessible INTEGER,

    --FOREIGN KEY (route_id) REFERENCES routes (route_id)
    FOREIGN KEY (service_id) REFERENCES calendar (service_id)

);

CREATE TABLE IF NOT EXISTS transfers (
    from_stop_id      TEXT NOT NULL,
    min_transfer_time INTEGER NOT NULL,
    to_stop_id        TEXT NOT NULL,
    transfer_type     INTEGER NOT NULL,
    from_trip_id      TEXT,
    to_trip_id        TEXT,

    FOREIGN KEY (from_stop_id) REFERENCES stops (stop_id),
    FOREIGN KEY (to_stop_id) REFERENCES stops (stop_id),
    FOREIGN KEY (from_trip_id) REFERENCES trips (from_trip_id),
    FOREIGN KEY (to_trip_id) REFERENCES trips (from_trip_id)

);



















-- 3. Create an index for faster search queries on order dates
--CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
