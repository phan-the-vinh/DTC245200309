import sys
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

print("Adding files to git...")
run_command("cd /home/ubuntu/trienkhaihethong; git add README.md report/")

print("Committing...")
code, out, _ = run_command('cd /home/ubuntu/trienkhaihethong; git commit -m "docs: Hoàn thiện README hướng dẫn vận hành và báo cáo cuối kỳ"')
print(out)

print("Git Log:")
code, out, _ = run_command("cd /home/ubuntu/trienkhaihethong; git log --oneline -n 6")
print(out)
