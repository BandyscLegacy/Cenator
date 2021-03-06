from typing import List, Dict

class Product(object):
    def __init__(self, unique_id = None, url = None, name = None, price = None, source = None, discoutPrice = False):
        self.Id : str = unique_id
        self.Name : str = name
        self.Url : str = url
        self.Price : float = price
        self.Source : str = source
        self.History : List[Dict] = []
        self.DiscountPrice : bool = discoutPrice