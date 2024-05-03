import json
import time
import asyncio
import aiohttp
import csv
from bs4 import BeautifulSoup
import datetime

start_time = time.time()


async def get_page_data(session, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
    url = f"https://www.labirint.ru/genres/2308/?paperbooks=1&available=1&page={page}"

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")

        data = soup.find("div", class_="genres-catalog").find("div",
                                                              class_="catalog-responsive outer-catalog catalog") \
            .find("div", "inner-catalog").find("div", class_="content-block-outer") \
            .find_all("div", class_="genres-carousel__item")

        books_on_page = []

        for i in data:
            try:
                name = i.find('div', class_="product-cover").find("span", class_="product-title").text
            except:
                name = None

            try:
                author = i.find("div", class_="product-author").find("a").text
            except:
                author = None

            try:
                pubhouse = i.find("div", class_="product-pubhouse").find("a",
                                                                         class_="product-pubhouse__pubhouse").text \
                           + ":" + i.find("div", class_="product-pubhouse").find("a",
                                                                                 class_="product-pubhouse__series").text.strip()
            except:
                pubhouse = None

            try:
                discounted_price = i.find("div", class_="product-cover").find("div", class_="price") \
                                       .find("span", class_="price-val").find("span").text + "₽"
            except:
                discounted_price = None

            try:
                price = i.find("div", class_="product-cover").find("div", class_="price") \
                            .find("span", class_="price-old").find("span").text + "₽"
            except:
                price = None

            books_on_page.append({
                "name": name,
                "author": author,
                "pubhouse": pubhouse,
                "discounted_price": discounted_price,
                "price": price,
            })

        print(f"[INFO] Обработана страница {page}")

        return books_on_page


async def gather_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }

    url = "https://www.labirint.ru/genres/2308/?paperbooks=1&available=1"

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        page_count = soup.find("div", class_="pagination-numbers").find_all("a")[-1].text
        tasks = []

        for page in range(1, int(page_count) + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def main():
    loop = asyncio.get_event_loop()
    book_data = loop.run_until_complete(gather_data())
    loop.close()

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}_async.json", "w", encoding="utf-8") as file:
        json.dump(book_data, file, indent=4, ensure_ascii=False)

    with open(f"labirint_{cur_time}_async.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Название книги",
            "Автор",
            "Издательство",
            "Цена со скидкой",
            "Цена без скидки",
        ])

        for page in book_data:
            for book in page:
                writer.writerow([
                    book["name"],
                    book["author"],
                    book["pubhouse"],
                    book["discounted_price"],
                    book["price"],
                ])

    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time} секунд")


if __name__ == "__main__":
    main()
