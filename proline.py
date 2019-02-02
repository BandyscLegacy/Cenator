from typing import List
from bs4 import BeautifulSoup
from requester import HtmlRequest
from product import Product

class ProlineStripper(object):

    def fetch_products(self, search_text : str, req : HtmlRequest) -> List[Product]:
        html_doc = req.request("https://proline.pl/?qp=" + search_text)
        soup = BeautifulSoup(html_doc, 'html.parser')

        prods : List[Product] = []

        for link in soup.find_all("a", class_="produkt pbig"):
            title = link.find("span").string.strip()
            uid = title

            tr = link.parent.parent
            pricetag = tr.find("td", class_="c")
            url = link["href"]
            price = float(pricetag.string.strip().replace(u"\xa0", "").replace(" ", "").replace(u"zł", "").replace(",", "."))

            #print(title + " at " + url + " for " + str(price))

            prod = Product(uid, url, title, price, "Proline")
            prods.append(prod)

        return prods
