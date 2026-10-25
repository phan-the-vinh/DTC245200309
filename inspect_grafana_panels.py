import urllib.request
import urllib.parse
import json
import os
import subprocess
import time
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')


GRAFANA_HOST = "192.168.177.128"
GRAFANA_PORT = 3000

print("="*70)
print("KIỂM TRA TRỰC TIẾP GRAFANA VÀ PROMETHEUS (READ-ONLY)")
print("="*70)

# 1. Đăng nhập Grafana
login_url = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/login"
login_payload = json.dumps({"user": "admin", "password": "Grafana_Admin2026!"}).encode("utf-8")
req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    cookies = resp.headers.get_all("Set-Cookie")
cookie_header = "; ".join([c.split(";")[0] for c in cookies])
print(f"[1] Đăng nhập Grafana thành công.")

# 2. Kiểm tra datasources
ds_req = urllib.request.Request(f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/api/datasources", headers={"Cookie": cookie_header})
with urllib.request.urlopen(ds_req) as resp:
    ds_list = json.loads(resp.read().decode("utf-8"))

print("\n[2] DANH SÁCH DATASOURCES TRONG GRAFANA:")
prom_ds = None
for ds in ds_list:
    print(f"  - Name: {ds.get('name'):<15} Type: {ds.get('type'):<12} UID: {ds.get('uid'):<20} URL: {ds.get('url')} (Default: {ds.get('isDefault')})")
    if ds.get('type') == 'prometheus':
        prom_ds = ds

# 3. Tìm kiếm Dashboards trong Grafana
dash_search_req = urllib.request.Request(f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/api/search?type=dash-db", headers={"Cookie": cookie_header})
with urllib.request.urlopen(dash_search_req) as resp:
    dashboards = json.loads(resp.read().decode("utf-8"))

print("\n[3] DANH SÁCH DASHBOARDS TRONG GRAFANA:")
for d in dashboards:
    print(f"  - Title: '{d.get('title')}' | UID: {d.get('uid')} | URL: {d.get('url')}")

# 4. Kiểm tra chi tiết Dashboard System Overview
target_dash = None
for d in dashboards:
    if "overview" in d.get('title', '').lower() or "system" in d.get('title', '').lower():
        target_dash = d
        break
if not target_dash and dashboards:
    target_dash = dashboards[0]

if target_dash:
    dash_uid = target_dash.get('uid')
    dash_detail_req = urllib.request.Request(f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/api/dashboards/uid/{dash_uid}", headers={"Cookie": cookie_header})
    with urllib.request.urlopen(dash_detail_req) as resp:
        dash_detail = json.loads(resp.read().decode("utf-8"))
    
    dash_obj = dash_detail.get('dashboard', {})
    print(f"\n[4] CHI TIẾT DASHBOARD: '{dash_obj.get('title')}' (UID: {dash_uid}):")
    print(f"  - Time Range: from='{dash_obj.get('time', {}).get('from')}', to='{dash_obj.get('time', {}).get('to')}'")
    print(f"  - Refresh: '{dash_obj.get('refresh', 'None')}'")
    
    print("\n  DANH SÁCH CÁC PANEL VÀ TRUY VẤN:")
    for p in dash_obj.get('panels', []):
        p_id = p.get('id')
        p_title = p.get('title')
        p_type = p.get('type')
        targets = p.get('targets', [])
        print(f"\n  Panel ID: {p_id} | Title: '{p_title}' | Type: {p_type}")
        for t in targets:
            print(f"    - RefId: {t.get('refId')}")
            print(f"    - Expr: {t.get('expr')}")
            print(f"    - Legend: {t.get('legendFormat')}")
            print(f"    - Datasource: {t.get('datasource')}")

# 5. Truy vấn PromQL trực tiếp trên Prometheus
print("\n[5] TRUY VẤN THỬ CÁC BIỂU THỨC PROMQL TRỰC TIẾP TRÊN PROMETHEUS:")
def test_promql(title, expr):
    url = "http://192.168.177.128:9090/api/v1/query?" + urllib.parse.urlencode({"query": expr})
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            res = json.loads(r.read().decode())['data']['result']
            print(f"\n--- {title} ---")
            print(f"  Expr: {expr}")
            print(f"  Số chuỗi dữ liệu (series count): {len(res)}")
            for item in res:
                metric_name = item['metric'].get('name', item['metric'].get('instance', 'unknown'))
                val = item['value'][1]
                print(f"    Container: {metric_name:<20} => Giá trị: {val}")
    except Exception as e:
        print(f"  Lỗi truy vấn '{expr}': {e}")

# 6. Kiểm tra trực tiếp qua Grafana Backend Query API (/api/ds/query)
print("\n[6] KIỂM TRA TRỰC TIẾP QUA GRAFANA BACKEND QUERY API (/api/ds/query):")
def test_grafana_api_query(name, expr):
    query_url = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/api/ds/query"
    payload = {
        "queries": [
            {
                "refId": "A",
                "datasource": {"type": "prometheus", "uid": prom_ds.get('uid')},
                "expr": expr,
                "instant": False,
                "range": True
            }
        ],
        "from": "now-15m",
        "to": "now"
    }
    req = urllib.request.Request(query_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Cookie": cookie_header})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            frames = data.get('results', {}).get('A', {}).get('frames', [])
            print(f"\n--- Grafana Query API: {name} ---")
            print(f"  Expr: {expr}")
            print(f"  Số frames dữ liệu trả về: {len(frames)}")
            for f in frames:
                labels = f.get('schema', {}).get('fields', [{}])[-1].get('labels', {})
                values_field = f.get('data', {}).get('values', [[], []])
                last_val = values_field[1][-1] if len(values_field) > 1 and values_field[1] else "None"
                print(f"    Container: {labels.get('name', 'N/A'):<20} | Điểm dữ liệu cuối: {last_val}")
    except Exception as e:
        print(f"  Lỗi Grafana Query API cho '{name}': {e}")

test_grafana_api_query("Panel 5: Container CPU Usage (%)", 'sum(rate(container_cpu_usage_seconds_total{name=~"news_.*"}[1m])) by (name) * 100')
test_grafana_api_query("Panel 6: Container Memory Usage", 'container_memory_usage_bytes{name=~"news_.*"}')

