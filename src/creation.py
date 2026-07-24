import sqlite3


def creating_tables(conn, cursor):
    try:
        with open("./src/db_creation.sql") as file:
            create_tables_script = file.read()

        cursor.executescript(create_tables_script)
        conn.commit()
    except sqlite3.Error as e:
        print("Error :", e)
        conn.rollback()