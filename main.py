from typing import List, Dict, Optional
from moreler import MoreleStripper
from xkomer import XKomStripper
from komputronik import KomputronikStripper
from requester import HtmlRequest
from database import Database
from sms import SMS
from product import Product
from settings import Settings
import os
import sys
import time

requester = HtmlRequest()
moreler = MoreleStripper()
xkomer = XKomStripper()
komp = KomputronikStripper()

database = Database()

settings = Settings()

def should_send_sms():
    return len(sys.argv) > 1 and sys.argv[1] == "sms"

if should_send_sms():
    if not 'SMS_SECRET' in os.environ:
        print("No SMS_SECRET for Twilio in environment variables")
        exit(0)
    if not 'SMS_AUTH' in os.environ:
        print("No SMS_SECRET for Twilio in environment variables")
        exit(0)
    if not 'PHONE_NUMBER' in os.environ:
        print("No PHONE_NUMBER for Twilio in environment variables")
        exit(0)
    if not 'SRC_PHONE_NUMBER' in os.environ:
        print("No SRC_PHONE_NUMBER for Twilio in environment variables")
        exit(0)

    sms = SMS(os.environ['SMS_SECRET'], os.environ['SMS_AUTH'])

sms_count = 0
def send_sms(msg):
    global sms_count
    global settings
    if should_send_sms() and sms_count < settings.max_sms_once:
        sms.send(os.environ['SRC_PHONE_NUMBER'], os.environ['PHONE_NUMBER'], msg)
        sms_count += 1

prods = moreler.fetch_products(settings.search_tag, requester)
prods += xkomer.fetch_products(settings.search_tag, requester)
prods += komp.fetch_products(settings.search_tag, requester)

old_prods : List[Product] = database.products()

tags = settings.search_tag.lower().split(' ')

for prod in prods:

    all=True
    for tag in tags:
        if not tag in prod.Name.lower():
            all=False
    
    if not all:
        print("Not all tags in " + prod.Name+ ". Ignoring")
    else:
        oldProd : Optional[Product] = database.product(prod.Id)
        if oldProd is None:
            if prod.Price >= settings.min_price and prod.Price <= settings.max_price:
                database.add_product(prod, int(time.time()))
                msg = "NOWY! " + prod.Name + " za " + str(prod.Price) + "zl na " + prod.Source
                if prod.Price <= settings.notify_below:
                    send_sms(msg)
                print(msg)
        else:
            if oldProd.Price > prod.Price:
                discount : float = (oldProd.Price - prod.Price) / oldProd.Price * 100

                msg = "TANIEJ o " + str(int(discount)) + "%: " + prod.Name + " za " + str(prod.Price) + "(" + str(oldProd.Price) + ") na " + prod.Source"
                if prod.Price <= settings.notify_below or discount >= settings.discount_to_notify:
                    send_sms(msg)
                print(msg)
                
                database.add_price(prod, int(time.time()))
            elif oldProd.Price < prod.Price:
                database.add_price(prod, int(time.time()))