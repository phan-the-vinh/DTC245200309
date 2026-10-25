import sys
import json
import base64
import urllib.request

def test_prometheus():
    print("--- 1. PROMETHEUS TARGETS ---")
    try:
        req = urllib.request.urlopen("http://192.168.177.128:9090/api/v1/targets", timeout=5)
        data = json.loads(req.read().decode('utf-8'))
        targets = data.get("data", {}).get("activeTargets", [])
        for t in targets:
            job = t.get("labels", {}).get("job")
            health = t.get("health")
            endpoint = t.get("scrapeUrl")
            print(f"Target [{job}]: {health.upper()} -> {endpoint}")
    except Exception as e:
        print(f"Prometheus error: {e}")

def test_grafana():
    print("\n--- 2. GRAFANA DATASOURCES & DASHBOARDS ---")
    try:
        auth_str = base64.b64encode(b"admin:Grafana_Admin2026!").decode('ascii')
        headers = {"Authorization": f"Basic {auth_str}"}
        
        # Datasources
        req = urllib.request.Request("http://192.168.177.128:3000/api/datasources", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            datasources = json.loads(resp.read().decode('utf-8'))
            for ds in datasources:
                print(f"Datasource: {ds.get('name')} (type: {ds.get('type')}, default: {ds.get('isDefault')})")
            
        # Dashboards
        req = urllib.request.Request("http://192.168.177.128:3000/api/search", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            dashboards = json.loads(resp.read().decode('utf-8'))
            for dash in dashboards:
                print(f"Dashboard: {dash.get('title')} (folder: {dash.get('folderTitle')}, url: {dash.get('url')})")
    except Exception as e:
        print(f"Grafana error: {e}")

if __name__ == "__main__":
    test_prometheus()
    test_grafana()
