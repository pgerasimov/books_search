import requests
from config import DEVELOPER_KEY
from bs4 import BeautifulSoup


def main():
    isbn = '0441172717'
    url = 'https://www.goodreads.com/book/isbn/{}?key={}'.format(
        isbn,
        DEVELOPER_KEY)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml-xml')
    print(soup.find('name').text)  # возвращает имя и фамилию автора по isbn


if __name__ == '__main__':
    main()
