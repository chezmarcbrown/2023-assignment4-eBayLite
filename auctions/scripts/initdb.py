import csv
from auctions.models import User, AuctionListing, Bid, Comment

LISTINGS_FILENAME = "auctions/seeddata/listings.csv"
def run():
    print(f'Opening file: {LISTINGS_FILENAME}')
    with open(LISTINGS_FILENAME) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            print(f'Processing row: {row}')
            category = row['category']
            active = row['active']
            # if not Airport.objects.exists(code=code, city=city):
            #     a=Airport(code=code, city=city)
            #     a.save()
            AuctionListing.objects.get_or_create(category=category, active=active, defaults={'starting_bid': 0})