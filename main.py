import csv
#import pandas as pd
import io
import sqlite3
from src.cleaning import clean_row_generator
from src.fetcher import download_gtfs
from src.peak_hour import query_peak_hour
from src.busy_platforms import query_busiest_platforms
from src.diagnosis import diagnose
from src.morning_destinations import query_frequent_morning_destinations
from src.service_frequency import query_service_frequency
"""
pd.set_option("display.max_columns", None)
# Don't truncate text inside individual cell values
pd.set_option("display.max_colwidth", None)
# Prevents wide tables from wrapping onto a new line below
pd.set_option("display.width", None)
"""
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
        try:
            with open("./src/db_creation.sql") as file:
                create_tables_script = file.read()

            cursor.executescript(create_tables_script)
            conn.commit()
        except sqlite3.Error as e:
            print("Error :", e)
            conn.rollback()
        cursor.close()
        conn.close()
        return
    extraction = ""
    while not extraction in ("y", "n"):
        extraction = input("Do you want to extract and insert data from the API to db? (y|n)\n")

    if extraction == "y":
        gtfs_zip = download_gtfs()
        for document in gtfs_zip.namelist():
            if not document.endswith(".txt") or document in ("agency.txt", "feed_info.txt", "routes.txt", "transfers.txt", "translations.txt"):
                continue
            binary_file = gtfs_zip.open(document)
            """
            doc_df = pd.read_csv(binary_file)
            print("_" * 50)
            print(document, ":\n")
            print(doc_df.info(), "\n")
            print(doc_df.head(), "\n")
            """
            text_file = io.TextIOWrapper(binary_file, encoding="utf-8-sig")
            reader = csv.reader(text_file)
            table_name = document.removesuffix(".txt")
            
            headers = next(reader)

            
            columns_str = ", ".join(headers)
            placeholders = ", ".join(["?"] * len(headers))
            sql_query = (
                f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})'
            )

            # Batch insert
            cursor.executemany(sql_query, clean_row_generator(reader))
            conn.commit()


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

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()