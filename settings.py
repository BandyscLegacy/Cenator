import json
import os

class Settings(object):

    def __init__(self, settings_path):
        self.__failed = False
        if not os.path.exists(settings_path):
            self.data = {}
            self.__failed = True
        else:
            self.data = json.load(open(settings_path))

        self.__ensure("tag", "2080 ti")
        self.__ensure("min_price", 3000)
        self.__ensure("max_price", 7000)
        self.__ensure("discount_to_notify", 12)
        self.__ensure("notify_below", 5100)
        self.__ensure("max_sms_once", 3)
        self.__ensure("exclude", "", False)

        if self.__failed:
            print("Some settings in " + settings_path + " are not filled. Fix to use this app")
            json.dump(self.data, open(settings_path, "w"), indent=4)
            exit(0)

    def __ensure(self, key, default, require = True):
        if not key in self.data:
            if require:
                self.__failed = True
            self.data[key] = default

    @property
    def search_tag(self):
        return self.data['tag']

    @property
    def min_price(self):
        return self.data['min_price']

    @property
    def max_price(self):
        return self.data['max_price']

    @property
    def discount_to_notify(self):
        return self.data['discount_to_notify']

    @property
    def exclude(self):
        return self.data['exclude']

    @property
    def notify_below(self):
        return self.data['notify_below']
        
    @property
    def max_sms_once(self):
        return self.data['max_sms_once']
        