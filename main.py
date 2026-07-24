import sqlite3
from src.creation import creating_tables
from src.insertion import inserting_data
from src.peak_hour import query_peak_hour
from src.busy_platforms import query_busiest_platforms
from src.diagnosis import diagnose
from src.morning_destinations import query_frequent_morning_destinations
from src.service_frequency import query_service_frequency
from src.accessibility import query_accessibility


def main():
    conn = sqlite3.connect("./data/sncb.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    # faster than journal
    # conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()

    #diagnose(cursor)

    # Create tables once
    creation = ""
    while not creation in ("y", "n"):
        creation = input("Do you want to recreate the tables of the database? (y|n) \n")

    if creation == "y":
        creating_tables(conn, cursor)

    extraction = ""
    while not extraction in ("y", "n"):
        extraction = input("Do you want to extract and insert data from the API to db? (y|n)\n")

    if extraction == "y":
        inserting_data(conn, cursor)

    elif creation == "y":
        cursor.close()
        conn.close()
        return


    q_peak_hour = input("Do you wish to query the peak hour ? (y|n)\n")
    if q_peak_hour == "y":
        query_peak_hour(cursor)

    q_busy_platforms = input("Do you wish to know the busiest platforms ? (y|n)\n")
    if q_busy_platforms == "y":
        station = input("From wich station ? (Default: 'Bruxelles-Central')\n")
        n_platforms = input("Top how many? (Default: 3)\n")
        if not station:
            station = 'Bruxelles-Central'
        if not n_platforms:
            n_platforms = 3
        query_busiest_platforms(cursor, station, n_platforms)

    q_morning_destinations = input("Do you wish to know most frequent morning destinations? (y|n)\n")
    if q_morning_destinations == "y":
        n_stations = input("Top how many? (Default: 3)\n")
        query_frequent_morning_destinations(cursor, n_stations)

    q_service_freq = input("Do you wish to see and add service frequencies ? (y|n)\n")
    if q_service_freq == "y":
        query_service_frequency(cursor)

    q_accessibility = input("Do you wish to do an accessibility audit? (y|n)\n")
    if q_accessibility == "y":
        query_accessibility(cursor)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()