from flask import Flask
import psycopg2
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = 'postgres://postgresql_8byt_user:VOxGZcJm7VAHff' \
               'DpDeZ3o01bojUnhz7H@dpg-cim3mdtgkuvinfm5tkvg-a.oregon-postgres.render.com/postgresql_8byt'


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = psycopg2.connect(DATABASE_URL)
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.commit()
    db.close()


create_db()
