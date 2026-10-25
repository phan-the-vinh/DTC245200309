import urllib.request
import urllib.parse
import json

PROM_URL = "http://192.168.177.128:9090"

def query_prom(promql):
    url = f"{PROM_URL}/api/v1/query?query=" + urllib.parse.quote(promql)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data['status'] == 'success':
                return data['data']['result']
            else:
                return f"Error: {data}"
    except Exception as e:
        return f"Request failed: {e}"

print("=== 1. CHECK CADVISOR TARGET STATUS ===")
targets_url = f"{PROM_URL}/api/v1/targets"
with urllib.request.urlopen(targets_url) as resp:
    t_data = json.loads(resp.read().decode('utf-8'))
    for t in t_data['data']['activeTargets']:
        if t['labels'].get('job') == 'cadvisor':
            print("cAdvisor Target:", t['labels'], "Health:", t['health'], "LastError:", t['lastError'])

print("\n=== 2. QUERY container_cpu_usage_seconds_total SAMPLES ===")
cpu_samples = query_prom('container_cpu_usage_seconds_total[1m]')
if isinstance(cpu_samples, list):
    print(f"Total series for container_cpu_usage_seconds_total: {len(cpu_samples)}")
    for s in cpu_samples[:5]:
        print("Metric labels:", s['metric'])
else:
    print(cpu_samples)

print("\n=== 3. QUERY container_memory_working_set_bytes SAMPLES ===")
mem_samples = query_prom('container_memory_working_set_bytes')
if isinstance(mem_samples, list):
    print(f"Total series for container_memory_working_set_bytes: {len(mem_samples)}")
    for s in mem_samples[:5]:
        print("Metric labels:", s['metric'])
else:
    print(mem_samples)

print("\n=== 4. CHECK SPECIFIC CONTAINER NAMES IN LABELS ===")
name_check = query_prom('container_cpu_usage_seconds_total{name=~".+"}')
if isinstance(name_check, list):
    print(f"Series with label 'name': {len(name_check)}")
    names = set(s['metric'].get('name') for s in name_check)
    print("Distinct 'name' values:", sorted(list(names)))

container_name_check = query_prom('container_cpu_usage_seconds_total{container_name=~".+"}')
if isinstance(container_name_check, list):
    print(f"Series with label 'container_name': {len(container_name_check)}")
    c_names = set(s['metric'].get('container_name') for s in container_name_check)
    print("Distinct 'container_name' values:", sorted(list(c_names)))
