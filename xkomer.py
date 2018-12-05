from typing import List
from bs4 import BeautifulSoup
from requester import HtmlRequest
from product import Product

class XKomStripper(object):

    def fetch_products(self, search_text : str, req : HtmlRequest) -> List[Product]:
        html_doc = req.request("https://www.x-kom.pl/szukaj?q=" + search_text + "&per_page=90&f[groups][5]=1&f[categories][346]=1")
        soup = BeautifulSoup(html_doc, 'html.parser')

        prods : List[Product] = []

        for link in soup.find_all("div", class_="product-item"):
            url = "https://www.x-kom.pl/" + link.find("a")['href']
            title = link['data-product-name']
            price = float(link['data-product-price'])

            prod = Product(url, url, title, price, "xkom")
            prods.append(prod)

        return prods