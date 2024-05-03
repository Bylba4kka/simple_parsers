import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {"User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


def download(url):
    responce = requests.get(url, stream=True)
    r = open("C:\\Users\\aleks\\OneDrive\\Pycharm_Projects\\parsing\\image\\" + url.split("/")[-1], "wb")
    for value in responce.iter_content(1024*1024):
        r.write(value)
    r.close()
    print('Картинка успешно загружена')


def get_url():
    for count in range(1, 7):
        url = f" exercise/list_basic/?page={count}"

        responce = requests.get(url, headers=headers)

        soup = BeautifulSoup(responce.text, "lxml")  # lxml and html.parser

        data = soup.find_all("div", class_="w-full rounded border")

        for i in data:
            card_url = "https://scrapingclub.com" + i.find("a").get("href")
            print("Получение ссылки:", card_url)
            yield card_url


def array():
    for card_url in get_url():

        responce = requests.get(card_url, headers=headers)
        sleep(3)
        soup = BeautifulSoup(responce.text, "lxml")  # lxml and html.parser

        data = soup.find("div", class_="my-8 w-full rounded border")
        name = data.find("h3").text
        ulr_img = "https://scrapingclub.com" + data.find("img").get('src')
        price = data.find("h4").text
        description = data.find(class_="card-description").text
        print("Получение информации с карточки", name)
        download(ulr_img)
        yield name, price, description, ulr_img