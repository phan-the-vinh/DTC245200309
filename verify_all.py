import sys
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

print("=== 1. DOCKER COMPOSE PS ===")
code, out, _ = run_command("cd /home/ubuntu/trienkhaihethong; docker compose ps")
print(out)

print("=== 2. HTTP TO HTTPS REDIRECT ===")
code, out, _ = run_command("curl -s -I http://localhost/ | head -n 5")
print(out)

print("=== 3. HTTPS NGINX + SECURITY HEADERS ===")
code, out, _ = run_command("curl -k -s -I https://localhost/ | head -n 12")
print(out)

print("=== 4. PHPMYADMIN VIA NGINX ===")
code, out, _ = run_command("curl -k -s -I https://localhost/pma/ | head -n 5")
print(out)

print("=== 5. PROMETHEUS TARGETS STATUS ===")
code, out, _ = run_command("curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health, lastScrape: .lastScrape}'")
print(out)

print("=== 6. GRAFANA LOGIN STATUS ===")
code, out, _ = run_command("curl -s -I http://localhost:3000/login | head -n 5")
print(out)

print("=== 7. LOKI STATUS ===")
code, out, _ = run_command("curl -s http://localhost:3100/ready")
print(out)

print("=== 8. GIT REPOSITORY STATUS ===")
code, out, _ = run_command("cd /home/ubuntu/trienkhaihethong; git status -s")
print(out if out.strip() else "Working tree clean!")
