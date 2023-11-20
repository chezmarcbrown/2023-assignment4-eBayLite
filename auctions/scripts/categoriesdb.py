import csv
from auctions.models import Category

CATEGORIES_FILENAME = "auctions/seeddata/categories.csv"
def run():
    print(f'Opening file: {CATEGORIES_FILENAME}')
    with open(CATEGORIES_FILENAME) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            name = row['name']
            Category.objects.get_or_create(name=name)