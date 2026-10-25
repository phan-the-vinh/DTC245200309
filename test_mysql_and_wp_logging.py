import remote_exec
import json
import urllib.parse
import time

print("="*60)
print("THỬ NGHIỆM GHI LOG VÀO DOCKER LOGS CHO WORDPRESS VÀ MYSQL")
print("="*60)

# 1. Thử nghiệm PHP error_log trong WordPress
print("\n[1] GỌI PHP error_log() TRONG CONTAINER news_wordpress:")
wp_php_cmd = "docker exec news_wordpress php -r 'error_log(\"[TEST_ERROR] [SIMULATION] WordPress simulated test error log for Grafana Explore verification\");'"
code, out, err = remote_exec.run_command(wp_php_cmd)
print("PHP error_log Exit Code:", code)
print("PHP error_log out:", out.strip())
if err: print("PHP error_log err:", err.strip())


code, out, err = remote_exec.run_command("docker logs news_wordpress --tail 3")
print("Docker logs news_wordpress:")
print(out.strip())

# 2. Thử nghiệm MySQL error logging
print("\n[2] THỬ NGHIỆM GHI LOG VÀO MYSQL SERVER ERROR LOG:")
# Thử 1: Failed connection attempt with TEST_ERROR user
mysql_cmd = "docker exec news_mysql mysql -u TEST_ERROR_SIMULATION_USER -pwrongpass 2>&1"
code, out, err = remote_exec.run_command(mysql_cmd)
print("MySQL client output:", out.strip())

code, out, err = remote_exec.run_command("docker logs news_mysql --tail 3")
print("Docker logs news_mysql:")
print(out.strip())


