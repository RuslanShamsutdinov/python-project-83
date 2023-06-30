import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime


def get_date():
    d = datetime.now().strftime('%Y-%m-%d')
    return d


def refactor_url(name):
    data = urlparse(name)
    return f'{data.scheme}://{data.hostname}'


def check_status_code(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception:
        raise Exception('Ошибка при проверке сайта')


def page_analyzer(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        h1 = soup.find('h1')
        title = soup.find('title')
        description = soup.find('meta', attrs={'name': 'description'})
        return {'h1': h1.text if h1 else None,
                'title': title.text if title else None,
                'description': description['content']
                if description and 'content' in description.attrs else None}
    except Exception:
        raise Exception('Ошибка при проверке сайта')
