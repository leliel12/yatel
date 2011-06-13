
import string

import sqlobject


DBS = {
    "memory": string.Template("sqlite:///:memory:"),
    "sqlite": string.Template("sqlite:/$name"),
    "mysql": string.Template("mysql://$user:$password@$host:$port/$name")
}


class W(object):
    
    def delete(self):
        super(self.__class__, self).delete(self.id)

class Network(W, sqlobject.SQLObject):
    
    nwid = sqlobject.StringCol(length=5000)
    name = sqlobject.StringCol()    



def connect(db, name="", user="", password="", host="", port=""):
    conn_str = DBS[db].substitute(name=name, user=user, 
                                  password=password, host=host, port=port)
    conn = sqlobject.connectionForURI(conn_str)
    sqlobject.sqlhub.processConnection = conn
    Network.createTable(ifNotExists=True)


        
connect("sqlite", "//home/juan/ej.sqlite")


