from pymongo import MongoClient

mdb = {
    "host": '172.24.132.208',
    # "host": '51facai.51vip.biz',
    "user": 'data',
    "password": 'data123',
    "db": 'invest',
    "port": '16538',
    "fcoin": 'fcoin'
}

mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
coll = sdb[mdb["fcoin"]]

