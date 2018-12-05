import requests

class HtmlRequest(object):

    def request(self, addr : str) -> str:
        return requests.get(addr).text