import remote_exec
import urllib.parse
import json
import time
import datetime

print("="*70)
print("KIỂM TRA CẤU HÌNH VÀ TẠO LOG KIỂM THỬ AN TOÀN")
print("="*70)

# 1. Kiểm tra các labels hiện tại trong Loki qua Promtail
print("\n[1] CÁC NHÃN TRÊN LOKI (qua news_promtail):")
cmd = "docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/labels'"
code, out, err = remote_exec.run_command(cmd)
print("Labels:", out.strip())

cmd = "docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/label/job/values'"
code, out, err = remote_exec.run_command(cmd)
print("Job values:", out.strip())

cmd = "docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/label/container/values'"
code, out, err = remote_exec.run_command(cmd)
print("Container values:", out.strip())

cmd = "docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/label/service/values'"
code, out, err = remote_exec.run_command(cmd)
print("Service values:", out.strip())

# 2. Tạo nội dung log kiểm thử
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
wp_msg = f"[TEST_ERROR] [SIMULATION] [{now_str}] WordPress simulated test log entry for Grafana Explore verification"
mysql_msg = f"[TEST_ERROR] [SIMULATION] [{now_str}] MySQL simulated test log entry for Grafana Explore verification"

print(f"\n[2] NỘI DUNG LOG DỰ KIẾN TẠO LÚC {now_str}:")
print("  - WordPress:", wp_msg)
print("  - MySQL    :", mysql_msg)

# 3. Đưa log vào luồng stderr của container
print("\n[3] GHI LOG VÀO LUỒNG STDERR CỦA CONTAINER:")
cmd_wp = f'docker exec news_wordpress sh -c "echo \\"{wp_msg}\\" > /proc/1/fd/2"'
code_wp, out_wp, err_wp = remote_exec.run_command(cmd_wp)
print("  - Ghi vào news_wordpress: Exit code:", code_wp)

cmd_mysql = f'docker exec news_mysql sh -c "echo \\"{mysql_msg}\\" > /proc/1/fd/2"'
code_mysql, out_mysql, err_mysql = remote_exec.run_command(cmd_mysql)
print("  - Ghi vào news_mysql: Exit code:", code_mysql)

# 4. Kiểm tra docker logs để xác nhận Docker engine đã nhận log
print("\n[4] XÁC NHẬN TRONG DOCKER LOGS:")
code, out, err = remote_exec.run_command("docker logs news_wordpress --tail 3")
print("  Docker logs news_wordpress:")
for l in out.strip().splitlines():
    print("   ", l)

code, out, err = remote_exec.run_command("docker logs news_mysql --tail 3")
print("  Docker logs news_mysql:")
for l in out.strip().splitlines():
    print("   ", l)

# 5. Chờ Promtail scrape và push sang Loki (refresh_interval là 5s)
print("\n[5] CHỜ 7 GIÂY ĐỂ PROMTAIL THU THẬP VÀ ĐẨY SANG LOKI...")
time.sleep(7)

# 6. Truy vấn trên Loki bằng LogQL
print("\n[6] TRUY VẤN LOGQL TRÊN LOKI:")
def query_loki(logql):
    encoded = urllib.parse.quote(logql)
    cmd = f"docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/query?query={encoded}&limit=5'"
    c, res, e = remote_exec.run_command(cmd)
    try:
        data = json.loads(res)
        results = data.get("data", {}).get("result", [])
        print(f"\n  LogQL: {logql}")
        print(f"  Số streams khớp: {len(results)}")
        if not results:
            print("  -> CHƯA TÌM THẤY DÒNG LOG NÀO.")
        for s in results:
            labels = s.get("stream", {})
            values = s.get("values", [])
            print(f"  Stream labels: {labels}")
            for v in values:
                print(f"    [{v[0]}] {v[1].strip()}")
    except Exception as ex:
        print(f"  Lỗi phân tích JSON cho '{logql}': {ex}, Raw: {res}")

query_loki('{container="news_wordpress"} |= "TEST_ERROR"')
query_loki('{job="webapp"} |= "TEST_ERROR"')
query_loki('{container="news_mysql"} |= "TEST_ERROR"')
query_loki('{job="database"} |= "TEST_ERROR"')
