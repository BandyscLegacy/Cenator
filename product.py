class Product(object):
    def __init__(self, unique_id = None, url = None, name = None, price = None, source = None):
        self.Id : str = unique_id
        self.Name : str = name
        self.Url : str = url
        self.Price : float = price
        self.Source : str = source