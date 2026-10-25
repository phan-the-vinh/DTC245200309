import remote_exec
import json
import urllib.request
import urllib.parse
import sys

print("="*70)
print("KIỂM TRA TOÀN DIỆN HỆ THỐNG VÀ 10 DỊCH VỤ (READ-ONLY)")
print("="*70)

# 1. Chạy docker compose ps
print("\n[1] TRẠNG THÁI CONTAINER (docker compose ps):")
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose ps")
print(out)

# 2. Kiểm tra chi tiết 10 dịch vụ từ bên trong máy ảo Ubuntu
print("\n[2] KIỂM TRA CHỨC NĂNG 10 DỊCH VỤ TẠI MÁY ẢO:")

services_check = [
    ("WordPress (HTTPS)", "curl -k -s -o /dev/null -w '%{http_code}' https://127.0.0.1/", "200"),
    ("phpMyAdmin (HTTPS)", "curl -k -s -o /dev/null -w '%{http_code}' https://127.0.0.1/pma/", "200"),
    ("Nginx Healthz (HTTPS)", "curl -k -s -o /dev/null -w '%{http_code}' https://127.0.0.1/healthz", "200"),
    ("Nginx Status (HTTP)", "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/nginx_status", "200"),
    ("Prometheus (HTTP:9090)", "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9090/-/healthy", "200"),
    ("Grafana Health (HTTP:3000)", "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/api/health", "200"),
    ("Loki (internal 3100)", "docker compose -f /home/ubuntu/trienkhaihethong/docker-compose.yml exec grafana wget -q -O - http://loki:3100/ready", "ready"),
    ("cAdvisor (internal 8080)", "docker compose -f /home/ubuntu/trienkhaihethong/docker-compose.yml exec prometheus wget -q -O - http://cadvisor:8080/healthz", "ok"),
    ("Node Exporter (internal 9100)", "docker compose -f /home/ubuntu/trienkhaihethong/docker-compose.yml exec prometheus wget -q -O - http://node_exporter:9100/metrics | head -n 1", "# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles."),
]

for name, cmd, expected in services_check:
    c, res, e = remote_exec.run_command(cmd)
    res_code = res.strip()
    status = "OK (Đạt)" if expected in res_code else f"FAIL ({res_code})"
    print(f"  - {name:<30}: {status}")


# Kiểm tra riêng MySQL bằng docker inspect health status
c, res, e = remote_exec.run_command("docker inspect news_mysql --format 'Status: {{.State.Status}} | Health: {{.State.Health.Status}}'")
print(f"  - {'MySQL Server':<28}: {res.strip()}")

# Kiểm tra riêng Promtail
c, res, e = remote_exec.run_command("docker inspect news_promtail --format 'Status: {{.State.Status}} | Running: {{.State.Running}}'")
print(f"  - {'Promtail Agent':<28}: {res.strip()}")

# 3. Kiểm tra khả năng truy cập Prometheus UI & Targets
print("\n[3] KIỂM TRA PROMETHEUS TẠI http://127.0.0.1:9090:")
try:
    with urllib.request.urlopen("http://192.168.177.128:9090/-/healthy", timeout=5) as r:
        print(f"  - Prometheus Healthy Endpoint: HTTP {r.status} ({r.read().decode().strip()})")
    
    with urllib.request.urlopen("http://192.168.177.128:9090/api/v1/targets", timeout=5) as r:
        t_data = json.loads(r.read().decode())['data']['activeTargets']
        print(f"  - Prometheus Active Targets ({len(t_data)} targets):")
        for t in t_data:
            print(f"    * Job: {t['labels'].get('job'):<15} Instance: {t['labels'].get('instance'):<20} Health: {t['health']}")
except Exception as ex:
    print(f"  Lỗi truy cập Prometheus: {ex}")

# 4. Kiểm tra khả năng truy cập Grafana UI
print("\n[4] KIỂM TRA GRAFANA TẠI http://127.0.0.1:3000:")
try:
    with urllib.request.urlopen("http://192.168.177.128:3000/api/health", timeout=5) as r:
        health_resp = json.loads(r.read().decode())
        print(f"  - Grafana API Health: HTTP {r.status} | Database: {health_resp.get('database')} | Version: {health_resp.get('version')}")
    
    # Kiểm tra login & datasource
    login_url = "http://192.168.177.128:3000/login"
    login_payload = json.dumps({"user": "admin", "password": "admin"}).encode("utf-8")
    req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        cookies = r.headers.get_all("Set-Cookie")
        cookie_hdr = "; ".join([ck.split(";")[0] for ck in cookies])
        print(f"  - Grafana Login: HTTP {r.status} (Xác thực Admin thành công)")
    
    ds_req = urllib.request.Request("http://192.168.177.128:3000/api/datasources", headers={"Cookie": cookie_hdr})
    with urllib.request.urlopen(ds_req, timeout=5) as r:
        ds_list = json.loads(r.read().decode())
        print(f"  - Grafana Datasources ({len(ds_list)} datasources):")
        for ds in ds_list:
            print(f"    * Name: {ds.get('name'):<12} Type: {ds.get('type'):<12} URL: {ds.get('url')}")
except Exception as ex:
    print(f"  Lỗi truy cập Grafana: {ex}")

print("\n" + "="*70)
print("HOÀN TẤT KIỂM TRA TOÀN DIỆN")
print("="*70)
