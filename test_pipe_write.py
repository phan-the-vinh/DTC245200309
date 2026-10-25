import remote_exec

print("Thử nghiệm ghi vào /proc/1/fd/2 với user root (-u 0):")

code, out, err = remote_exec.run_command("docker exec -u 0 news_mysql sh -c 'echo \"TEST_PIPE_MYSQL\" > /proc/1/fd/2'")
print("news_mysql exec:", code, out, err)

code, out, err = remote_exec.run_command("docker logs news_mysql --tail 2")
print("news_mysql docker logs:")
print(out)

code, out, err = remote_exec.run_command("docker exec news_wordpress sh -c 'echo \"TEST_PIPE_WORDPRESS\" > /proc/1/fd/2'")
print("news_wordpress exec:", code, out, err)

code, out, err = remote_exec.run_command("docker logs news_wordpress --tail 2")
print("news_wordpress docker logs:")
print(out)
