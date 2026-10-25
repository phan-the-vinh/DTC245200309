import remote_exec

print("Kiểm tra PID 1 và fd trong news_mysql:")
code, out, err = remote_exec.run_command("docker exec news_mysql ps aux")
print(out)

code, out, err = remote_exec.run_command("docker exec news_mysql ls -l /proc/1/fd")
print(out)

print("Kiểm tra PID 1 và fd trong news_wordpress:")
code, out, err = remote_exec.run_command("docker exec news_wordpress ps aux")
print(out)

code, out, err = remote_exec.run_command("docker exec news_wordpress ls -l /proc/1/fd")
print(out)
