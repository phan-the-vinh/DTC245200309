import urllib.request
import urllib.parse
import json
import os
import remote_exec

print("="*60)
print("GIAI ĐOẠN A: KIỂM TRA CHỈ ĐỌC TRƯỚC KHI SỬA")
print("="*60)

# 1. Trạng thái hiện tại của các container bằng docker compose ps
print("\n[1] TRẠNG THÁI HIỆN TẠI CỦA CÁC CONTAINER (docker compose ps):")
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose ps")
print(out)

# 2. Cấu hình cAdvisor và Prometheus hiện có
print("\n[2] CẤU HÌNH CADVISOR VÀ PROMETHEUS HIỆN CÓ TRONG docker-compose.yml:")
code, out, err = remote_exec.run_command("sed -n '110,150p' /home/ubuntu/trienkhaihethong/docker-compose.yml")
print(out)

print("\n[2b] CẤU HÌNH PROMETHEUS SCRAPE JOBS (prometheus.yml):")
code, out, err = remote_exec.run_command("cat /home/ubuntu/trienkhaihethong/prometheus/prometheus.yml")
print(out)

# 3. Tình trạng hoạt động của các target Prometheus
print("\n[3] TÌNH TRẠNG HOẠT ĐỘNG CỦA CÁC TARGET PROMETHEUS:")
try:
    with urllib.request.urlopen("http://192.168.177.128:9090/api/v1/targets") as resp:
        t_data = json.loads(resp.read().decode())['data']
        for t in t_data['activeTargets']:
            print(f"- Job: {t['labels'].get('job'):<15} Instance: {t['labels'].get('instance'):<20} Health: {t['health']:<6} ScrapeUrl: {t['scrapeUrl']}")
except Exception as e:
    print(f"Lỗi lấy targets: {e}")

# 4. Các metric container thực tế mà Prometheus nhận được
print("\n[4] CÁC METRIC CONTAINER THỰC TẾ TRÊN PROMETHEUS:")
def query(q):
    url = "http://192.168.177.128:9090/api/v1/query?query=" + urllib.parse.quote(q)
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())['data']['result']
    except Exception as ex:
        return str(ex)

res_cpu = query("container_cpu_usage_seconds_total")
print(f"- Số lượng time-series container_cpu_usage_seconds_total: {len(res_cpu) if isinstance(res_cpu, list) else res_cpu}")

res_mem = query("container_memory_working_set_bytes")
print(f"- Số lượng time-series container_memory_working_set_bytes: {len(res_mem) if isinstance(res_mem, list) else res_mem}")

# Check all label keys across these metrics
label_keys = set()
if isinstance(res_cpu, list):
    for s in res_cpu:
        label_keys.update(s['metric'].keys())
print(f"- Các nhãn (label keys) xuất hiện trong container_cpu_usage_seconds_total: {sorted(list(label_keys))}")

# Check if any label has docker/container info
name_labeled = query('container_cpu_usage_seconds_total{name!=""}')
print(f"- Số lượng series có nhãn 'name': {len(name_labeled) if isinstance(name_labeled, list) else name_labeled}")

container_name_labeled = query('container_cpu_usage_seconds_total{container_name!=""}')
print(f"- Số lượng series có nhãn 'container_name': {len(container_name_labeled) if isinstance(container_name_labeled, list) else container_name_labeled}")

image_labeled = query('container_cpu_usage_seconds_total{image!=""}')
print(f"- Số lượng series có nhãn 'image': {len(image_labeled) if isinstance(image_labeled, list) else image_labeled}")

# Check sample series
if isinstance(res_cpu, list) and len(res_cpu) > 0:
    print("- Mẫu 3 series đầu tiên của container_cpu_usage_seconds_total:")
    for s in res_cpu[:3]:
        print("  ", s['metric'], "=> Value:", s['value'])

# 5. Truy vấn PromQL hiện tại của hai panel trong system-overview.json
print("\n[5] TRUY VẤN PROMQL HIỆN TẠI CỦA 2 PANEL TRONG grafana/dashboards/system-overview.json:")
dash_path = "D:/trienkhaihethong/grafana/dashboards/system-overview.json"
with open(dash_path, "r", encoding="utf-8") as f:
    dash = json.load(f)

for p in dash.get('panels', []):
    if p.get('id') in [2, 3] or "Container" in p.get('title', ''):
        print(f"\nPanel ID: {p.get('id')}, Title: '{p.get('title')}', Type: {p.get('type')}")
        for t in p.get('targets', []):
            print(f"  RefId: {t.get('refId')}")
            print(f"  Expr: {t.get('expr')}")
            print(f"  Legend: {t.get('legendFormat')}")
            print(f"  Datasource: {t.get('datasource')}")

# 6. Cách dashboard được nạp vào Grafana
print("\n[6] CÁCH DASHBOARD ĐƯỢC NẠP VÀO GRAFANA (provisioning):")
code, out, err = remote_exec.run_command("cat /home/ubuntu/trienkhaihethong/grafana/provisioning/dashboards/dashboard.yml")
print(out)

# 7. Kiểm tra sâu cAdvisor error log
print("\n[7] NGUYÊN NHÂN TẠI SAO CADVISOR KHÔNG CÓ METRIC CỦA DOCKER CONTAINER:")
code, out, err = remote_exec.run_command("docker logs news_cadvisor 2>&1 | grep -i 'failed to create' | head -n 10")
print(out)

# 8. Kiểm tra sâu Docker daemon và storage engine
print("\n[8] CHI TIẾT DOCKER INFO VÀ STORAGE ENGINE:")
code, out, err = remote_exec.run_command("docker info", sudo=True)
for line in out.splitlines():
    if any(k in line.lower() for k in ['driver', 'root dir', 'containerd', 'cgroup', 'server version', 'snapshotter']):
        print("  ", line)

code, out, err = remote_exec.run_command("docker version", sudo=True)
print("\nDocker Version:")
for line in out.splitlines():
    if any(k in line.lower() for k in ['version:', 'api version:', 'os/arch:']):
        print("  ", line)

