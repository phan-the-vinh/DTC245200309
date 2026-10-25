import requests
import json
import time

GRAFANA_URL = "http://192.168.177.128:3000"
AUTH = ("admin", "admin")
LOKI_UID = "P8E80F9AEF21F6940"

def query_grafana_explore(expr):
    now_ms = int(time.time() * 1000)
    from_ms = now_ms - (30 * 60 * 1000) # 30 mins
    
    payload = {
        "queries": [
            {
                "refId": "A",
                "expr": expr,
                "datasource": {
                    "type": "loki",
                    "uid": LOKI_UID
                },
                "queryType": "range"
            }
        ],
        "from": str(from_ms),
        "to": str(now_ms)
    }
    
    res = requests.post(f"{GRAFANA_URL}/api/ds/query", auth=AUTH, json=payload)
    print(f"Status for query '{expr}':", res.status_code)
    try:
        data = res.json()
        frames = data.get("results", {}).get("A", {}).get("frames", [])
        print(f"Number of frames: {len(frames)}")
        for f in frames:
            schema = f.get("schema", {})
            data_values = f.get("data", {}).get("values", [])
            print("  Frame fields:", [field.get("name") for field in schema.get("fields", [])])
            if len(data_values) >= 2:
                times = data_values[0]
                lines = data_values[1]
                print(f"  Lines returned ({len(lines)}):")
                for t, l in zip(times[-3:], lines[-3:]):
                    print(f"    [{t}] {l}")
    except Exception as e:
        print("Error parsing response:", e)

print("--- Testing WordPress in Grafana ---")
query_grafana_explore('{container="news_wordpress"} |= "TEST_PIPE_WORDPRESS"')

print("\n--- Testing MySQL in Grafana ---")
query_grafana_explore('{container="news_mysql"} |= "TEST_ERROR"')
