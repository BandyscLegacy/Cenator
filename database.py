from typing import List, Dict, Optional
from product import Product
from datetime import datetime
import json
import os

from product import Product

def decode_object(o):
    if '__Product__' in o:
        a = Product() 
        a.__dict__.update(o['__Product__'])
        return a
    elif '__datetime__' in o:
        return datetime.strptime(o['__datetime__'], '%Y-%m-%dT%H:%M:%S')        
 
    return o

class CustomEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime):
             return {'__datetime__': o.replace(microsecond=0).isoformat()}
         return {'__{}__'.format(o.__class__.__name__): o.__dict__}

class Database(object):
    def __init__(self):
        if not os.path.exists('../database.json'):
            self.data = {}
        else:
            self.data = json.load(open("../database.json"), object_hook=decode_object)

        if not 'products' in self.data:
            self.data['products'] = {}
    
    def product(self, uid : str) -> Optional[Product]:
        if not uid in self.__products():
            return None
        return self.__products()[uid]

    def products(self) -> Dict[str, Product]:
        return dict(self.__products())

    def add_price(self, prod : Product, timestamp: int):
        self.__products()[prod.Id].Price = prod.Price
        self.__products()[prod.Id].History.append({"time": timestamp, "price": prod.Price})
        self.save()

    def __products(self) -> Dict[str, Product]:
        return self.data['products']

    def add_product(self, product : Product, timestamp: int):
        if not 'products' in self.data:
            self.data['products'] = {}
        
        self.data['products'][product.Id] = product
        self.data['products'][product.Id].History.append({"time": timestamp, "price": product.Price})

        self.save()

    def save(self):
        with open('../database.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=True, cls=CustomEncoder)