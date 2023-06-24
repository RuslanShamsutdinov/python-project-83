import psycopg2
from psycopg2 import extras, sql
import logging
import os
from page_analyzer.data_tools import refactor_data
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_all_from_urls_db():
    """Get all data from Database. Return dictionary"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls ORDER BY id')
        url_list = refactor_data(curs.fetchall())
        if url_list:
            return url_list
        return None
    
def get_all_urls_checkurl():
    """Get all data from Database. Return dictionary"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as curs:
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
        url_list = refactor_data(curs.fetchall())
        if url_list:
            return url_list
        return None
    


def get_by_name(table, name):
    """Get data by name from Database. Return dictionary"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute(sql.SQL("SELECT * FROM {} WHERE name = %s LIMIT 1").format(sql.Identifier(table)), (name,))
        url = curs.fetchone()
        if url:
            return url
        return None


def get_by_id(table, url_id):
    """Get data by id from Database. Return dictionary"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute(sql.SQL("SELECT * FROM {} WHERE id = %s LIMIT 1").format(sql.Identifier(table)), (url_id,))
        url = curs.fetchone()
        if url:
            return url
        return None


def insert_into_urls(name, created_at):
    conn = psycopg2.connect(DATABASE_URL)
    
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute("INSERT INTO urls (name, created_at) VALUES(%s, %s) RETURNING id", (name, created_at))
        id_url = curs.fetchone()
    return id_url

def insert_into_url_checks(url_id=None, status_code=None, h1=None, title=None, description=None, created_at=None):
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as curs:
        curs.execute("INSERT INTO url_checks (url_id, created_at, status_code, h1, title, description, created_at ) "
                     "VALUES(%s, %s) RETURNING id", (url_id, created_at, status_code, h1, title, description, created_at))
