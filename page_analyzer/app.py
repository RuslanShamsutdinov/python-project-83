from flask import Flask, render_template, request, url_for, flash, redirect
import validators
from .db import get_from_db, get_all_urls_checkurl, \
    get_all_from_url_checks, insert_into_urls, \
    insert_into_url_checks
from .urls import analyze_page, \
    parse
from datetime import datetime
from dotenv import load_dotenv
import requests
import logging
import os


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a")
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_key"
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

DATABASE_URL = os.getenv('DATABASE_URL')


@app.route("/", methods=["POST", "GET"])
def index():
    logging.debug('index')
    return render_template('index.html')


@app.route("/urls", methods=["POST", "GET"])
def urls():
    logging.debug('urls')
    if request.method == 'GET':
        data = get_all_urls_checkurl()
        return render_template('urls.html', data=data)
    elif request.method == 'POST':
        get_url = request.form.get('url')
        validation = validators.url(get_url, public=True)
        if validation:
            created_at = datetime.now().strftime('%Y-%m-%d')
            name = parse(get_url)
            table = 'urls'
            if not get_from_db(table, 'name', name):
                url_id = insert_into_urls(name, created_at)
                flash('Страница успешно добавлена', 'success')
            else:
                url_id = get_from_db(table, 'name', name).id
                flash('Страница уже существует', 'warning')
            return redirect(url_for('url_page', url_id=url_id))
        else:
            flash('Некорректный URL!', 'danger')
            return render_template('index.html'), 422


@app.route("/urls/<int:url_id>")
def url_page(url_id):
    url = get_from_db('urls', 'id', url_id)
    check_url = get_all_from_url_checks(url_id)
    if not url:
        return render_template('404.html')
    return render_template('url_id.html', url=url, check_url=check_url)


@app.route('/url/<int:url_id>/checks', methods=["POST"])
def url_check(url_id):
    logging.info('def url_check')
    url_name = get_from_db('urls', 'id', url_id).name
    try:
        status_code = requests.get(url_name).status_code
        parsed_data = analyze_page(url_name)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_page', url_id=url_id))
    date = datetime.now().strftime('%Y-%m-%d')
    insert_into_url_checks(url_id=url_id, status_code=status_code,
                           **parsed_data, created_at=date)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_page', url_id=url_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
