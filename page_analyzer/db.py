import psycopg2.extras
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_all_from_url_checks(url_id):
    """Get all data from Database. Return dictionary"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as curs:
        curs.execute("SELECT *  FROM url_checks WHERE url_id = %s"
                     " ORDER BY id DESC", (url_id,))
        url_list = curs.fetchall()
        conn.close()
        if url_list:
            return url_list
            # return [dict(i) for i in url_list]
        return None


def get_all_urls_checkurl():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as curs:
        curs.execute("""
                SELECT urls.id, urls.name,
                url_checks.created_at,
                url_checks.status_code
                FROM urls
                LEFT OUTER JOIN url_checks
                ON urls.id = url_checks.url_id
                AND url_checks.id = (
                    SELECT MAX(id)
                    FROM url_checks
                    WHERE url_checks.url_id = urls.id
                )
                ORDER BY urls.id DESC
                """)
        url_list = curs.fetchall()
        conn.close()
        if url_list:
            return url_list
            # return [dict(i) for i in url_list]
        return None


def insert_into_urls(name, created_at):
    conn = psycopg2.connect(DATABASE_URL)

    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute("INSERT INTO urls (name, created_at) VALUES(%s, %s)"
                     " RETURNING id", (name, created_at))
        id_url = curs.fetchone()
        conn.close()
    return id_url[0]


def insert_into_url_checks(url_id, status_code,
                           h1, title, description, created_at):
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute("INSERT INTO url_checks "
                     "(url_id, status_code, h1, title, "
                     "description, created_at ) "
                     "VALUES(%s, %s, %s, %s, %s, %s) RETURNING id",
                     (url_id, status_code, h1, title, description, created_at))
        conn.close()


def get_from_db(table, db_column, data):
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as curs:
        curs.execute(sql.SQL("SELECT * FROM {} WHERE {} = %s LIMIT 1")
                     .format(sql.Identifier(table),
                             sql.Identifier(db_column)), (data,))
        url = curs.fetchone()
        conn.close()
        if url:
            return url
        return None
