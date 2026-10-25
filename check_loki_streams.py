import urllib.request
import json
import urllib.parse
import sys

if sys.stdout.encoding.lower() != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8': sys.stderr.reconfigure(encoding='utf-8')

print("="*70)
print("KIỂM TRA CÁC NHÃN VÀ STREAMS HIỆN CÓ TRÊN LOKI")
print("="*70)

LOKI_URL = "http://192.168.177.128:3100"

# 1. Lấy danh sách labels từ Loki (/loki/api/v1/labels)
try:
    with urllib.request.urlopen(f"{LOKI_URL}/loki/api/v1/labels", timeout=5) as r:
        labels = json.loads(r.read().decode())['data']
        print(f"[1] Các nhãn (label names) hiện có trên Loki: {labels}")
        for lbl in labels:
            with urllib.request.urlopen(f"{LOKI_URL}/loki/api/v1/label/{lbl}/values", timeout=5) as r_val:
                vals = json.loads(r_val.read().decode())['data']
                print(f"  - Nhãn '{lbl}': {vals}")
except Exception as e:
    print(f"Lỗi lấy labels từ Loki: {e}")

# 2. Truy vấn thử log gần đây của từng job/container
def query_loki(logql):
    url = f"{LOKI_URL}/loki/api/v1/query_range?" + urllib.parse.urlencode({
        "query": logql,
        "limit": 5,
        "range": "1h"
    })
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())['data']['result']
            print(f"\n--- LogQL: {logql} ---")
            print(f"  Số luồng (streams): {len(data)}")
            for s in data:
                stream_labels = s.get('stream', {})
                values = s.get('values', [])
                print(f"  Stream: {stream_labels} | Số dòng log: {len(values)}")
                for ts, line in values[:2]:
                    print(f"    [{ts}] {line.strip()[:120]}")
    except Exception as e:
        print(f"Lỗi truy vấn '{logql}': {e}")

print("\n[2] KIỂM TRA CÁC LOGQL TIÊU BIỂU:")
query_loki('{job="nginx"}')
query_loki('{job="webapp"}')
query_loki('{job="database"}')
query_loki('{container="news_wordpress"}')
query_loki('{container="news_mysql"}')
