from fetcher import download_gtfs
from cleaning import clean_row_generator
import io
import csv
#import pandas as pd
"""
pd.set_option("display.max_columns", None)
# Don't truncate text inside individual cell values
pd.set_option("display.max_colwidth", None)
# Prevents wide tables from wrapping onto a new line below
pd.set_option("display.width", None)
"""

def inserting_data(conn, cursor):
    gtfs_zip = download_gtfs()
    for document in gtfs_zip.namelist():
        if not document.endswith(".txt") or document in ("agency.txt", "feed_info.txt", "transfers.txt", "translations.txt"):
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