import remote_exec

code, out, err = remote_exec.run_command("docker inspect --format '{{.State.Pid}}' news_mysql")
mysql_pid = out.strip()
print(f"news_mysql host PID: {mysql_pid}")

code, out, err = remote_exec.run_command(f"ls -l /proc/{mysql_pid}/fd", sudo=True)
print(out)
