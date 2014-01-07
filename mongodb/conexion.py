from pymongo import MongoClient

cnx = None
base = None

def conecta():
    global cnx, base
    #cnx =  MongoClient('mongodb://xmn:Mongolab!1@ds049467.mongolab.com:49467/xmn')
    cnx =  MongoClient('mongodb://admin:V5e2Ir_KTNcf@127.3.69.129:27017/open')

    base = cnx['open']
    assert len(base.collection_names()) >= 2
    return

if __name__ == '__main__':
    conecta()
