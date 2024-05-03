from requests import Session
from bs4 import BeautifulSoup
from time import sleep
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }

# ex6 Scraping Infinite Scrolling Pages (Ajax)
base_url = "https://scrapingclub.com/exercise/list_infinite_scroll/"


def main(base_url):
    s = Session()
    s.headers.update(headers)

    count = 1
    pagination = 0
    while True:
        sleep(3)
        if count > 1:
            url = base_url + "?page=" + str(count)
            print("url", url)
        else:
            url = base_url
            print("url", url)

        responce = s.get(url)

        soup = BeautifulSoup(responce.text, "lxml")

        if count == 1:
            data = soup.find_all("span", class_="page")
            pagination = str(data[-2])[-13]
            # print("pagination", pagination)

        cards = soup.find_all("div", class_="w-full rounded border post")

        for card in cards:
            name = card.find("h4").text
            price = soup.find("h5").text
            print(name, price)

        if count == int(pagination):
            print("конец")
            break
        else:
            count += 1



main(base_url)
