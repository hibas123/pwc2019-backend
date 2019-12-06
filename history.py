import requests
import json
from tinydb import TinyDB, Query
import time
import threading
from json import dumps
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt

DTFORMAT = "%m/%d/%Y, %H:%M:%S"

db = TinyDB('./data/db.json')

query = """
{
  stock(Symbol: "TSLA") {
    Symbol
    CompanyName
    Price
    Diff
  }
}
"""


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("access-control-allow-headers",
                         "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("access-control-allow-origin", "*")
        self.end_headers()
        prices, times = [], []
        for el in db.all()[-72:]:
            prices.append(el['price'])
            times.append(el['time'])
        data = {'price': prices, 'time': times}  # GET DATA FROM DB
        self.wfile.write(bytes(dumps(data), "utf-8"))


def http_listen():
    httpd = HTTPServer(("", 7767), SimpleHTTPRequestHandler)
    httpd.serve_forever()


def gqlquery(query):
    resp = requests.post(
        "https://graphql-stock-api.herokuapp.com/graphql", {"query": query})
    assert resp.status_code == 200
    test = json.loads(resp.text)
    return test['data']


def cont_gqlquery():
    count = 0
    while(1):
        print(count)
        tick = gqlquery(query)
        dic = {"price": tick['stock']['Price'],
               "time": dt.now().strftime(DTFORMAT)}
        db.insert(dic)
        time.sleep(300)
        count += 1


def main():
    thread = threading.Thread(target=http_listen)
    thread.start()
    cont_gqlquery()
