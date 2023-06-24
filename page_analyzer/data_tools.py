import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def refactor_data(data):
    if data is not None:
        new_dict = dict(zip(['id', 'name', 'created_at'], data))
        return new_dict
    else:
        return None


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
        return {'h1': h1,
                'title': title,
                'description': description['content']}
    except Exception:
        raise Exception('Ошибка при проверке сайта')


