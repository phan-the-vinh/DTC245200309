import requests
import json

GRAFANA_URL = "http://192.168.177.128:3000"
AUTH = ("admin", "admin")

r = requests.get(f"{GRAFANA_URL}/api/datasources", auth=AUTH)
print("Datasources Status:", r.status_code)
ds_list = r.json()
for ds in ds_list:
    print(f"Name: {ds.get('name')}, Type: {ds.get('type')}, UID: {ds.get('uid')}, URL: {ds.get('url')}")
