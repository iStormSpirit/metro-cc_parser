import logging

import requests
from processing_json import open_json, save_result

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def save_result_json(document_for_preresult, document):
    """Достаем нужные для нас данные
       из json файла и сохраняем в файл с результатами."""
    products_data = open_json(document_for_preresult)

    if len(products_data) != 0:
        data = {}
        for item in products_data:
            product_id = item.get('id')
            product_name = item.get('name')
            product_url = 'https://online.metro-cc.ru' + item.get('url')
            product_manufacturer = item.get('manufacturer').get('name')
            product_price = item.get('stocks')[0].get('prices_per_unit').get('old_price')
            # если основная цена равна null, то скидки на товар нет
            # и его регулярная цена равна цене в данный момент
            if product_price is None:
                product_price = item.get('stocks')[0].get('prices_per_unit').get('offline')['price']
                product_price_discount = None
            else:
                product_price_discount = item.get('stocks')[0].get('prices_per_unit').get('offline')['price']

            data[product_name] = {
                'product_id': product_id,
                'url': product_url,
                'manufacturer': product_manufacturer,
                'price': product_price,
                'price_discount': product_price_discount
            }
        save_result(data, document)
    else:
        print(f'{logging.exception(Exception)} Error save in py_log.log')


class ParserMetro:
    """Класс для парсинга сайта https://online.metro-cc.ru/."""

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'authority': 'api.metro-cc.ru',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-AU,ru;q=0.9,en-VI;q=0.8,en;q=0.7,ru-RU;q=0.6,en-US;q=0.5',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

    def scrape_metro_shop_category(self, json_data, document):
        """Получаем количество товара от нужного нам эндпоинта
           и отправляем запрос на получение всех товаров."""
        response = self.session.post('https://api.metro-cc.ru/products-api/graph', headers=self.headers,
                                     json=json_data).json()
        quantity = response.get('data').get('category').get('filters').get('facets')[0].get('total')
        json_data['variables']['size'] = quantity
        response = self.session.post('https://api.metro-cc.ru/products-api/graph', headers=self.headers,
                                     json=json_data).json()
        save_result(response, document)

    def start(self, city, store_id):
        json_data = {
            'query': '\n  query Query($storeId: Int!, $slug: String!, $attributes:[AttributeFilter], $filters: [FieldFilter], $from: Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, $eshop_order: Boolean, $is_action: Boolean, $price_levels: Boolean) {\n    category (storeId: $storeId, slug: $slug, inStock: $in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, priceLevels: $price_levels) {\n      id\n      name\n      slug\n      id\n      parent_id\n      meta {\n        description\n        h1\n        title\n        keywords\n      }\n      disclaimer\n      description {\n        top\n        main\n        bottom\n      }\n#      treeBranch {\n#        id\n#        name\n#        slug\n#        children {\n#          category_type\n#          id\n#          name\n#          slug\n#          children {\n#            category_type\n#            id\n#            name\n#            slug\n#            children {\n#              category_type\n#              id\n#              name\n#              slug\n#              children {\n#                category_type\n#                id\n#                name\n#                slug\n#              }\n#            }\n#          }\n#        }\n#      }\n      breadcrumbs {\n        category_type\n        id\n        name\n        parent_id\n        parent_slug\n        slug\n      }\n      promo_banners {\n        id\n        image\n        name\n        category_ids\n        virtual_ids\n        type\n        sort_order\n        url\n        is_target_blank\n        analytics {\n          name\n          category\n          brand\n          type\n          start_date\n          end_date\n        }\n      }\n\n\n      dynamic_categories(from: 0, size: 9999) {\n        slug\n        name\n        id\n      }\n      filters {\n        facets {\n          key\n          total\n          filter {\n            id\n            name\n            display_title\n            is_list\n            is_main\n            text_filter\n            is_range\n            category_id\n            category_name\n            values {\n              slug\n              text\n              total\n            }\n          }\n        }\n      }\n      total\n      prices {\n        max\n        min\n      }\n      pricesFiltered {\n        max\n        min\n      }\n      products(attributeFilters: $attributes, from: $from, size: $size, sort: $sort, fieldFilters: $filters)  {\n        health_warning\n        limited_sale_qty\n        id\n        slug\n        name\n        name_highlight\n        article\n        is_target\n        category_id\n        url\n        images\n        pick_up\n        icons {\n          id\n          badge_bg_colors\n          caption\n          image\n          type\n          is_only_for_sales\n          stores\n          caption_settings {\n            colors\n            text\n          }\n          stores\n          sort\n          image_png\n          image_svg\n          description\n          end_date\n          start_date\n          status\n        }\n        manufacturer {\n          id\n          image\n          name\n        }\n        packing {\n          size\n          type\n          pack_factors {\n            instamart\n          }\n        }\n        stocks {\n          value\n          text\n          eshop_availability\n          scale\n          prices_per_unit {\n            old_price\n            offline {\n              price\n              old_price\n              type\n              offline_discount\n              offline_promo\n            }\n            price\n            is_promo\n            levels {\n              count\n              price\n            }\n            discount\n          }\n          prices {\n            price\n            is_promo\n            old_price\n            offline {\n              old_price\n              price\n              type\n              offline_discount\n              offline_promo\n            }\n            levels {\n              count\n              price\n            }\n            discount\n          }\n        }\n      }\n    }\n  }\n',
            'variables': {
                'isShouldFetchOnlyProducts': True,
                'slug': 'chipsy-suhari-sneki',
                # при смене здесь слага можно получить данные о товарах из других категорий
                'storeId': None,
                'sort': 'default',
                'size': 0,
                'from': 0,
                'filters': [],
                'attributes': [],
                'in_stock': True,
                'eshop_order': False,
            },
        }
        json_data['variables']['storeId'] = store_id
        document_for_pre_result = 'pre_result_for_' + city + '.json'
        self.scrape_metro_shop_category(json_data, document_for_pre_result)
        document_for_result = 'result_for_' + city + '.json'
        try:
            save_result_json(document_for_pre_result, document_for_result)
            print(f'Сохранение произошло успешно в файл: {document_for_result}')
        except Exception as ex:
            print(f'{logging.exception(ex)} Error save in py_log.log')


if __name__ == '__main__':
    parser = ParserMetro()
    cities = {
        'Moscow': 10,
        'SPb': 15
    }
    for key, value in cities.items():
        parser.start(city=key, store_id=value)
