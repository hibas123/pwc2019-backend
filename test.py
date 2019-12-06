from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests
import json 
from tinydb import TinyDB, Query
import time 
import threading
from json import dumps  
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
from thread import start_new_thread

DTFORMAT = "%m/%d/%Y, %H:%M:%S"

db = TinyDB('db.json')




class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("access-control-allow-headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("access-control-allow-origin", "*")
        self.end_headers()
        prices, times = [], []
        for el in db.all()[-72:]:
            prices.append(el['price'])
            times.append(el['time'])
        data = {'price': prices, 'time': times}  # GET DATA FROM DB
        self.wfile.write(dumps(data))

def http_listen():
    httpd = HTTPServer(("", 7767), SimpleHTTPRequestHandler)
    httpd.serve_forever()

thread = threading.Thread(target=http_listen)
thread.start()




def gqlquery(query): 
    resp = requests.post("https://graphql-stock-api.herokuapp.com/graphql", {"query": query})
    assert resp.status_code == 200
    test = json.loads(resp.text)
    # print(json.dumps(test,indent=4, sort_keys=True))
    return test['data']


def cont_gqlquery():
    count = 0
    while(1): 
        print(count)
        tick = gqlquery(query)
        dic = {"price": tick['stock']['Price'], "time": dt.now().strftime(DTFORMAT)}
        db.insert(dic)
        time.sleep(300)
        count +=1


#_transport = RequestsHTTPTransport(
#    url='https://www.graphqlhub.com/graphql',
#    use_json=True,
#)


#client = Client(
#    transport=_transport,
#    fetch_schema_from_transport=True,
#)
#query = """
#{
#  graphQLHub
#  twitter {
#    search(q: "Tesla", count: 2, result_type: recent) {
#      user {
#        screen_name
#      }
#      id
#      text
#      created_at
#    }
#  }
#}

# resp = requests.post("https://grql.stamm.me/graphql", {"query": query})
# print(resp.text, resp.status_code)
# print(json.dumps(gqlquery(query), indent=4, sort_keys=True))
#for el in test['twitter']:
#    db.insert({'text': el, 'count': 7})
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
print(json.dumps(gqlquery(query), indent=4, sort_keys=True))
start_new_thread(cont_gqlquery,())