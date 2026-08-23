import requests

url = "https://api.semanticscholar.org/graph/v1/paper/search"

params = {
    "query": "deep learning",
    "limit": 1,
    "fields": "title"
}

response = requests.get(
    url,
    params=params,
    timeout=30
)

print(response.status_code)
print(response.text[:500])