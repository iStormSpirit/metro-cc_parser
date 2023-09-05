import json
import logging
import os

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def folder_checker():
    dir_path = os.path.abspath(os.curdir)
    if not os.path.exists('data'):
        os.mkdir('data')
    return f'{dir_path}/data'


def make_file_path(document):
    file_path = os.path.join(folder_checker(), document)
    return file_path


def save_result(response, document):
    file_path = make_file_path(document)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
    except Exception as ex:
        print(f'{logging.exception(ex)} Error save in py_log.log')


def open_json(document):
    file_path = make_file_path(document)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            products_data = json.load(file)['data']['category']['products']
            return products_data
    except Exception as ex:
        print(f'{logging.exception(ex)} Error save in py_log.log')
