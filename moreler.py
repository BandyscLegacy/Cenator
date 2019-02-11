from typing import List
from bs4 import BeautifulSoup
from requester import HtmlRequest
from product import Product

class MoreleStripper(object):

    def prepare_discounts(self, req : HtmlRequest):
        html_doc = req.request("https://www.morele.net/alarmcenowy/")
        soup = BeautifulSoup(html_doc, 'html.parser')

        discounts = {}

        for discount in soup.find_all("div", class_="owl-item"):
            link_tag = discount.find("a", class_="link-top")
            key = link_tag['href']
            
            if not 'morele' in key:
                continue

            price_tag = discount.find("div", class_="product-slider-price")
            prices = price_tag.find_all("span")
            price = None
            for price_t in prices:
                if price_t.has_attr('class') and 'price-old' in price_t['class']:
                    continue
                price = float(price_t.string.replace(",", ".").replace("zł", "").replace(" ", "").strip())
            
            discounts[key] = price
        return discounts

    def fetch_products(self, search_text : str, req : HtmlRequest) -> List[Product]:
        discounts = self.prepare_discounts(req)

        html_doc = req.request("https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,,,,,/1/?q=" + search_text)
        soup = BeautifulSoup(html_doc, 'html.parser')

        prods : List[Product] = []

        for link in soup.find_all("div", class_="cat-product"):
            uid = link["data-product-id"]
            a = link.find("a", class_="cat-product-image")
            pricetag = link.find("div", class_="price-new")
            url = "https://www.morele.net" + a['href']
            title = a['title']
            price = float(pricetag.string.strip().replace(" ", "").replace(",", ".").replace(u"zł", ""))
            discount = False
            if url in discounts:
                price = discounts[url]
                discount = True

            prod = Product(uid, url, title, price, "Morele", discount)
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