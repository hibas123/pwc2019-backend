from gql import gql, Client
import requests
from gql.transport.requests import RequestsHTTPTransport
_transport = RequestsHTTPTransport(
    url='http://grql.stamm.me',
    use_json=True,
)

#test = requests.post("http://grql.stamm.me/graphql")
#print(test.status_code)
#print(test.text)
client = Client(
    transport=_transport,
    fetch_schema_from_transport=False,
)
query = gql("""

{
  graphQLHub
  twitter {
    tweet(id: "687433440774459392") {
      text,
      retweets(limit: 2) {
        id,
        retweeted_status {
          id
        }
        user {
          screen_name
        }
      }
    }
  }
}
""")

print(client.execute(query))
