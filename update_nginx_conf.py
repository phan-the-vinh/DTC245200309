import remote_exec
import os
import difflib

print("="*60)
print("CẬP NHẬT NGINX DEFAULT.CONF TRÊN UBUNTU")
print("="*60)

# 1. Sao lưu file trên Ubuntu
bak_cmd = "cp -p /home/ubuntu/trienkhaihethong/nginx/conf.d/default.conf /home/ubuntu/trienkhaihethong/nginx/conf.d/default.conf.bak_healthz"
code, out, err = remote_exec.run_command(bak_cmd)
print("Tạo backup trên Ubuntu:", "OK" if code == 0 else f"Lỗi: {err}")

# 2. Upload file mới từ Windows lên Ubuntu
local_path = r"d:\trienkhaihethong\nginx\conf.d\default.conf"
remote_path = "/home/ubuntu/trienkhaihethong/nginx/conf.d/default.conf"
remote_exec.upload_file(local_path, remote_path)
print("Upload file thành công.")

# 3. Kiểm tra diff trên Ubuntu
print("\n[DIFF TRÊN UBUNTU]:")
code, out, err = remote_exec.run_command("diff -u /home/ubuntu/trienkhaihethong/nginx/conf.d/default.conf.bak_healthz /home/ubuntu/trienkhaihethong/nginx/conf.d/default.conf")
print(out)

# 4. Kiểm tra cú pháp: docker compose exec nginx nginx -t
print("\n[KIỂM TRA CÚ PHÁP: docker compose exec nginx nginx -t]:")
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose exec nginx nginx -t")
print(out)
if err:
    print(err)

# 5. Kiểm tra hiện trạng 3 endpoint (trước khi reload)
print("\n[KIỂM TRA 3 ENDPOINT HIỆN TẠI (TRƯỚC KHI RELOAD)]:")
code, out, err = remote_exec.run_command('curl -k -sS -o /dev/null -w "HTTP %{http_code}\n" https://127.0.0.1/healthz && curl -k -sS -o /dev/null -w "HTTP %{http_code}\n" https://127.0.0.1/ && curl -k -sS -o /dev/null -w "HTTP %{http_code}\n" https://127.0.0.1/pma/')
print(out)


