import sqlite3

def query_service_frequency(cursor):
    query = """
        WITH ServiceDayTypes AS (
            SELECT 
                service_id,
                -- Converts 'YYYYMMDD' string to 'YYYY-MM-DD' so strftime('%w') can extract the weekday (0-6)
                COUNT(DISTINCT strftime('%w', substr(date, 1, 4) || '-' || substr(date, 5, 2) || '-' || substr(date, 7, 2))) AS distinct_weekdays
            FROM calendar_dates
            WHERE exception_type = 1 -- Only active service dates
            GROUP BY service_id
        ),
        CategorizedServices AS (
            SELECT 
                service_id,
                CASE 
                    WHEN distinct_weekdays >= 5 THEN 'High Frequency'
                    WHEN distinct_weekdays BETWEEN 2 AND 4 THEN 'Medium Frequency'
                    ELSE 'Low Frequency/Special'
                END AS frequency_category
            FROM ServiceDayTypes
        )
        SELECT 
            frequency_category,
            COUNT(*) AS service_count,
            ROUND(
                CAST(COUNT(*) AS REAL) * 100.0 / (SELECT COUNT(DISTINCT service_id) FROM calendar_dates WHERE exception_type = 1), 
                2
            ) AS percentage
        FROM CategorizedServices
        GROUP BY frequency_category
        ORDER BY service_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Print formatted breakdown
    print("Service Frequency Distribution (Strategy 2 - Distinct Weekdays):")
    print("=" * 60)
    print(f"{'Frequency Category':<24} | {'Services':<10} | {'Percentage'}")
    print("-" * 60)

    for category, count, percentage in results:
        print(f"{category:<24} | {count:<10,} | {percentage:>6.2f}%")