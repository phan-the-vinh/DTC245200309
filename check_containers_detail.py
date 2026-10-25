import sys
import json
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

containers = "news_nginx news_wordpress news_mysql news_phpmyadmin news_prometheus news_node_exporter news_cadvisor news_grafana news_loki news_promtail"

print("=== 1. CONTAINER USERS & PRIVILEGES ===")
cmd = f'docker inspect -f "{{{{.Name}}}}: User=\'{{{{.Config.User}}}}\' Privileged={{{{.HostConfig.Privileged}}}} SecOpt={{{{.HostConfig.SecurityOpt}}}} CapAdd={{{{.HostConfig.CapAdd}}}} CapDrop={{{{.HostConfig.CapDrop}}}}" {containers}'
code, out, _ = run_command(cmd)
print(out)

print("\n=== 2. CONTAINER MOUNTS (DOCKER SOCKET CHECK) ===")
cmd = f'docker inspect -f "{{{{.Name}}}}: {{{{range .Mounts}}}}{{{{.Type}}}}:{{{{.Source}}}}->{{{{.Destination}}}}(rw={{{{.RW}}}}) {{{{end}}}}" {containers}'
code, out, _ = run_command(cmd)
print(out)

print("\n=== 3. NETWORK MEMBERS ===")
for net in ["news_frontend_net", "news_backend_net", "news_monitoring_net"]:
    cmd = f'docker network inspect {net} -f "{{{{.Name}}}}: {{{{range $id, $c := .Containers}}}}{{{{$c.Name}}}} ({{{{$c.IPv4Address}}}}) {{{{end}}}}"'
    code, out, _ = run_command(cmd)
    print(out)

print("\n=== 4. RUNNING PROCESSES (USER INSIDE CONTAINER) ===")
for c in containers.split():
    cmd = f'docker top {c} -eo user,pid,comm 2>/dev/null | head -n 3'
    code, out, _ = run_command(cmd)
    print(f"[{c}]:\n{out.strip()}")
