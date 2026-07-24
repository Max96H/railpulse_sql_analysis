import sqlite3


def query_peak_hour(cursor):
    query = """
        SELECT 
            strftime('%H', departure_time) AS peak_hour, 
            COUNT(*) AS frequency
        FROM stop_times
        GROUP BY peak_hour
        ORDER BY frequency DESC
        LIMIT 1;
    """
    query2 = """
        SELECT 
            substr(departure_time, 1, 2) AS peak_hour, 
            COUNT(*) AS frequency
        FROM stop_times
        GROUP BY peak_hour
        ORDER BY frequency DESC
        LIMIT 1;
    """
    query3 = """
        SELECT 
            substr(st.departure_time, 1, 2) AS peak_hour, 
            COUNT(*) AS total_active_departures
        FROM stop_times st
        JOIN trips t 
            ON st.trip_id = t.trip_id
        JOIN calendar_dates cd 
            ON t.service_id = cd.service_id
        WHERE st.departure_time IS NOT NULL 
        AND cd.exception_type = 1 -- Only count trips active on service dates
        GROUP BY peak_hour
        ORDER BY total_active_departures DESC
        LIMIT 1;
    """

    cursor.execute(query3)
    result = cursor.fetchone()

    if result:
        hour, count = result
        print(f"Peak hour is between {hour}h and {int(hour) + 1}h with {count} total trains departing across the year in Belgium.")

    query = """
    WITH HourlyStats AS (
        SELECT 
            substr(st.departure_time, 1, 2) AS dep_hour,
            COUNT(*) AS total_departures,
            COUNT(DISTINCT cd.date) AS unique_days_operating
        FROM stop_times st
        JOIN trips t ON st.trip_id = t.trip_id
        JOIN calendar_dates cd ON t.service_id = cd.service_id
        WHERE st.departure_time IS NOT NULL 
        AND cd.exception_type = 1
        GROUP BY dep_hour
    )
    SELECT 
        dep_hour,
        total_departures,
        unique_days_operating,
        ROUND(CAST(total_departures AS REAL) / unique_days_operating, 2) AS avg_departures_per_day
    FROM HourlyStats
    ORDER BY avg_departures_per_day DESC
    LIMIT 1;
    """

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        hour, total, days, avg = result
        print(f"Peak Hour: {hour}:00")
        print(f"Average Departures/Day: {avg}")
        print(f"Based on {total} total departures across {days} active service days.")

