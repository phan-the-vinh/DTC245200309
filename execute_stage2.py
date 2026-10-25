import remote_exec
import json
import time
import sys
import urllib.request
import urllib.parse

print("="*70)
print("GIAI ĐOẠN 2: CẬP NHẬT CẤU HÌNH VÀ TÁI TẠO RIÊNG CONTAINER CADVISOR")
print("="*70)

# ==============================================================================
# BƯỚC A: KIỂM TRA TRƯỚC KHI SỬA
# ==============================================================================
print("\n>>> BƯỚC A: KIỂM TRA TRƯỚC KHI SỬA")

# A.1 Xác nhận thư mục làm việc trên Ubuntu
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && pwd")
work_dir = out.strip()
print(f"1. Thư mục làm việc: {work_dir}")
if work_dir != "/home/ubuntu/trienkhaihethong":
    print(f"LỖI: Thư mục làm việc không phải /home/ubuntu/trienkhaihethong! Dừng.")
    sys.exit(1)

# A.2 Kiểm tra dung lượng trống (df -m /)
code, out, err = remote_exec.run_command("df -m /")
print("2. Dung lượng đĩa:")
print(out)
lines = [l for l in out.strip().splitlines() if l.startswith('/dev/')]
if lines:
    avail_mb_pre = int(lines[0].split()[3])
    print(f"Dung lượng khả dụng trước triển khai: {avail_mb_pre} MB")
    if avail_mb_pre < 2000:
        print(f"LỖI: Dung lượng khả dụng {avail_mb_pre} MB < 2000 MB! DỪNG.")
        sys.exit(1)
else:
    print("LỖI: Không đọc được dung lượng đĩa! DỪNG.")
    sys.exit(1)

# A.3 Xác nhận container news_cadvisor đang chạy, image cũ tồn tại, image mới tồn tại
print("3. Kiểm tra container news_cadvisor và các images:")
code, out, err = remote_exec.run_command("docker inspect news_cadvisor --format 'Container: {{.Name}} | Status: {{.State.Status}} | ImageID: {{.Image}}'")
print("  Container hiện tại:", out.strip())

code, out, err = remote_exec.run_command("docker inspect gcr.io/cadvisor/cadvisor:v0.49.1 --format 'Image cũ ID: {{.Id}}'")
print("  Image cũ:", out.strip())

code, out, err = remote_exec.run_command("docker inspect ghcr.io/google/cadvisor:v0.60.6 --format 'Image mới ID: {{.Id}}'")
print("  Image mới:", out.strip())

# A.4 Kiểm tra cấu hình Compose hiện tại và xác định chính xác tên service cadvisor
code, out, err = remote_exec.run_command("docker compose -f /home/ubuntu/trienkhaihethong/docker-compose.yml config --services")
services = out.strip().splitlines()
print(f"4. Danh sách services trong Compose: {services}")
if "cadvisor" not in services:
    print("LỖI: Service 'cadvisor' không tìm thấy trong Compose! DỪNG.")
    sys.exit(1)
print("  -> Xác nhận service name chính xác: 'cadvisor'")

# A.5 Tạo bản sao lưu riêng của docker-compose.yml
backup_file = "/home/ubuntu/trienkhaihethong/docker-compose.yml.bak_stage2"
code, out, err = remote_exec.run_command(f"[ -f {backup_file} ] && echo EXISTS || echo NOT_EXISTS")
if "EXISTS" in out:
    backup_file = f"/home/ubuntu/trienkhaihethong/docker-compose.yml.bak_stage2_{int(time.time())}"
print(f"5. Tạo bản sao lưu: {backup_file}")
code, out, err = remote_exec.run_command(f"cp -p /home/ubuntu/trienkhaihethong/docker-compose.yml {backup_file}")
if code != 0:
    print(f"LỖI: Không tạo được sao lưu! DỪNG: {err}")
    sys.exit(1)
code, out, err = remote_exec.run_command(f"ls -l {backup_file}")
print("  Bản sao lưu đã tạo:", out.strip())

# A.6 Ghi nhận baseline: container status và Prometheus targets
print("6. Baseline trạng thái trước triển khai:")
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose ps")
print("--- docker compose ps (Baseline) ---")
print(out)

baseline_targets = "N/A"
try:
    with urllib.request.urlopen("http://192.168.177.128:9090/api/v1/targets", timeout=5) as r:
        t_json = json.loads(r.read().decode())['data']['activeTargets']
        print("--- Prometheus Targets (Baseline) ---")
        for t in t_json:
            print(f"  Job: {t['labels'].get('job'):<15} Health: {t['health']}")
except Exception as e:
    print(f"Lỗi lấy baseline targets: {e}")

# ==============================================================================
# BƯỚC B: THAY ĐỔI TỐI THIỂU TRÊN UBUNTU
# ==============================================================================
print("\n>>> BƯỚC B: THAY ĐỔI TỐI THIỂU TRÊN UBUNTU")
print("1. Chỉ sửa dòng image của service cadvisor trong /home/ubuntu/trienkhaihethong/docker-compose.yml")
# Dùng sed an toàn thay thế chính xác dòng gcr.io/cadvisor/cadvisor:v0.49.1 thành ghcr.io/google/cadvisor:v0.60.6
cmd_sed = "sed -i 's|image: gcr.io/cadvisor/cadvisor:v0.49.1|image: ghcr.io/google/cadvisor:v0.60.6|' /home/ubuntu/trienkhaihethong/docker-compose.yml"
code, out, err = remote_exec.run_command(cmd_sed)
if code != 0:
    print(f"LỖI khi chạy sed: {err}")
    sys.exit(1)

# Kiểm tra diff chính xác giữa backup và file đã sửa
print("2. Diff chính xác giữa backup và docker-compose.yml:")
code, out, err = remote_exec.run_command(f"diff -u {backup_file} /home/ubuntu/trienkhaihethong/docker-compose.yml")
print(out)

# 3. Kiểm tra cú pháp và cấu hình Compose bằng docker compose config
print("3. Kiểm tra tính hợp lệ bằng docker compose config:")
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose config > /dev/null")
if code != 0:
    print(f"LỖI: docker compose config không hợp lệ! DỪNG: {err}")
    # Phục hồi ngay
    remote_exec.run_command(f"cp -f {backup_file} /home/ubuntu/trienkhaihethong/docker-compose.yml")
    sys.exit(1)
print("  Xác nhận: docker compose config cú pháp hoàn toàn hợp lệ.")

# 4. Xác nhận file Windows giữ nguyên
print("4. Xác nhận file Windows D:\\trienkhaihethong\\docker-compose.yml giữ nguyên:")
with open("d:/trienkhaihethong/docker-compose.yml", "r", encoding="utf-8") as f:
    for line in f:
        if "cadvisor" in line and "image:" in line:
            print("  Windows docker-compose.yml line:", line.strip())

# ==============================================================================
# BƯỚC C: TÁI TẠO RIÊNG CADVISOR
# ==============================================================================
print("\n>>> BƯỚC C: TÁI TẠO RIÊNG CADVISOR")

# C.1 Kiểm tra dung lượng đĩa trước khi up
code, out, err = remote_exec.run_command("df -m /")
avail_mb_deploy = int([l for l in out.strip().splitlines() if l.startswith('/dev/')][0].split()[3])
print(f"1. Dung lượng đĩa ngay trước khi tái tạo: {avail_mb_deploy} MB")
if avail_mb_deploy < 2000:
    print("LỖI: Dung lượng đĩa < 2000 MB! DỪNG.")
    sys.exit(1)

# C.2 Chạy docker compose up -d --no-deps cadvisor
print("2. Thực thi: docker compose up -d --no-deps cadvisor")
t_start = time.time()
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose up -d --no-deps cadvisor")
t_duration = time.time() - t_start
print(f"  Thời gian thực thi lệnh: {t_duration:.2f} giây")
print("  Exit code:", code)
print("  Output:", out)
if code != 0:
    print(f"LỖI khi tái tạo cadvisor: {err}")
    print("DỪNG ĐỂ BÁO CÁO THEO YÊU CẦU.")
    sys.exit(1)

# C.3 Kiểm tra trạng thái container và image thực tế
print("3. Kiểm tra trạng thái container news_cadvisor sau khi tái tạo:")
code, out, err = remote_exec.run_command("docker inspect news_cadvisor --format 'Status: {{.State.Status}} | Image: {{.Config.Image}} | ImageID: {{.Image}} | StartedAt: {{.State.StartedAt}}'")
print("  news_cadvisor:", out.strip())

# C.4 Kiểm tra log khởi động của cAdvisor
print("4. Nhật ký khởi động của news_cadvisor (docker logs news_cadvisor --tail 30):")
time.sleep(3) # Cho container khởi động 3 giây
code, out, err = remote_exec.run_command("docker logs news_cadvisor --tail 30")
print(out)

# C.5 Chờ Prometheus scrape cycle (khoảng 15-20 giây)
print("5. Chờ 15 giây để cAdvisor thu thập và Prometheus hoàn tất chu kỳ scrape...")
time.sleep(15)

# C.6 Kiểm tra Prometheus target cadvisor:8080
print("6. Kiểm tra Prometheus target cadvisor:8080:")
try:
    with urllib.request.urlopen("http://192.168.177.128:9090/api/v1/targets", timeout=10) as r:
        t_json = json.loads(r.read().decode())['data']['activeTargets']
        for t in t_json:
            if t['labels'].get('job') == 'cadvisor':
                print(f"  Target: {t['labels'].get('instance')} | Health: {t['health']} | LastScrape: {t.get('lastScrape')} | LastError: '{t.get('lastError')}'")
except Exception as e:
    print(f"Lỗi kiểm tra target: {e}")

# ==============================================================================
# BƯỚC D: XÁC MINH METRIC TRÊN PROMETHEUS
# ==============================================================================
print("\n>>> BƯỚC D: XÁC MINH METRIC TRÊN PROMETHEUS")

def query_prometheus(promql):
    url = "http://192.168.177.128:9090/api/v1/query?" + urllib.parse.urlencode({"query": promql})
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())['data']['result']
    except Exception as e:
        return f"Error: {e}"

# D.1 container_cpu_usage_seconds_total
print("1. Kiểm tra container_cpu_usage_seconds_total:")
res_cpu_all = query_prometheus("container_cpu_usage_seconds_total")
if isinstance(res_cpu_all, list):
    print(f"  Tổng số chuỗi thời gian: {len(res_cpu_all)}")
    all_labels = set()
    for s in res_cpu_all:
        all_labels.update(s['metric'].keys())
    print(f"  Các nhãn xuất hiện: {sorted(list(all_labels))}")
    
    # Kiểm tra nhãn 'name'
    names = set(s['metric'].get('name') for s in res_cpu_all if 'name' in s['metric'])
    print(f"  Các giá trị nhãn 'name' ({len(names)}): {sorted(list(names))}")
    
    # Kiểm tra nhãn 'container_name' hoặc 'image' hoặc 'id'
    c_names = set(s['metric'].get('container_name') for s in res_cpu_all if 'container_name' in s['metric'])
    if c_names:
        print(f"  Các giá trị nhãn 'container_name': {sorted(list(c_names))}")
    
    # Mẫu 3 series có name hoặc container
    filtered = [s for s in res_cpu_all if s['metric'].get('name') or s['metric'].get('container_name')]
    if filtered:
        print(f"  Mẫu series có định danh container:")
        for s in filtered[:5]:
            print(f"    Name: {s['metric'].get('name')}, Labels: {s['metric']}, Value: {s['value']}")
    else:
        print("  CẢNH BÁO: Chưa thấy series có nhãn 'name' hay 'container_name'. Kiểm tra các id:")
        for s in res_cpu_all[:5]:
            print(f"    ID: {s['metric'].get('id')}")

# D.2 container_memory_usage_bytes
print("\n2. Kiểm tra container_memory_usage_bytes:")
res_mem_usage = query_prometheus("container_memory_usage_bytes")
if isinstance(res_mem_usage, list):
    print(f"  Tổng số chuỗi thời gian: {len(res_mem_usage)}")
    names_mem = set(s['metric'].get('name') for s in res_mem_usage if 'name' in s['metric'])
    print(f"  Các giá trị nhãn 'name' ({len(names_mem)}): {sorted(list(names_mem))}")
    filtered_mem = [s for s in res_mem_usage if s['metric'].get('name') or s['metric'].get('container_name')]
    for s in filtered_mem[:5]:
        print(f"    Name: {s['metric'].get('name')}, Value: {s['value']}")

# D.3 container_memory_working_set_bytes
print("\n3. Kiểm tra container_memory_working_set_bytes:")
res_mem_wss = query_prometheus("container_memory_working_set_bytes")
if isinstance(res_mem_wss, list):
    print(f"  Tổng số chuỗi thời gian: {len(res_mem_wss)}")
    names_wss = set(s['metric'].get('name') for s in res_mem_wss if 'name' in s['metric'])
    print(f"  Các giá trị nhãn 'name' ({len(names_wss)}): {sorted(list(names_wss))}")

# D.4 Kiểm tra trạng thái của toàn bộ 10 container
print("\n4. Trạng thái toàn bộ các container sau triển khai (docker compose ps):")
code, out, err = remote_exec.run_command("cd /home/ubuntu/trienkhaihethong && docker compose ps")
print(out)

# D.5 Kiểm tra dung lượng đĩa sau cùng
print("\n5. Dung lượng đĩa sau khi hoàn thành Giai đoạn 2 (df -m /):")
code, out, err = remote_exec.run_command("df -m /")
print(out)
lines_final = [l for l in out.strip().splitlines() if l.startswith('/dev/')]
if lines_final:
    avail_mb_final = int(lines_final[0].split()[3])
    print(f"  Dung lượng trống sau cùng: {avail_mb_final} MB (Chênh lệch so với trước: {avail_mb_pre - avail_mb_final} MB)")
    if avail_mb_final < 1500:
        print("  CẢNH BÁO NGUY CƠ: Dung lượng trống < 1500 MB!")
    else:
        print("  Xác nhận: Dung lượng an toàn (> 1500 MB).")

print("\n" + "="*70)
print("HOÀN TẤT GIAI ĐOẠN 2 - DỪNG CHỜ PHÊ DUYỆT")
print("="*70)
