import sqlite3

def query_frequent_morning_destinations(cursor, n_stations):
    query = f"""
        WITH MorningTrips AS (
            SELECT 
                t.trip_id,
                t.trip_headsign,
                MIN(st.departure_time) AS initial_departure
            FROM trips t
            JOIN stop_times st ON t.trip_id = st.trip_id
            JOIN calendar_dates cd ON t.service_id = cd.service_id
            WHERE cd.exception_type = 1
            GROUP BY t.trip_id, t.trip_headsign
            HAVING MIN(st.departure_time) < '12:00:00'
        )
        SELECT 
            trip_headsign AS terminal_destination,
            COUNT(*) AS total_morning_trips
        FROM MorningTrips
        WHERE trip_headsign IS NOT NULL AND trip_headsign != ''
        GROUP BY terminal_destination
        ORDER BY total_morning_trips DESC
        LIMIT {n_stations};
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print(f"Top {n_stations} Morning Terminal Destinations (Departures before 12:00 PM):")
    for rank, (destination, count) in enumerate(results, 1):
        print(f"{rank}. {destination} — {count:,} trips")