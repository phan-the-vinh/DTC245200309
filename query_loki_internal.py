import remote_exec
import urllib.parse
import json
import sys
import time

print("="*70)
print("TRUY VẤN LOKI QUA NEWS_PROMTAIL")
print("="*70)

def query_loki(logql):
    encoded = urllib.parse.quote(logql)
    # Start 1h ago, end now in nanoseconds
    now_ns = int(time.time() * 1e9)
    start_ns = now_ns - int(3600 * 1e9)
    cmd = f"docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/query_range?query={encoded}&start={start_ns}&end={now_ns}&limit=10'"
    code, out, err = remote_exec.run_command(cmd)
    try:
        data = json.loads(out)
        results = data.get("data", {}).get("result", [])
        print(f"\nLogQL: {logql}")
        print(f"Số streams khớp: {len(results)}")
        for s in results:
            print("  Stream labels:", s.get("stream"))
            for v in s.get("values", [])[:3]:
                print(f"    [{v[0]}] {v[1].strip()[:140]}")
    except Exception as e:
        print(f"Lỗi: {e}, Raw: {out}")


# Kiểm tra labels
cmd = "docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/label/container/values'"
code, out, err = remote_exec.run_command(cmd)
print("Container label values:", out.strip())

cmd = "docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/label/job/values'"
code, out, err = remote_exec.run_command(cmd)
print("Job label values:", out.strip())

# Query WordPress test error
query_loki('{container="news_wordpress"} |= "TEST_ERROR"')
query_loki('{job="webapp"} |= "TEST_ERROR"')

# Query MySQL warning
query_loki('{container="news_mysql"}')
query_loki('{job="database"}')
