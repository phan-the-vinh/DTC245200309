import urllib.request
import urllib.error
import http.server
import socketserver
import threading
import json
import subprocess
import os
import time

GRAFANA_HOST = "192.168.177.128"
GRAFANA_PORT = 3000
LOCAL_PROXY_PORT = 8888
CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1. Login to Grafana
login_url = f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/login"
login_payload = json.dumps({"user": "admin", "password": "Grafana_Admin2026!"}).encode("utf-8")
req = urllib.request.Request(login_url, data=login_payload, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
cookies = resp.headers.get_all("Set-Cookie")
cookie_header = "; ".join([c.split(";")[0] for c in cookies])
print(f"[OK] Logged in to Grafana. Cookie header length: {len(cookie_header)}")

# Get real UIDs
ds_req = urllib.request.Request(f"http://{GRAFANA_HOST}:{GRAFANA_PORT}/api/datasources", headers={"Cookie": cookie_header})
ds_list = json.loads(urllib.request.urlopen(ds_req).read().decode("utf-8"))
prom_uid = next((d["uid"] for d in ds_list if d["type"] == "prometheus"), "prometheus")
loki_uid = next((d["uid"] for d in ds_list if d["type"] == "loki"), "loki")
print(f"[OK] Prometheus UID: {prom_uid}, Loki UID: {loki_uid}")

# 2. Forwarding Proxy
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
                
                # If loading dashboard JSON, map datasource UID if needed
                if "/api/dashboards/uid/" in self.path and target_resp.headers.get("Content-Type", "").startswith("application/json"):
                    body = body.replace(b'"uid":"prometheus"', f'"uid":"{prom_uid}"'.encode("utf-8"))
                    body = body.replace(b'"uid": "prometheus"', f'"uid": "{prom_uid}"'.encode("utf-8"))

                for h, val in target_resp.headers.items():
                    if h.lower() not in ["transfer-encoding", "content-length"]:
                        self.send_header(h, val)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for h, val in e.headers.items():
                if h.lower() not in ["transfer-encoding", "content-length"]:
                    self.send_header(h, val)
            body = e.read()
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
print(f"[OK] Proxy running on 127.0.0.1:{LOCAL_PROXY_PORT}")

# 3. Capture Screenshots
def capture(url, out_path, wait_ms=8000):
    print(f"[*] Capturing: {url} -> {out_path}...")
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1600,1050",
        f"--virtual-time-budget={wait_ms}",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    if os.path.exists(out_path):
        print(f"[OK] Captured: {out_path} ({os.path.getsize(out_path)} bytes)")
    else:
        print(f"[FAIL] Screenshot failed: return {res.returncode}")

# Capture 04_grafana_dashboard.png
dash_url = f"http://127.0.0.1:{LOCAL_PROXY_PORT}/d/devops-overview/devops-system-and-container-overview?kiosk&refresh=5s"
capture(dash_url, r"d:\trienkhaihethong\report\images\04_grafana_dashboard.png", wait_ms=8000)

# Capture 05_loki_logql.png
explore_url = f"http://127.0.0.1:{LOCAL_PROXY_PORT}/explore?left=%7B%22datasource%22:%22{loki_uid}%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%7Bjob%3D%5C%22nginx%5C%22%7D%22%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D"
capture(explore_url, r"d:\trienkhaihethong\report\images\05_loki_logql.png", wait_ms=8000)

proxy_server.shutdown()
print("[OK] Done capturing.")
