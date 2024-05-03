from requests import Session
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }


def get_quotes_authors():
    work = Session()

    work.get("https://quotes.toscrape.com/", headers=headers)

    responce = work.get("https://quotes.toscrape.com/login", headers=headers)

    soup = BeautifulSoup(responce.text, "lxml")

    csrf_token = soup.find("input").get("value")
    data = {
            "csrf_token": csrf_token,
            "username": "username",
            "password": "password"
            }

    result = work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True)

    soup = BeautifulSoup(result.text, "lxml")

    page = 0

    while True:
        page += 1
        # sleep(2)
        data = work.get(f"https://quotes.toscrape.com/page/{page}/", headers=headers)

        soup = BeautifulSoup(data.text, "lxml")

        quotes = [span.text.strip() for span in soup.find_all('span', class_='text')]
        authors = [span.text.strip() for span in soup.find_all("small", class_="author")]
        if not quotes:
            break
        quotes_authors = dict(map(lambda kv: (kv[0].strip(), kv[1].strip()), zip(quotes, authors)))
        print("получение цитаты", quotes_authors)
        yield quotes_authors


def writer(parametr):

    book = xlsxwriter.Workbook(r'/data1.xlsx')
    page = book.add_worksheet('цитаты')

    row = 0
    column = 0

    page.set_column("A:A", 150)
    page.set_column("B:B", 10)

    quotes_authors = parametr
    for item in parametr:
        for k,v in item.items():
            page.write(row, column, k)
            page.write(row, column + 1, v)

            row += 1

    print("цитата  записана")
    book.close()


writer(get_quotes_authors())
