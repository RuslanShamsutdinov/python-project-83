from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = psycopg2.connect(DATABASE_URL)
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()
    db.close()

print(DATABASE_URL)
create_db()
