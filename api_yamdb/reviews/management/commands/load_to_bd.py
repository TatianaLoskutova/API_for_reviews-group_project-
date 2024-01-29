import csv

from django.core.management import BaseCommand
from django.db import IntegrityError
from django.conf import settings

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)
from users.models import CustomUser

TABLES = {
    CustomUser: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', CustomUser),
    'review_id': ('review', Review),
}


def open_csv_file(file_name):
    csv_path = f'{settings.BASE_DIR}/static/data/{file_name}'
    try:
        with open(csv_path, encoding='utf-8') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        print(f'Файл {file_name} не найден.')


def change_foreign_values(data_csv):
    data_csv_copy = data_csv.copy()
    for key, value in data_csv.items():
        if key in FIELDS.keys():
            field_key = FIELDS[key][0]
            data_csv_copy[field_key] = FIELDS[key][1].objects.get(
                pk=value)
    return data_csv_copy


def load_csv(model, file_name):
    """Осуществляет загрузку csv-файлов."""
    table_not_loaded = f'Таблица {file_name} не загружена.'
    table_loaded = f'Таблица {file_name} загружена.'
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = model(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            print(f'Ошибка в загружаемых данных. {error}. '
                  f'{table_not_loaded}')
            break
    print(table_loaded)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for molel, csv_file in TABLES.items():
            load_csv(molel, csv_file)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
