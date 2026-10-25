import sys
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING ALL GIT COMMITS FOR SECRETS ===")
code, out, _ = run_command("cd /home/ubuntu/trienkhaihethong && git --no-pager log -p")

# Search for sensitive keywords in git history
sensitive_keywords = ["MYSQL_ROOT_PASSWORD", "MYSQL_PASSWORD", "GRAFANA_ADMIN_PASSWORD", "BEGIN RSA PRIVATE KEY", "BEGIN PRIVATE KEY"]
found = []
for line in out.splitlines():
    if line.startswith("+") and not line.startswith("+++"):
        for kw in sensitive_keywords:
            if kw in line:
                found.append(line)

print(f"Total sensitive lines found in git diffs: {len(found)}")
for f in found:
    # Mask actual value for security
    print("  * " + f[:30] + "... [MASKED]")
