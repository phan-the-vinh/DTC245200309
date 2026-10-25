import remote_exec
import requests
import json
import urllib.parse
import time
import datetime
import os
import subprocess
import threading
import http.server
import socketserver

print("="*75)
print("QUY TRÌNH TẠO VÀ XÁC MINH LOG KIỂM THỬ AN TOÀN TRÊN WORDPRESS & MYSQL")
print("="*75)

# 1. Thời điểm tạo
utc_now = datetime.datetime.now(datetime.timezone.utc)
iso_now = utc_now.strftime("%Y-%m-%dT%H:%M:%S.000000Z")
fmt_now = utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")

wp_log_content = f"[TEST_ERROR] [SIMULATION] [{fmt_now}] WordPress simulated application error log for Grafana Explore verification"
mysql_log_content = f"{iso_now} 0 [ERROR] [MY-000000] [Server] [TEST_ERROR] [SIMULATION] MySQL simulated database error log for Grafana Explore verification"

print(f"\n[BƯỚC 1] THÔNG TIN LOG KIỂM THỬ SẼ TẠO:")
print(f"  Thời điểm UTC: {fmt_now}")
print(f"  - WordPress Log:")
print(f"    {wp_log_content}")
print(f"  - MySQL Log:")
print(f"    {mysql_log_content}")

# 2. Đưa log vào luồng stderr của container một cách an toàn
print(f"\n[BƯỚC 2] THỰC HIỆN ĐƯA LOG VÀO LUỒNG STDERR:")

# 2a. Container news_wordpress: ghi vào fd 2 của PID 1
cmd_wp = f'docker exec news_wordpress sh -c "echo \\"{wp_log_content}\\" > /proc/1/fd/2"'
code_wp, out_wp, err_wp = remote_exec.run_command(cmd_wp)
print(f"  -> news_wordpress injection: Exit code {code_wp}")

# 2b. Container news_mysql: tìm PID trên host và ghi vào fd 2
code_pid, out_pid, err_pid = remote_exec.run_command("docker inspect --format '{{.State.Pid}}' news_mysql")
mysql_host_pid = out_pid.strip()
print(f"  -> news_mysql host PID: {mysql_host_pid}")

cmd_mysql = f'echo "{mysql_log_content}" | sudo tee /proc/{mysql_host_pid}/fd/2'
code_mysql, out_mysql, err_mysql = remote_exec.run_command(cmd_mysql, sudo=True)
print(f"  -> news_mysql injection: Exit code {code_mysql}")

# 3. Kiểm tra docker logs của container
print(f"\n[BƯỚC 3] KIỂM TRA DOCKER LOGS ĐỂ XÁC NHẬN DOCKER ENGINE ĐÃ GHI NHẬN:")
code, out_wplog, err = remote_exec.run_command("docker logs news_wordpress --tail 2")
print("  Docker logs news_wordpress (cuối cùng):")
for line in out_wplog.strip().splitlines():
    print("   ", line)

code, out_mysqllog, err = remote_exec.run_command("docker logs news_mysql --tail 2")
print("  Docker logs news_mysql (cuối cùng):")
for line in out_mysqllog.strip().splitlines():
    print("   ", line)

# 4. Chờ Promtail thu thập và chuyển tiếp tới Loki
print(f"\n[BƯỚC 4] CHỜ 7 GIÂY ĐỂ PROMTAIL SCRAPE & PUSH SANG LOKI...")
time.sleep(7)

# 5. Truy vấn trực tiếp trên Loki API qua container Promtail
print(f"\n[BƯỚC 5] TRUY VẤN LOKI API VỚI LOGQL:")

def query_loki_api(logql):
    encoded = urllib.parse.quote(logql)
    now_ns = int(time.time() * 1e9)
    start_ns = now_ns - int(10 * 60 * 1e9)
    url = f"http://loki:3100/loki/api/v1/query_range?query={encoded}&start={start_ns}&end={now_ns}&limit=5"
    cmd = f"docker exec news_promtail wget -qO- '{url}'"
    c, res, e = remote_exec.run_command(cmd)
    try:
        data = json.loads(res)
        results = data.get("data", {}).get("result", [])
        print(f"  LogQL: {logql}")
        print(f"  Số luồng (stream) khớp: {len(results)}")
        matched_lines = []
        for idx, s in enumerate(results):
            labels = s.get("stream", {})
            values = s.get("values", [])
            print(f"    Stream #{idx+1} labels: {labels}")
            for v in values:
                ts_ns, line_txt = v[0], v[1].strip()
                matched_lines.append((ts_ns, line_txt))
                print(f"      [{ts_ns}] {line_txt}")
        return matched_lines
    except Exception as ex:
        print(f"    Lỗi truy vấn Loki: {ex}")
        return []

print("\n--- Truy vấn log WordPress ---")
wp_results = query_loki_api('{container="news_wordpress"} |= "TEST_ERROR"')
wp_results_job = query_loki_api('{job="webapp"} |= "TEST_ERROR"')

print("\n--- Truy vấn log MySQL ---")
mysql_results = query_loki_api('{container="news_mysql"} |= "TEST_ERROR"')
mysql_results_job = query_loki_api('{job="database"} |= "TEST_ERROR"')

# 6. Kiểm tra qua Grafana Explore API
print(f"\n[BƯỚC 6] KIỂM TRA TRUY VẤN QUA GRAFANA API (DATASOURCE LOKI):")
GRAFANA_URL = "http://192.168.177.128:3000"
AUTH = ("admin", "admin")
LOKI_UID = "P8E80F9AEF21F6940"

def query_grafana_api(expr):
    now_ms = int(time.time() * 1000)
    from_ms = now_ms - (10 * 60 * 1000)
    payload = {
        "queries": [
            {
                "refId": "A",
                "expr": expr,
                "datasource": {"type": "loki", "uid": LOKI_UID},
                "queryType": "range"
            }
        ],
        "from": str(from_ms),
        "to": str(now_ms)
    }
    r = requests.post(f"{GRAFANA_URL}/api/ds/query", auth=AUTH, json=payload, timeout=10)
    if r.status_code == 200:
        data = r.json()
        frames = data.get("results", {}).get("A", {}).get("frames", [])
        print(f"  Grafana API Query '{expr}': HTTP 200 OK, Số frame: {len(frames)}")
        for f in frames:
            vals = f.get("data", {}).get("values", [])
            if len(vals) >= 2:
                print(f"    Số dòng log trả về qua Grafana: {len(vals[1])}")
                for l in vals[1]:
                    print(f"      -> {l}")
    else:
        print(f"  Grafana API Query '{expr}' FAILED: HTTP {r.status_code}")

query_grafana_api('{container="news_wordpress"} |= "TEST_ERROR"')
query_grafana_api('{container="news_mysql"} |= "TEST_ERROR"')

# 7. Lưu kết quả ra file JSON để phục vụ tổng hợp
summary = {
    "generated_time_utc": fmt_now,
    "iso_time": iso_now,
    "wordpress": {
        "container": "news_wordpress",
        "job": "webapp",
        "service": "wordpress",
        "log_content": wp_log_content,
        "logql_queries": [
            '{container="news_wordpress"} |= "TEST_ERROR"',
            '{job="webapp"} |= "TEST_ERROR"'
        ],
        "verified_in_loki": len(wp_results) > 0,
        "matched_lines": wp_results
    },
    "mysql": {
        "container": "news_mysql",
        "job": "database",
        "service": "mysql",
        "log_content": mysql_log_content,
        "logql_queries": [
            '{container="news_mysql"} |= "TEST_ERROR"',
            '{job="database"} |= "TEST_ERROR"'
        ],
        "verified_in_loki": len(mysql_results) > 0,
        "matched_lines": mysql_results
    }
}

with open("d:\\trienkhaihethong\\test_logs_result.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("\n[BƯỚC 7] HOÀN TẤT VÀ ĐÃ LƯU KẾT QUẢ VÀO test_logs_result.json")
