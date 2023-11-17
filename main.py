import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

from model import Product

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}


def parser(url: str, max_item: int):
    global list_product
    create_csv()

    page = 1
    count_items = 0

    while max_item > count_items and page < 23:
        item_url_list = []
        actual_price_list = []
        old_price_list = []

        sleep(0)
        res = requests.get(f"{url}&page={page}", headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        products = soup.find_all("div",
                                 class_="catalog-2-level-product-card product-card subcategory-or-type__products-item with-rating with-prices-drop")

        for product in products:
            list_product = []
            sleep(0)
            if count_items >= max_item:
                break
            count_items += 1
            item_url = "https://online.metro-cc.ru" + product.find("a").get("href")
            item_url_list.append(item_url)

            actual_price_elem = product.find("div", class_="product-unit-prices__actual-wrapper")
            actual_price = actual_price_elem.findNext("span", class_="product-price__sum-rubles").text.replace(" ", "")
            actual_price_list.append(actual_price)

            old_price_elem = product.find("div", class_="product-unit-prices__old-wrapper")
            old_price = old_price_elem.findNext("span", class_="product-price__sum-rubles").text.replace(" ", "")
            old_price_list.append(old_price)

        i = 0

        for item in item_url_list:
            sleep(0)
            res_new = requests.get(item, headers=headers)
            soup_new = BeautifulSoup(res_new.text, "lxml")
            data = soup_new.find("div", class_="page-subcategory__wrapper")

            id_product = data.find("p", class_="product-page-content__article").text.strip().replace("Артикул: ", "")
            name_product = data.find("h1",
                                     class_="product-page-content__product-name catalog-heading heading__h2").text.strip()
            url_product = item_url_list[i]
            brand = data.find("a", class_="product-attributes__list-item-link reset-link active-blue-text").text.strip()
            actual_price_item = actual_price_list[i]
            old_price_item = old_price_list[i]
            list_product.append(Product(id_product=id_product,
                                        name_product=name_product,
                                        url_product=url_product,
                                        brand=brand,
                                        actual_price_item=actual_price_item,
                                        old_price_item=old_price_item))

            i += 1
        write_csv(list_product)
        page += 1
        print(f"count_items{count_items}")
        print(f"page{page}")


def create_csv():
    with open(f"metro.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "id_product",
            "name_product",
            "url_product",
            "brand",
            "actual_price_item",
            "old_price_item",
        ])


def write_csv(products: list[Product]):
    with open(f"metro.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([
                product.id_product,
                product.name_product,
                product.url_product,
                product.brand,
                product.actual_price_item,
                product.old_price_item,
            ])


if __name__ == "__main__":
    parser(
        url="https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry?from=under_search&order=price_desc&in_stock=1",
        max_item=485)
