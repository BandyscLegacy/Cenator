from typing import List
from bs4 import BeautifulSoup
from requester import HtmlRequest
from product import Product

class MoreleStripper(object):

    def fetch_products(self, search_text : str, req : HtmlRequest) -> List[Product]:
        html_doc = req.request("https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,,,,,/1/?q=" + search_text)
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

        if len(prods) == 0:
            el = soup.find("section", class_="product-grid")
            if el != None:
                linkTag = el.find("div", class_="fb-like")
                titleTag = el.find("h1", class_="prod-name")
                uidTag = el
                priceTag = el.find("div", id="product_price_brutto")

                uid = uidTag["data-product-id"]
                url = "https://www.morele.net" + linkTag['data-href']
                title = titleTag.string.strip()
                price = float(priceTag['content'])

                prod = Product(uid, url, title, price, "Morele")
                prods.append(prod)


        return prods