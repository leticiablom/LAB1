from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from config import GITHUB_TOKEN

transport = RequestsHTTPTransport(
    url="https://api.github.com/graphql",      
    headers={"Authorization": f"bearer {GITHUB_TOKEN}"},  
    use_json=True,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
query {
  viewer {
    login
  }
}
""")

response = client.execute(query)
print("Usuário autenticado:", response["viewer"]["login"])
