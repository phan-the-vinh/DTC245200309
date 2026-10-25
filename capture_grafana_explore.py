import urllib.request
import urllib.parse
import json
import subprocess
import os
import time
import http.server
import socketserver
import threading

GRAFANA_HOST = "192.168.177.128"
GRAFANA_PORT = 3000
LOCAL_PROXY_PORT = 8889
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

login_url = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/login"
login_payload = json.dumps({"user": "admin", "password": "admin"}).encode("utf-8")
req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
cookies = resp.headers.get_all("Set-Cookie")
cookie_header = "; ".join([c.split(";")[0] for c in cookies])
print(f"[OK] Logged in to Grafana. Cookie header length: {len(cookie_header)}")

ds_req = urllib.request.Request(f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/api/datasources", headers={"Cookie": cookie_header})
ds_list = json.loads(urllib.request.urlopen(ds_req).read().decode("utf-8"))
loki_uid = next((d["uid"] for d in ds_list if d["type"] == "loki"), "P8E80F9AEF21F6940")

class GrafanaProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.forward_request("GET")
    def do_POST(self):
        self.forward_request("POST")
    def forward_request(self, method):
        target_url = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}{self.path}"
        data = None
        if "Content-Length" in self.headers:
            length = int(self.headers["Content-Length"])
            data = self.rfile.read(length)
        headers = {}
        for h, val in self.headers.items():
            if h.lower() not in ["host", "cookie", "origin", "referer"]:
                headers[h] = val
        headers["Host"] = f"{GRAFANA_HOST}:{GRAFANA_PORT}"
        headers["Cookie"] = cookie_header
        headers["Origin"] = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}"
        headers["Referer"] = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/"
        req = urllib.request.Request(target_url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=15) as target_resp:
                self.send_response(target_resp.status)
                body = target_resp.read()
                for h, val in target_resp.headers.items():
                    if h.lower() not in ["transfer-encoding", "content-length"]:
                        self.send_header(h, val)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))
    def log_message(self, format, *args):
        pass

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

proxy_server = ThreadedHTTPServer(("127.0.0.1", LOCAL_PROXY_PORT), GrafanaProxyHandler)
proxy_thread = threading.Thread(target=proxy_server.serve_forever)
proxy_thread.daemon = True
proxy_thread.start()

def capture(url, out_path, wait_ms=10000):
    print(f"[*] Capturing: {url} -> {out_path}...")
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1600,1000",
        f"--virtual-time-budget={wait_ms}",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    if os.path.exists(out_path):
        print(f"[OK] Captured: {out_path} ({os.path.getsize(out_path)} bytes)")
    else:
        print(f"[FAIL] Screenshot failed: return {res.returncode}")

# WordPress explore
query_wp = urllib.parse.quote(json.dumps({
    "datasource": loki_uid,
    "queries": [{"refId": "A", "expr": '{container="news_wordpress"} |= "TEST_ERROR"'}],
    "range": {"from": "now-1h", "to": "now"}
}))
url_wp = f"http://127.0.0.1:{LOCAL_PROXY_PORT}/explore?left={query_wp}"
capture(url_wp, r"d:\trienkhaihethong\report\images\grafana_explore_wordpress_test_error.png", wait_ms=8000)

# MySQL explore
query_mysql = urllib.parse.quote(json.dumps({
    "datasource": loki_uid,
    "queries": [{"refId": "A", "expr": '{container="news_mysql"} |= "TEST_ERROR"'}],
    "range": {"from": "now-1h", "to": "now"}
}))
url_mysql = f"http://127.0.0.1:{LOCAL_PROXY_PORT}/explore?left={query_mysql}"
capture(url_mysql, r"d:\trienkhaihethong\report\images\grafana_explore_mysql_test_error.png", wait_ms=8000)

proxy_server.shutdown()
print("[OK] Done capturing Explore screenshots.")
