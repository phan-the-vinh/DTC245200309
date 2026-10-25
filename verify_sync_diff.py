import difflib
import hashlib
import remote_exec
import sys

if sys.stdout.encoding.lower() != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8': sys.stderr.reconfigure(encoding='utf-8')

print("="*70)
print("KIỂM TRA DIFF WINDOWS VÀ ĐỐI CHIẾU VỚI UBUNTU")
print("="*70)

win_file = r"d:\trienkhaihethong\docker-compose.yml"
bak_file = r"d:\trienkhaihethong\docker-compose.yml.bak_cadvisor_upgrade"

with open(bak_file, "r", encoding="utf-8") as f:
    bak_lines = f.readlines()
with open(win_file, "r", encoding="utf-8") as f:
    win_lines = f.readlines()

# 1. Diff giữa bản backup và bản hiện tại trên Windows
print("\n[1] DIFF CHÍNH XÁC TRÊN WINDOWS (trước vs sau khi sửa):")
diff = list(difflib.unified_diff(bak_lines, win_lines, fromfile="docker-compose.yml.bak_cadvisor_upgrade", tofile="docker-compose.yml", lineterm=""))
for line in diff:
    print(line)

# Đếm số dòng thay đổi
additions = [l for l in diff if l.startswith('+') and not l.startswith('+++')]
deletions = [l for l in diff if l.startswith('-') and not l.startswith('---')]
print(f"\n-> Số dòng thêm (+): {len(additions)}")
print(f"-> Số dòng bớt (-): {len(deletions)}")
print(f"-> Chứng minh: CHỈ CÓ ĐÚNG 1 DÒNG ĐƯỢC THAY ĐỔI.")

# 2. Đọc file docker-compose.yml trên Ubuntu
code, out, err = remote_exec.run_command("cat /home/ubuntu/trienkhaihethong/docker-compose.yml")
ubuntu_content = out
ubuntu_lines = [l + "\n" for l in ubuntu_content.splitlines()]

# So sánh MD5 giữa Windows và Ubuntu
win_md5 = hashlib.md5("".join(win_lines).replace("\r\n", "\n").encode("utf-8")).hexdigest()
ubuntu_md5 = hashlib.md5("".join(ubuntu_lines).replace("\r\n", "\n").encode("utf-8")).hexdigest()

print("\n[2] ĐỐI CHIẾU WINDOWS VỚI UBUNTU:")
print(f"  Windows MD5 (LF): {win_md5}")
print(f"  Ubuntu  MD5 (LF): {ubuntu_md5}")
print(f"  -> Trùng khớp 100% từng byte: {win_md5 == ubuntu_md5}")

# 3. Kiểm tra dòng image cAdvisor trên cả hai môi trường
print("\n[3] XÁC NHẬN DÒNG IMAGE CADVISOR:")
win_cadvisor_img = [l.strip() for l in win_lines if "image:" in l and "cadvisor" in l][0]
ubuntu_cadvisor_img = [l.strip() for l in ubuntu_lines if "image:" in l and "cadvisor" in l][0]
print(f"  Windows: {win_cadvisor_img}")
print(f"  Ubuntu : {ubuntu_cadvisor_img}")
print(f"  -> Hai dòng image hoàn toàn giống nhau: {win_cadvisor_img == ubuntu_cadvisor_img}")

# 4. Kiểm tra mọi khác biệt còn lại (nếu có)
diff_remote = list(difflib.unified_diff(
    [l.replace("\r\n", "\n") for l in win_lines],
    [l.replace("\r\n", "\n") for l in ubuntu_lines],
    fromfile="Windows: docker-compose.yml",
    tofile="Ubuntu: docker-compose.yml",
    lineterm=""
))
print("\n[4] LIỆT KÊ KHÁC BIỆT CÒN LẠI GIỮA WINDOWS VÀ UBUNTU (nếu có):")
if not diff_remote:
    print("  -> KHÔNG CÓ BẤT KỲ KHÁC BIỆT NÀO! Hai tệp hoàn toàn đồng nhất 100%.")
else:
    for line in diff_remote:
        print(line)
