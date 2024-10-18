import psycopg2
import os

dbname=os.getenv("DB_NAME")
dbuser=os.getenv("DB_USERNAME")
dbpass=os.getenv("DB_PASS")
dbhost=os.getenv("DB_HOST")
conn = psycopg2.connect(f"dbname={dbname} user={dbuser} password={dbpass} host={dbhost}")


def truncate_table(table):
    cur = conn.cursor()
    cur.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")
    conn.commit()
    cur.close()

truncate_table("items")