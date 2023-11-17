# Проект
__Парсер для сайта METRO по категории "Сыры".__
## Описание
```
* Парсит по категории Сыр: 
    https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry?from=under_search&order=price_desc&in_stock=1.
* В категории 485 товаров на 23 страницах.
* Данные, которые забирает парсер:
-id товара;
-наименование;
-ссылка на товар;
-новая цена;
-старая цена;
-бренд.
* Парсер создает csv-файл и собирает информацию в него.
* Файл с массивом данных называется "metro.csv".
```
## Используемый стек
```
beautifulsoup4==4.12.2
lxml==4.9.3
requests==2.31.0
```
