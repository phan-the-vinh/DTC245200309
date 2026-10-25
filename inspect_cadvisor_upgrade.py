import remote_exec
import json

print("="*60)
print("KIỂM TRA DUNG LƯỢNG Ổ ĐĨA, IMAGES VÀ CADVISOR CONFIG")
print("="*60)

# 1. Dung lượng ổ đĩa
print("\n[1] DUNG LƯỢNG Ổ ĐĨA (df -h /):")
code, out, err = remote_exec.run_command("df -h /")
print(out)

# 2. Images hiện có
print("\n[2] DOCKER IMAGES HIỆN CÓ (docker images):")
code, out, err = remote_exec.run_command("docker images")
print(out)

# 3. Cấu hình cAdvisor trong docker-compose.yml
print("\n[3] CẤU HÌNH CADVISOR TRONG docker-compose.yml:")
code, out, err = remote_exec.run_command("sed -n '114,130p' /home/ubuntu/trienkhaihethong/docker-compose.yml")
print(out)

# 4. Mount thực tế của container news_cadvisor đang chạy
print("\n[4] MOUNT THỰC TẾ CỦA news_cadvisor ĐANG CHẠY (docker inspect):")
code, out, err = remote_exec.run_command("docker inspect news_cadvisor --format '{{json .Mounts}}'")
try:
    mounts = json.loads(out)
    for m in mounts:
        print(f"  - Source: {m.get('Source')} -> Dest: {m.get('Destination')} (RW: {m.get('RW')}, Mode: {m.get('Mode')})")
except Exception as e:
    print(f"Error parsing mounts: {e}, raw: {out}")

# 5. Privileged và Devices của news_cadvisor
print("\n[5] HOST CONFIG (Privileged, Devices, Network):")
code, out, err = remote_exec.run_command("docker inspect news_cadvisor --format 'Privileged={{.HostConfig.Privileged}}, Devices={{json .HostConfig.Devices}}, NetworkMode={{.HostConfig.NetworkMode}}'")
print(out.strip())

# 7. Chi tiết image cũ gcr.io/cadvisor/cadvisor:v0.49.1
print("\n[7] CHI TIẾT IMAGE CŨ (docker inspect image):")
code, out, err = remote_exec.run_command("docker inspect gcr.io/cadvisor/cadvisor:v0.49.1 --format 'ID: {{.Id}} | Size: {{.Size}} bytes | RepoTags: {{json .RepoTags}}'")
print(out.strip())

