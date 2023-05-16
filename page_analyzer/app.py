from flask import Flask

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Flask! Checking'
