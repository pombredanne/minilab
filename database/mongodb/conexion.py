from pymongo import MongoClient

cnx = None
base = None

def conecta():
    global cnx, base
    cnx =  MongoClient('mongodb://USER:PASSWD@SERVER:PORT/DATABASE')

    base = cnx['open']
    assert len(base.collection_names()) >= 2
    return

if __name__ == '__main__':
    conecta()
