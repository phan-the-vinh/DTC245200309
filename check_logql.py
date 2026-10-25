import urllib.parse
import json
import time
from remote_exec import run_command, upload_file

def trigger_sample_logs():
    print("-> Sao chép error_test.php vào WordPress container và kích hoạt log...")
    upload_file("d:\\trienkhaihethong\\error_test.php", "/home/ubuntu/trienkhaihethong/error_test.php")
    run_command("docker cp /home/ubuntu/trienkhaihethong/error_test.php news_wordpress:/var/www/html/error_test.php")
    
    # 1. Trigger Nginx 5xx simulation
    run_command("curl -k -s https://127.0.0.1/error500 > /dev/null; curl -k -s https://127.0.0.1/error502 > /dev/null")
    
    # 2. Trigger WordPress error via HTTP request
    run_command("curl -k -s https://127.0.0.1/error_test.php > /dev/null")
    
    # Wait for Promtail to scrape and push to Loki
    time.sleep(3)

def query_logql(query_str, label_title):
    print(f"\n=======================================================")
    print(f"LogQL Query: {query_str}")
    print(f"Mô tả: {label_title}")
    print(f"=======================================================")
    
    encoded = urllib.parse.quote(query_str)
    cmd = f"docker exec news_promtail wget -qO- 'http://loki:3100/loki/api/v1/query?query={encoded}&limit=5'"
    code, out, err = run_command(cmd)
    
    try:
        data = json.loads(out)
        results = data.get("data", {}).get("result", [])
        if not results:
            print("[Trạng thái] Không có dòng log nào khớp truy vấn.")
        else:
            print(f"[Trạng thái] THÀNH CÔNG! Tìm thấy {len(results)} log stream:")
            for stream in results:
                stream_labels = stream.get("stream", {})
                print(f"  Labels: {stream_labels}")
                values = stream.get("values", [])
                for val in values[:3]:
                    timestamp, line = val[0], val[1]
                    print(f"    -> [{timestamp}]: {line.strip()}")
    except Exception as e:
        print(f"[Error parsing JSON]: {e}\nRaw Output: {out}\nErr: {err}")

if __name__ == "__main__":
    trigger_sample_logs()
    
    # Query 1: Xem log Nginx
    query_logql('{job="nginx"}', "1. Xem toàn bộ log Nginx Reverse Proxy")
    
    # Query 2: Tìm request HTTP lỗi 5xx
    query_logql('{job="nginx"} |~ "HTTP/[0-9.]+\\" 5[0-9][0-9]"', "2. Lọc các HTTP request lỗi 5xx trên Nginx")
    
    # Query 3: Tìm thông điệp lỗi trong log ứng dụng
    query_logql('{job="webapp"} |~ "(?i)(error|exception|failed)"', "3. Tìm thông điệp lỗi (error/exception/failed) trong log ứng dụng WordPress")
