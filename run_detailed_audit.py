import sys
import json
import os
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

results = {}

def execute(key, cmd, sudo=False):
    code, out, err = run_command(cmd, sudo=sudo)
    results[key] = {
        "code": code,
        "stdout": out.strip(),
        "stderr": err.strip()
    }
    print(f"[*] {key}: exit {code}")

# 1. Container Users & Processes
execute("container_users", "docker ps --format '{{.Names}}' | while read c; do u=$(docker inspect --format '{{.Config.User}}' \"$c\"); echo \"$c: user='$u'\"; done")
execute("container_top_pids", "docker ps --format '{{.Names}}' | while read c; do echo \"=== $c ===\"; docker top \"$c\" -eo user,pid,comm 2>/dev/null | head -n 5; done")

# 2. Privileges and Capabilities
execute("container_security_opts", "docker ps --format '{{.Names}}' | while read c; do priv=$(docker inspect --format 'Privileged={{.HostConfig.Privileged}}, CapAdd={{.HostConfig.CapAdd}}, CapDrop={{.HostConfig.CapDrop}}, SecurityOpt={{.HostConfig.SecurityOpt}}, ReadonlyRootfs={{.HostConfig.ReadonlyRootfs}}' \"$c\"); echo \"$c: $priv\"; done")

# 3. Mounts & Docker Socket
execute("container_mounts", "docker ps --format '{{.Names}}' | while read c; do echo \"=== $c ===\"; docker inspect --format '{{range .Mounts}}  - {{.Type}}: {{.Source}} -> {{.Destination}} (RW={{.RW}}){{\"\n\"}}{{end}}' \"$c\"; done")

# 4. Network Members
execute("net_frontend_members", "docker network inspect news_frontend_net --format '{{range $id, $c := .Containers}}  - {{$c.Name}}: {{$c.IPv4Address}}{{\"\n\"}}{{end}}'")
execute("net_backend_members", "docker network inspect news_backend_net --format '{{range $id, $c := .Containers}}  - {{$c.Name}}: {{$c.IPv4Address}}{{\"\n\"}}{{end}}'")
execute("net_monitoring_members", "docker network inspect news_monitoring_net --format '{{range $id, $c := .Containers}}  - {{$c.Name}}: {{$c.IPv4Address}}{{\"\n\"}}{{end}}'")

# 5. Loki API via internal network
execute("loki_ready", "docker exec news_grafana wget -qO- http://news_loki:3100/ready")
execute("loki_labels", "docker exec news_grafana wget -qO- http://news_loki:3100/loki/api/v1/labels")
execute("loki_query_1", "docker exec news_grafana wget -qO- 'http://news_loki:3100/loki/api/v1/query_range?query=%7Bjob%3D%22nginx%22%7D&limit=2'")
execute("loki_query_2", "docker exec news_grafana wget -qO- 'http://news_loki:3100/loki/api/v1/query_range?query=%7Bjob%3D%22nginx%22%7D+%7C%7E+%22HTTP%2F%5B0-9.%5D%2B%5C%22+5%5B0-9%5D%5B0-9%5D%22&limit=2'")
execute("loki_query_3", "docker exec news_grafana wget -qO- 'http://news_loki:3100/loki/api/v1/query_range?query=%7Bjob%3D%22webapp%22%7D+%7C%7E+%22%28%3Fi%29%28error%7Cexception%7Cfailed%29%22&limit=2'")

# 6. Test endpoints check
execute("check_test_endpoints_curl", "curl -k -s -I https://localhost/error500 | head -n 4; curl -k -s -I https://localhost/error502 | head -n 4; curl -k -s -I https://localhost/error_test.php | head -n 4")
execute("check_test_file_on_wp", "docker exec news_wordpress ls -la /var/www/html/error_test.php 2>&1")

# 7. Git commits and secrets history check
execute("git_log_full", "cd /home/ubuntu/trienkhaihethong && git log --format='%h - %an - %ad : %s'")
execute("git_secrets_check", "cd /home/ubuntu/trienkhaihethong && git log -p | grep -E '^[+-].*(PASSWORD|password|secret|SECRET|PRIVATE KEY)' | grep -v 'E_ALL' | grep -v 'MYSQL_ROOT_PASSWORD=' | grep -v 'MYSQL_PASSWORD=' | grep -v 'AdminPassword' | head -n 30")

# Save detailed results
with open('d:/trienkhaihethong/audit_detailed_raw.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n[OK] Detailed audit data collected in d:/trienkhaihethong/audit_detailed_raw.json")
