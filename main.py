from typing import List, Dict, Optional
from moreler import MoreleStripper
from xkomer import XKomStripper
from komputronik import KomputronikStripper
from proline import ProlineStripper
from requester import HtmlRequest
from database import Database
from sms import SMS
from product import Product
from settings import Settings
import os
import sys
import time
import argparse

requester = HtmlRequest()
moreler = MoreleStripper()
xkomer = XKomStripper()
komp = KomputronikStripper()
proline = ProlineStripper()

parser = argparse.ArgumentParser(description='Read prices from xkom, morele, komputronik!')
parser.add_argument('-d', '--database', dest='database_path', action='store', default="database.json")
parser.add_argument('-s', '--settings', dest='settings_path', action='store', default="settings.json")
parser.add_argument('--sms', dest='sms', action='store_true', default=False)
parser.add_argument('-v', dest='verbose', action='store_true', default=False)

args = parser.parse_args()

database = Database(args.database_path)

settings = Settings(args.settings_path)

def should_send_sms():
    global args
    return args.sms

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
prods += proline.fetch_products(settings.search_tag, requester)

old_prods : List[Product] = database.products()

tags = settings.search_tag.lower().split(' ')
exclude_tags = settings.exclude.lower().split(' ')

if args.verbose:
    print("Tags: " + str(tags))
    print("Exclude tags: " + str(exclude_tags))

for prod in prods:

    all=True
    for tag in tags:
        if len(tag) > 0 and not tag in prod.Name.lower():
            all=False
    
    noneWrong=True
    for tag in exclude_tags:
        if len(tag) > 0 and tag in prod.Name.lower():
            noneWrong = False

    if not all:
        if args.verbose:
            print("Not all tags in " + prod.Name+ ". Ignoring")
    elif not noneWrong:
        if args.verbose:
            print("Invalid tags in " + prod.Name + ". Ignoring")
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

                msg = "TANIEJ o " + str(int(discount)) + "%: " + prod.Name + " za " + str(prod.Price) + "(" + str(oldProd.Price) + ") na " + prod.Source
                if prod.Price <= settings.notify_below or discount >= settings.discount_to_notify:
                    send_sms(msg)
                print(msg)
                
                database.add_price(prod, int(time.time()))
            elif oldProd.Price < prod.Price:
                database.add_price(prod, int(time.time()))