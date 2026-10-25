import sys
import json
import os
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

audit_results = {}

def run_step(step_name, cmd, sudo=False):
    print(f"[*] Running: {step_name}...")
    code, out, err = run_command(cmd, sudo=sudo)
    audit_results[step_name] = {
        "command": cmd,
        "exit_code": code,
        "output": out,
        "error": err
    }

# 1. Docker & Resources
run_step("docker_compose_config_valid", "cd /home/ubuntu/trienkhaihethong && docker compose config --quiet && echo 'CONFIG_SYNTAX_VALID'")
run_step("docker_compose_services", "cd /home/ubuntu/trienkhaihethong && docker compose config --services")
run_step("docker_compose_volumes", "cd /home/ubuntu/trienkhaihethong && docker compose config --volumes")
run_step("docker_compose_ps", "cd /home/ubuntu/trienkhaihethong && docker compose ps -a")
run_step("disk_space", "df -h / /var/lib/docker")
run_step("docker_inspect_health", "docker inspect --format '{{.Name}}: Status={{.State.Status}} Health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' $(docker ps -aq)")
run_step("docker_networks", "docker network ls")
run_step("docker_network_inspect_frontend", "docker network inspect trienkhaihethong_news_frontend_net --format '{{range .Containers}}{{.Name}} ({{.IPv4Address}}) {{end}}'")
run_step("docker_network_inspect_backend", "docker network inspect trienkhaihethong_news_backend_net --format '{{range .Containers}}{{.Name}} ({{.IPv4Address}}) {{end}}'")
run_step("docker_network_inspect_monitoring", "docker network inspect trienkhaihethong_news_monitoring_net --format '{{range .Containers}}{{.Name}} ({{.IPv4Address}}) {{end}}'")
run_step("docker_volumes", "docker volume ls")

# 2. Security
run_step("listening_ports", "ss -tulpn | grep -E ':(80|443|3000|3100|3306|8080|8081|9090|9100|9080)'")
run_step("container_user", "docker inspect --format '{{.Name}}: User=\"{{.Config.User}}\"' $(docker ps -q)")
run_step("container_privileges", "docker inspect --format '{{.Name}}: Privileged={{.HostConfig.Privileged}}, CapAdd={{.HostConfig.CapAdd}}, CapDrop={{.HostConfig.CapDrop}}, SecurityOpt={{.HostConfig.SecurityOpt}}' $(docker ps -q)")
run_step("docker_socket_mounts", "docker inspect --format '{{.Name}}: {{range .Mounts}}{{if eq .Destination \"/var/run/docker.sock\"}}{{.Source}} RW={{.RW}}{{end}}{{end}}' $(docker ps -q)")
run_step("file_permissions", "ls -la /home/ubuntu/trienkhaihethong/.env /home/ubuntu/trienkhaihethong/nginx/ssl/ /home/ubuntu/trienkhaihethong/docker-compose.yml")
run_step("curl_http_redirect", "curl -s -I http://localhost/")
run_step("curl_https_headers", "curl -k -s -I https://localhost/")
run_step("test_endpoints_nginx", "curl -k -s -o /dev/null -w 'error500=%{http_code}\n' https://localhost/error500; curl -k -s -o /dev/null -w 'error502=%{http_code}\n' https://localhost/error502; curl -k -s -o /dev/null -w 'error_test_php=%{http_code}\n' https://localhost/error_test.php")

# 3. Monitoring & Logging
run_step("prometheus_targets_api", "curl -s http://localhost:9090/api/v1/targets | jq '{activeTargets: [.data.activeTargets[] | {job: .labels.job, instance: .labels.instance, health: .health, lastError: .lastError}]}'")
run_step("prometheus_promql_up", "curl -s 'http://localhost:9090/api/v1/query?query=up' | jq '.data.result[] | {metric: .metric, value: .value}'")
run_step("grafana_datasources_api", "curl -s -u admin:Grafana_Admin2026! http://localhost:3000/api/datasources | jq '[.[] | {name: .name, type: .type, url: .url, isDefault: .isDefault}]'")
run_step("grafana_dashboards_api", "curl -s -u admin:Grafana_Admin2026! http://localhost:3000/api/search | jq '[.[] | {title: .title, type: .type, url: .url}]'")
run_step("loki_ready_api", "curl -s -i http://localhost:3100/ready")
run_step("loki_labels_api", "curl -s http://localhost:3100/loki/api/v1/labels | jq .")
run_step("loki_query_1", "curl -s -G -H 'Accept: application/json' --data-urlencode 'query={job=\"nginx\"}' --data-urlencode 'limit=2' http://localhost:3100/loki/api/v1/query_range | jq '{status: .status, resultCount: (.data.result | length)}'")
run_step("loki_query_2", "curl -s -G -H 'Accept: application/json' --data-urlencode 'query={job=\"nginx\"} |~ \"HTTP/[0-9.]+\\\" 5[0-9][0-9]\"' --data-urlencode 'limit=2' http://localhost:3100/loki/api/v1/query_range | jq '{status: .status, resultCount: (.data.result | length)}'")
run_step("loki_query_3", "curl -s -G -H 'Accept: application/json' --data-urlencode 'query={job=\"webapp\"} |~ \"(?i)(error|exception|failed)\"' --data-urlencode 'limit=2' http://localhost:3100/loki/api/v1/query_range | jq '{status: .status, resultCount: (.data.result | length)}'")

# 4. Git
run_step("git_status", "cd /home/ubuntu/trienkhaihethong && git status")
run_step("git_log", "cd /home/ubuntu/trienkhaihethong && git log --oneline --graph")
run_step("git_remotes", "cd /home/ubuntu/trienkhaihethong && git remote -v")
run_step("git_tracked_files", "cd /home/ubuntu/trienkhaihethong && git ls-files")
run_step("git_history_check_secrets", "cd /home/ubuntu/trienkhaihethong && git log -p | grep -E '(\.env|BEGIN RSA PRIVATE KEY|PASSWORD|password|SECRET)' | grep -v 'E_ALL' | grep -v 'MYSQL_ROOT_PASSWORD=' | head -n 20")

# Save output to audit_raw.json
with open('d:/trienkhaihethong/audit_raw.json', 'w', encoding='utf-8') as f:
    json.dump(audit_results, f, ensure_ascii=False, indent=2)

print("\n[OK] Raw audit data collected in d:/trienkhaihethong/audit_raw.json")
