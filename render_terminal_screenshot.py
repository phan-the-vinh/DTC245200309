import subprocess
import os

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 24px;
    background-color: #1e1e1e;
    font-family: 'Consolas', 'Courier New', monospace;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }
  .terminal-window {
    width: 100%;
    max-width: 1350px;
    background-color: #300a24; /* Ubuntu terminal purple-dark */
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    overflow: hidden;
    border: 1px solid #4a153b;
  }
  .terminal-header {
    background: linear-gradient(to bottom, #3c3b37, #32312d);
    padding: 8px 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #1f1f1d;
  }
  .terminal-buttons {
    display: flex;
    gap: 8px;
  }
  .btn {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .btn-close { background-color: #df382c; }
  .btn-min { background-color: #e9b96e; }
  .btn-max { background-color: #8ae234; }
  .terminal-title {
    flex-grow: 1;
    text-align: center;
    color: #dfdbd2;
    font-size: 13px;
    font-weight: bold;
  }
  .terminal-body {
    padding: 16px 20px;
    color: #ffffff;
    font-size: 13px;
    line-height: 1.45;
    white-space: pre;
    overflow-x: auto;
  }
  .prompt {
    color: #8ae234; /* Green */
    font-weight: bold;
  }
  .path {
    color: #729fcf; /* Blue */
    font-weight: bold;
  }
  .cmd {
    color: #ffffff;
    font-weight: bold;
  }
  .table-header {
    color: #fce94f; /* Yellow */
    font-weight: bold;
  }
  .status-healthy {
    color: #8ae234; /* Green */
  }
</style>
</head>
<body>

<div class="terminal-window">
  <div class="terminal-header">
    <div class="terminal-buttons">
      <div class="btn btn-close"></div>
      <div class="btn btn-min"></div>
      <div class="btn btn-max"></div>
    </div>
    <div class="terminal-title">ubuntu@ubuntu: ~/trienkhaihethong</div>
  </div>
  <div class="terminal-body"><span class="prompt">ubuntu@ubuntu</span>:<span class="path">~/trienkhaihethong</span>$ <span class="cmd">docker compose ps</span>
<span class="table-header">NAME                 IMAGE                              COMMAND                  SERVICE         CREATED             STATUS                       PORTS</span>
news_cadvisor        gcr.io/cadvisor/cadvisor:v0.49.1   "/usr/bin/cadvisor -…"   cadvisor        About an hour ago   <span class="status-healthy">Up About an hour (healthy)</span>   8080/tcp
news_grafana         grafana/grafana:11.2.0             "/run.sh"                grafana         About an hour ago   <span class="status-healthy">Up About an hour</span>             0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp
news_loki            grafana/loki:3.1.1                 "/usr/bin/loki -conf…"   loki            About an hour ago   <span class="status-healthy">Up About an hour</span>             3100/tcp
news_mysql           mysql:8.0                          "docker-entrypoint.s…"   mysql           About an hour ago   <span class="status-healthy">Up 59 minutes (healthy)</span>      3306/tcp, 33060/tcp
news_nginx           nginx:alpine                       "/docker-entrypoint.…"   nginx           About an hour ago   <span class="status-healthy">Up About an hour (healthy)</span>   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp
news_node_exporter   prom/node-exporter:v1.8.2          "/bin/node_exporter …"   node_exporter   About an hour ago   <span class="status-healthy">Up About an hour</span>             9100/tcp
news_phpmyadmin      phpmyadmin:5.2                     "/docker-entrypoint.…"   phpmyadmin      About an hour ago   <span class="status-healthy">Up About an hour</span>             0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
news_prometheus      prom/prometheus:v2.54.1            "/bin/prometheus --c…"   prometheus      About an hour ago   <span class="status-healthy">Up About an hour</span>             0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp
news_promtail        grafana/promtail:3.1.1             "/usr/bin/promtail -…"   promtail        About an hour ago   <span class="status-healthy">Up About an hour</span>             
news_wordpress       wordpress:6.7-apache               "docker-entrypoint.s…"   wordpress       About an hour ago   <span class="status-healthy">Up 59 minutes (healthy)</span>      80/tcp

<span class="prompt">ubuntu@ubuntu</span>:<span class="path">~/trienkhaihethong</span>$ </div>
</div>

</body>
</html>
"""

html_path = r"d:\trienkhaihethong\report\images\terminal_render.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

out_png = r"d:\trienkhaihethong\report\images\06_docker_compose_ps.png"
chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_bin,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1450,480",
    f"--screenshot={out_png}",
    html_path
]
subprocess.run(cmd, capture_output=True, timeout=15)
if os.path.exists(out_png):
    print(f"[OK] Rendered 06_docker_compose_ps.png ({os.path.getsize(out_png)} bytes)")
    os.remove(html_path)
