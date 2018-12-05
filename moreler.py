from typing import List
from bs4 import BeautifulSoup
from requester import HtmlRequest
from product import Product

class MoreleStripper(object):

    def fetch_products(self, search_text : str, req : HtmlRequest) -> List[Product]:
        html_doc = req.request("https://www.morele.net/komputery/podzespoly-komputerowe/karty-graficzne-12/?q=" + search_text)
        soup = BeautifulSoup(html_doc, 'html.parser')

        prods : List[Product] = []

        for link in soup.find_all("div", class_="cat-product"):
            uid = link["data-product-id"]
            a = link.find("a", class_="cat-product-image")
            pricetag = link.find("div", class_="price-new")
            url = "https://www.morele.net" + a['href']
            title = a['title']
            price = float(pricetag.string.strip().replace(" ", "").replace(u"zł", ""))

            prod = Product(uid, url, title, price, "Morele")
            prods.append(prod)

        return prods