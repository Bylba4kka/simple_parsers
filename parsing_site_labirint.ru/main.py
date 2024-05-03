import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv
# название книги, автор, издательство, цена со скидкой, цена без скидки

start_time = time.time()

headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
            "Название книги",
            "Автор",
            "Издательство",
            "Цена со скидкой",
            "Цена без скидки",
            )
        )


    url = "https://www.labirint.ru/genres/2308/?paperbooks=1&available=1"

    responce = requests.get(url, headers=headers)

    soup = BeautifulSoup(responce.text, "lxml")

    page_count = soup.find("div", class_="pagination-numbers").find_all("a")[-1].text

    book_data = list()

    for page in range(1, int(page_count) + 1):
        url = f"https://www.labirint.ru/genres/2308/?paperbooks=1&available=1&page={page}"

        responce = requests.get(url, headers=headers)
        soup = BeautifulSoup(responce.text, "lxml")

        data = soup.find("div", class_="genres-catalog").find("div", class_="catalog-responsive outer-catalog catalog") \
            .find("div", "inner-catalog").find("div", class_="content-block-outer") \
            .find_all("div", class_="genres-carousel__item")

        for i in data:
            try:
                name = i.find('div', class_="product-cover").find("span", class_="product-title").text
            except:
                name = None
            # print("Название книги:", name)  # РАБОТАЕТ

            try:
                author = i.find("div", class_="product-author").find("a").text
            except:
                author = None
            # print("Автор:", author)

            try:
                pubhouse = i.find("div", class_="product-pubhouse").find("a", class_="product-pubhouse__pubhouse").text \
                + ":" + i.find("div", class_="product-pubhouse").find("a", class_="product-pubhouse__series").text.strip()
            except:
                pubhouse = None
            # print("Издательство:", pubhouse)

            try:
                discounted_price = i.find("div", class_="product-cover").find("div", class_="price")\
                    .find("span", class_="price-val").find("span").text + "₽"
            except:
                discounted_price = None
            # print("Цена со скидкой:", discounted_price) # РАБОТАЕТ
            try:
                price = i.find("div", class_="product-cover").find("div", class_="price")\
                    .find("span", class_="price-old").find("span").text + "₽"
            except:
                price = None
            # print("Цена без скидки:", price) # РАБОТАЕТ
            book_data.append(
                {
                    "name": name,
                    "author": author,
                    "pubhouse": pubhouse,
                    "discounted_price": discounted_price,
                    "price": price,
                }
            )

            with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name,
                        author,
                        pubhouse,
                        discounted_price,
                        price,
                    )
                )
        print(f"Обработана страница {page}/{page_count}")

        time.sleep(1)

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(book_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время:", finish_time)


if __name__ == "__main__":
    main()
