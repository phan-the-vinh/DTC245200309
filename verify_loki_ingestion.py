import remote_exec
import json
import urllib.parse
import time

print("="*70)
print("KIỂM TRA TRUY VẤN LOKI CHO WORDPRESS VÀ MYSQL")
print("="*70)

# Chờ 5 giây để Promtail kịp đọc và đẩy log vào Loki
print("Đang chờ 5s...")
time.sleep(5)

def query_loki(logql):
    encoded = urllib.parse.quote(logql)
    # Lấy 15 phút gần nhất
    now_ns = int(time.time() * 1e9)
    start_ns = now_ns - int(15 * 60 * 1e9)
    url = f"http://loki:3100/loki/api/v1/query_range?query={encoded}&start={start_ns}&end={now_ns}&limit=10"
    cmd = f"docker exec news_promtail wget -qO- '{url}'"
    c, res, e = remote_exec.run_command(cmd)
    try:
        data = json.loads(res)
        results = data.get("data", {}).get("result", [])
        print(f"\n[+] LogQL: {logql}")
        print(f"    Số stream kết quả: {len(results)}")
        for idx, s in enumerate(results):
            labels = s.get("stream", {})
            values = s.get("values", [])
            print(f"    Stream #{idx+1} labels: {labels}")
            for v in values:
                ts, line = v[0], v[1]
                print(f"      - [{ts}] {line.strip()}")
    except Exception as ex:
        print(f"    Lỗi: {ex}, raw output: {res}")

query_loki('{container="news_wordpress"} |= "TEST_PIPE_WORDPRESS"')
query_loki('{container="news_mysql"} |= "TEST_ERROR"')
query_loki('{job="database"} |= "TEST_ERROR"')
query_loki('{job="webapp"} |= "TEST_ERROR"')
