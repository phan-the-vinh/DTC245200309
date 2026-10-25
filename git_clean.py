import sys
sys.path.append('d:/trienkhaihethong')
from remote_exec import upload_file, run_command

upload_file('d:/trienkhaihethong/.gitignore', '/home/ubuntu/trienkhaihethong/.gitignore')
run_command('cd /home/ubuntu/trienkhaihethong; git add .gitignore nginx/conf.d/default.conf')
code, out, _ = run_command('cd /home/ubuntu/trienkhaihethong; git commit -m "chore: Cập nhật .gitignore và hoàn thiện cấu hình Nginx"')
print("Commit output:\n", out)
code, out, _ = run_command('cd /home/ubuntu/trienkhaihethong; git status')
print("Git Status:\n", out)
code, out, _ = run_command('cd /home/ubuntu/trienkhaihethong; git log --oneline -n 6')
print("Git Log:\n", out)
