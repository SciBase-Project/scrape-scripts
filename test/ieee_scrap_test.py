from src import ieee_scrap

ieee_scrap.store_article("400")
ieee_scrap.store_article("1000")
ieee_scrap.store_article("5000")
ieee_scrap.store_article("10000")
ieee_scrap.store_article("50000")

print "\nInserted articles"
print "\nPrinting articles"

import pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.scibase

articles = db.ieee.find()
for article in articles :
    print article
    print "\n\n"


