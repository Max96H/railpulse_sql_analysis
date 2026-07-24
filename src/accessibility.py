import sqlite3

def query_accessibility(cursor):
    query = """
        WITH RouteBikeStats AS (
            SELECT 
                r.route_id,
                r.route_long_name AS route_name,
                r.route_short_name as short_name,
                COUNT(DISTINCT t.trip_id) AS total_active_trips,
                COUNT(DISTINCT CASE WHEN t.bikes_allowed = 1 THEN t.trip_id END) AS bike_allowed_trips
            FROM routes r
            JOIN trips t ON r.route_id = t.route_id
            JOIN calendar_dates cd ON t.service_id = cd.service_id
            WHERE cd.exception_type = 1
            GROUP BY r.route_id, route_name
        )
        SELECT 
            route_id,
            route_name,
            bike_allowance_ratio,
            bike_allowed_percentage,
            total_active_trips
        FROM (
            SELECT 
                route_id,
                route_name,
                bike_allowed_trips || '/' || total_active_trips AS bike_allowance_ratio,
                ROUND(CAST(bike_allowed_trips AS REAL) * 100.0 / total_active_trips, 2) AS bike_allowed_percentage,
                total_active_trips
            FROM RouteBikeStats
            WHERE short_name != 'BUS'
        )
        ORDER BY bike_allowed_percentage ASC, total_active_trips DESC
        LIMIT 10;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("Lowest Scoring Routes for Bicycle Storage Availability:")
    print("=" * 65)
    print(f"{'Route ID':<10} | {'Route Name':<25} | {'Ratio':<10} | {'Bikes Allowed %'}")
    print("-" * 65)

    for route_id, route_name, ratio, pct, total in results:
        print(f"{route_id:<10} | {route_name[:25]:<25} | {ratio:<10} | {pct:>6.2f}%")