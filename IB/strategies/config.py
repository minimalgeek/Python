from pymongo import MongoClient

mongo = {
    'host': 'localhost',
    'port': 27017,
    'db': 'python_import'
}

client = MongoClient(host=mongo['host'], port=mongo['port'])
db = client.get_database(mongo['db'])