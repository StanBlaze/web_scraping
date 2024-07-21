import re
import requests
import hashlib
import json
import sqlite3
from pprint import pprint


def get_content(url):
    # Генерация имени файла на основе хэширования URL
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        # Попытка открыть файл с сохраненным контентом
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print('Контент отримано з файлу')
            return content
    except FileNotFoundError:
        # Если файл не найден, выполняется запрос к веб-странице
        response = requests.get(url)
        if response.status_code == 200:
            # Если запрос успешен, сохраняем контент в файл
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print('Контент отримано з сервера')
            return response.text
        else:
            # В случае ошибки при запросе выводим сообщение об ошибке
            print(f'Не вдалося отримати веб-сторінку. Код статусу: {response.status_code}')
            return None


def extract_job_info(content):
    # Регулярный выражение для поиска названий вакансий и ссылок
    job_info_pattern = re.compile(
        r'<a href="(https://www\.lejobadequat\.com/emplois/[^"]+)"[^>]*title="Consulter l\'offre d\'emploi ([^"]+)"')

    # Поиск всех совпадений в контенте
    job_infos = job_info_pattern.findall(content)

    # Создание списка словарей с названиями вакансий и ссылками
    job_list = [{'title': title, 'link': link} for link, title in job_infos]
    return job_list


def write_json(data):
    # Файл для сохранения данных
    filename = 'job_infos.json'

    # Печать данных для проверки
    pprint(data)

    # Сохранение данных в файл в формате JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'Дані збережено у файл {filename}')


def write_sqlite(data):
    # Имя файла базы данных
    filename = 'jobs.db'

    # Подключение к базе данных и создание курсора
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Создание таблицы, если ее не существует
    sql = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        link TEXT
    )
    """
    cursor.execute(sql)

    # Вставка данных в таблицу
    for entry in data:
        cursor.execute("""
        INSERT INTO jobs (title, link)
        VALUES (?, ?)
        """, (entry['title'], entry['link']))

    # Фиксация изменений и закрытие соединения
    conn.commit()
    conn.close()
    print(f'Дані збережено у базу даних {filename}')


if __name__ == '__main__':
    # URL страницы с вакансиями
    url = 'https://www.lejobadequat.com/emplois'

    # Получение контента страницы
    content = get_content(url)

    if content:
        # Извлечение информации о вакансиях
        job_infos = extract_job_info(content)

        # Вывод названий вакансий и ссылок
        for job in job_infos:
            print(f"Title: {job['title']}, Link: {job['link']}")

        # Сохранение данных в формате JSON
        write_json(job_infos)

        # Сохранение данных в базе данных SQLite
        write_sqlite(job_infos)
