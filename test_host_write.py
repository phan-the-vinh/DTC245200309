import remote_exec

code, out, err = remote_exec.run_command("docker inspect --format '{{.State.Pid}}' news_mysql")
mysql_pid = out.strip()
print(f"news_mysql host PID: {mysql_pid}")

test_msg = "2026-10-26T01:16:00.000000Z 0 [ERROR] [MY-000000] [Server] [TEST_ERROR] [SIMULATION] Host-injected simulated test error for MySQL container"
cmd = f"echo '{test_msg}' | sudo tee /proc/{mysql_pid}/fd/2"
code, out, err = remote_exec.run_command(cmd, sudo=True)
print("tee result:", code)

code, out, err = remote_exec.run_command("docker logs news_mysql --tail 3")
print("docker logs news_mysql:")
print(out)
