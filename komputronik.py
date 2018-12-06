from typing import List
from bs4 import BeautifulSoup
from requester import HtmlRequest
from product import Product

class KomputronikStripper(object):

    def fetch_products(self, search_text : str, req : HtmlRequest) -> List[Product]:
        html_doc = req.request("https://www.komputronik.pl/search/category/1?query=" + search_text)
        soup = BeautifulSoup(html_doc, 'html.parser')

        prods : List[Product] = []

        for link in soup.find_all("li", class_="product-entry2 "):
            atag = link.find("div", class_="pe2-head").find("a")
            idtag = link.find("div", class_="pe2-codes")
            pricetag = link.find("div", class_="ps4-price").find("span")
            url = atag["href"]
            title = atag.string.strip()
            uid = idtag.string.strip()
            price = float(pricetag.string.strip().replace(u"\xa0", "").replace(" ", "").replace(u"zł", ""))

            prod = Product(uid, url, title, price, "Komputronik")
            prods.append(prod)

        return prods