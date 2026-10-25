import remote_exec
import json
import sys

print("="*60)
print("GIAI ĐOẠN 1: TẢI IMAGE CADVISOR MỚI VÀ KIỂM TRA SAU TẢI")
print("="*60)

# BƯỚC 1: Kiểm tra dung lượng đĩa trước khi tải
print("\n[BƯỚC 1] KIỂM TRA DUNG LƯỢNG ĐĨA TRƯỚC KHI TẢI (df -m /):")
code, out, err = remote_exec.run_command("df -m /")
print(out)
lines = [l for l in out.strip().splitlines() if l.startswith('/dev/')]
if lines:
    parts = lines[0].split()
    avail_mb = int(parts[3])
    print(f"Dung lượng trống trước tải: {avail_mb} MB")
    if avail_mb < 2000:
        print(f"LỖI: Dung lượng trống {avail_mb} MB nhỏ hơn ngưỡng an toàn 2.000 MB! DỪNG LẠI.")
        sys.exit(1)
    else:
        print(f"Xác nhận: Dung lượng trống {avail_mb} MB >= 2.000 MB. Đạt điều kiện tiếp tục.")
else:
    print("Không phân tích được đầu ra df -m /!")
    sys.exit(1)

# BƯỚC 2: Xác nhận container news_cadvisor đang chạy và image cũ tồn tại
print("\n[BƯỚC 2] XÁC NHẬN CONTAINER news_cadvisor VÀ IMAGE CŨ:")
code, out, err = remote_exec.run_command("docker inspect news_cadvisor --format 'Container: {{.Name}} | Status: {{.State.Status}} | Image: {{.Config.Image}} | ImageID: {{.Image}}'")
print("Container hiện tại:", out.strip())

code, out, err = remote_exec.run_command("docker inspect gcr.io/cadvisor/cadvisor:v0.49.1 --format 'Image cũ ID: {{.Id}} | Tags: {{json .RepoTags}}'")
print(out.strip())

# BƯỚC 3: Thực hiện docker pull ghcr.io/google/cadvisor:v0.60.6
print("\n[BƯỚC 3] THỰC HIỆN DOCKER PULL ghcr.io/google/cadvisor:v0.60.6:")
code, out, err = remote_exec.run_command("docker pull ghcr.io/google/cadvisor:v0.60.6")
print("Exit code:", code)
print(out)
if code != 0:
    print("LỖI KHI PULL IMAGE:", err)
    sys.exit(code)

# BƯỚC 4: Kiểm tra dung lượng đĩa sau tải và xác nhận image mới
print("\n[BƯỚC 4] KIỂM TRA DUNG LƯỢNG ĐĨA SAU KHI TẢI (df -m /):")
code, out, err = remote_exec.run_command("df -m /")
print(out)
lines_after = [l for l in out.strip().splitlines() if l.startswith('/dev/')]
if lines_after:
    parts_after = lines_after[0].split()
    avail_mb_after = int(parts_after[3])
    print(f"Dung lượng trống sau tải: {avail_mb_after} MB (Chênh lệch: {avail_mb - avail_mb_after} MB)")
    if avail_mb_after < 1500:
        print(f"CẢNH BÁO: Dung lượng trống sau tải {avail_mb_after} MB nhỏ hơn 1.500 MB! DỪNG LẠI CHỜ QUYẾT ĐỊNH.")
    else:
        print(f"Xác nhận: Dung lượng trống {avail_mb_after} MB >= 1.500 MB. An toàn.")

# BƯỚC 5: Chi tiết image mới đã tải thành công
print("\n[BƯỚC 5] THÔNG TIN IMAGE MỚI:")
code, out, err = remote_exec.run_command("docker inspect ghcr.io/google/cadvisor:v0.60.6 --format 'Image ID: {{.Id}}\nSize: {{.Size}} bytes\nRepoTags: {{json .RepoTags}}\nCreated: {{.Created}}'")
print(out)

# BƯỚC 6: Kiểm tra lại container cAdvisor cũ vẫn đang chạy liên tục
print("\n[BƯỚC 6] KIỂM TRA LẠI CONTAINER news_cadvisor HIỆN TẠI:")
code, out, err = remote_exec.run_command("docker inspect news_cadvisor --format 'Status: {{.State.Status}} | Running: {{.State.Running}} | StartedAt: {{.State.StartedAt}}'")
print("Container news_cadvisor:", out.strip())
