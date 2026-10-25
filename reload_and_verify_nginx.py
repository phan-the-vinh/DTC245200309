import remote_exec
import sys

print("="*60)
print("RELOAD NGINX VÀ KIỂM TRA 3 ENDPOINTS")
print("="*60)

# 1. Reload Nginx
print("\n[1] THỰC HIỆN: docker compose exec nginx nginx -s reload")
cmd_reload = "cd /home/ubuntu/trienkhaihethong && docker compose exec nginx nginx -s reload"
code, out, err = remote_exec.run_command(cmd_reload)
print("Exit code:", code)
print("Output:", out.strip())
if err:
    print("Stderr:", err.strip())

# 2. Kiểm tra mã phản hồi HTTP của 3 endpoint
print("\n[2] KIỂM TRA HTTP STATUS CODES:")
for ep in ["https://127.0.0.1/healthz", "https://127.0.0.1/", "https://127.0.0.1/pma/"]:
    cmd = f'curl -k -sS -o /dev/null -w "HTTP %{{http_code}}\\n" {ep}'
    code, out, err = remote_exec.run_command(cmd)
    print(f"{ep:<26} => {out.strip()}")


# 3. Kiểm tra chi tiết nội dung phản hồi
print("\n[3] KIỂM TRA CHI TIẾT NỘI DUNG PHẢN HỒI:")

# 3.1 Endpoint /healthz
print("--- Chi tiết /healthz ---")
code, out, err = remote_exec.run_command("curl -k -sS -i https://127.0.0.1/healthz")
print(out.strip())

# 3.2 Endpoint / (WordPress)
print("\n--- Chi tiết / (WordPress) ---")
code, out, err = remote_exec.run_command("curl -k -sS https://127.0.0.1/ | grep -i '<title>'")
print("Title:", out.strip())

# 3.3 Endpoint /pma/ (phpMyAdmin)
print("\n--- Chi tiết /pma/ (phpMyAdmin) ---")
code, out, err = remote_exec.run_command("curl -k -sS https://127.0.0.1/pma/ | grep -i '<title>'")
print("Title:", out.strip())
