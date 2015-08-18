import urllib2
import time
import json
from pymongo import MongoClient

api = 'https://api.bitfinex.com/v1'
symbol = 'ltcusd'
limit = 25
book_url = '{0}/book/{1}?limit_bids={2}&limit_asks={2}'.format(api,
                                                               symbol, limit)

client = MongoClient()
db = client['bitmicro']
ltc_books = db['ltc_books']


def get_json(url):
    resp = urllib2.urlopen(url)
    return json.load(resp), resp.getcode()

while True:
    start = time.time()

    book, code = get_json(book_url)
    if code != 200:
        print code
    else:
        book['_id'] = time.time()
        ltc_books.insert_one(book)

    time_delta = time.time()-start
    print time_delta
    # if time_delta < 1.0:
    #     time.sleep(1-time_delta)
