import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def parse(name):
    data = urlparse(name)
    return f'{data.scheme}://{data.hostname}'


def analyze_page(url):
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
