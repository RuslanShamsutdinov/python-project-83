from flask import Flask, render_template, request, url_for, flash, redirect, g
import validators
from datetime import datetime
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from page_analyzer.db_tools import get_by_name, get_by_id, get_all_from_urls_db, insert_into_urls, \
    insert_into_url_checks
import logging
from page_analyzer.data_tools import check_status_code, page_analyzer

from page_analyzer.data_tools import refactor_url, refactor_data

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key"

DATABASE_URL = os.getenv('DATABASE_URL')


@app.route("/", methods=["POST", "GET"])  # Главная страница, Анализатор страниц
def index():
    return render_template('index.html')


@app.route("/urls", methods=["POST", "GET"])  # Сайты
def urls():
    table = 'urls'
    if request.method == 'GET':
        data = get_all_from_urls_db()
        return render_template('urls.html', data=data)
    elif request.method == 'POST':
        get_url = request.form.get('url')
        validation = validators.url(get_url, public=True)
        if validation:
            created_at = datetime.now().strftime('%Y-%m-%d')
            name = refactor_url(get_url)
            if not get_by_name(table, name):
                url_id = insert_into_urls(name, created_at)
                flash('Страница успешно добавлена', 'success')
            else:
                url_id=get_by_name('urls', name)[0]
                flash('Страница уже существует', 'warning')
            return redirect(url_for('url_page', url_id=url_id))
        else:
            flash('Некорректный URL!', 'danger')
            return render_template('index.html'), 422


@app.route("/urls/<int:url_id>")
def url_page(url_id):
    url = get_by_id('urls', url_id)
    check_url = refactor_data(get_by_id('url_checks', url_id))
    if not url:
        return render_template('404.html')
    return render_template('url_id.html', check_url=check_url)



@app.route("/urls/<id>/checks", methods=["POST"])
def url_check(url_id):
    try:
        status_code = check_status_code(url_id)
        parsed_data = page_analyzer(url_id)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_id', url_id=url_id))
    dt = datetime.now().strftime('%Y-%m-%d')
    insert_into_url_checks(url_id=url_id, status_code=status_code, **parsed_data, created_at=dt)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_id', url_id=url_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

# sudo service postgresql start
