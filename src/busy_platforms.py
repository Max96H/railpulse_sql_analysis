import sqlite3

def query_busiest_platforms(cursor, station, n_platforms):
    query = f"""
        SELECT 
            COALESCE(p.platform_code, p.stop_name, p.stop_id) AS platform,
            COUNT(*) AS total_stop_events
        FROM stop_times st
        JOIN trips t ON st.trip_id = t.trip_id
        JOIN calendar_dates cd ON t.service_id = cd.service_id
        JOIN stops p ON st.stop_id = p.stop_id
        JOIN stops station 
            ON p.parent_station = station.stop_id OR p.stop_id = station.stop_id
        WHERE station.stop_name LIKE '%{station}%'
        AND cd.exception_type = 1
        GROUP BY platform
        ORDER BY total_stop_events DESC
        LIMIT {n_platforms};
    """

    cursor.execute(query)
    busiest_platforms = cursor.fetchall()

    print(f"Top {n_platforms} Busiest Platforms at {station}:")
    for rank, (platform, count) in enumerate(busiest_platforms, 1):
        print(f"Rank {rank}: Platform {platform} - {count:,} total scheduled stops")