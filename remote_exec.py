import sys
import os
import argparse
import paramiko

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

HOST = "192.168.177.128"
PORT = 22
USER = "ubuntu"
PASS = "ubuntu"

def get_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=PORT, username=USER, password=PASS, timeout=10)
    return client

import shlex

def run_command(cmd, sudo=False):
    client = get_ssh_client()
    try:
        if sudo:
            full_cmd = f"sudo -S bash -c {shlex.quote(cmd)}"
        else:
            full_cmd = f"bash -c {shlex.quote(cmd)}"
        
        stdin, stdout, stderr = client.exec_command(full_cmd, get_pty=True)
        if sudo:
            stdin.write(PASS + "\n")
            stdin.flush()
            
        output = stdout.read().decode('utf-8', errors='replace')
        err_output = stderr.read().decode('utf-8', errors='replace')
        exit_code = stdout.channel.recv_exit_status()
        
        if sudo and "[sudo] password for" in output:
            lines = output.splitlines()
            output = "\n".join(l for l in lines if not l.startswith("[sudo] password for"))
            
        return exit_code, output, err_output
    finally:
        client.close()

def upload_file(local_path, remote_path):
    client = get_ssh_client()
    sftp = client.open_sftp()
    try:
        remote_dir = os.path.dirname(remote_path).replace("\\", "/")
        try:
            sftp.stat(remote_dir)
        except IOError:
            dirs = remote_dir.split('/')
            cur = ""
            for d in dirs:
                if not d: continue
                cur += "/" + d
                try:
                    sftp.stat(cur)
                except IOError:
                    sftp.mkdir(cur)
        sftp.put(local_path, remote_path)
        print(f"Uploaded: {local_path} -> {remote_path}")
    finally:
        sftp.close()
        client.close()

def upload_dir(local_path, remote_path):
    client = get_ssh_client()
    sftp = client.open_sftp()
    try:
        for root, dirs, files in os.walk(local_path):
            rel_dir = os.path.relpath(root, local_path).replace("\\", "/")
            cur_remote_dir = remote_path if rel_dir == "." else f"{remote_path}/{rel_dir}"
            try:
                sftp.stat(cur_remote_dir)
            except IOError:
                dirs = cur_remote_dir.split('/')
                cur = ""
                for d in dirs:
                    if not d: continue
                    cur += "/" + d
                    try:
                        sftp.stat(cur)
                    except IOError:
                        sftp.mkdir(cur)
            for f in files:
                if f.endswith(".pyc") or f in ["remote_exec.py", "test_ssh.py"]:
                    continue
                local_file = os.path.join(root, f)
                remote_file = f"{cur_remote_dir}/{f}"
                sftp.put(local_file, remote_file)
                print(f"Uploaded: {remote_file}")
    finally:
        sftp.close()
        client.close()

def download_file(remote_file, local_file):
    client = get_ssh_client()
    sftp = client.open_sftp()
    try:
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        sftp.get(remote_file, local_file)
        print(f"Downloaded: {remote_file} -> {local_file}")
    finally:
        sftp.close()
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH & SFTP helper")
    parser.add_argument("command", nargs="?", default=None, help="Command to run")
    parser.add_argument("--sudo", action="store_true", help="Run with sudo")
    parser.add_argument("--upload-all", action="store_true", help="Upload workspace to remote")
    parser.add_argument("--upload", nargs=2, metavar=("LOCAL", "REMOTE"), help="Upload single file")
    parser.add_argument("--download", nargs=2, metavar=("REMOTE", "LOCAL"), help="Download file from remote")
    args = parser.parse_args()
    
    if args.upload:
        upload_file(args.upload[0], args.upload[1])
        sys.exit(0)
    elif args.upload_all:
        upload_dir("d:\\trienkhaihethong", "/home/ubuntu/trienkhaihethong")
        sys.exit(0)
    elif args.download:
        download_file(args.download[0], args.download[1])
        sys.exit(0)
    elif args.command:
        code, out, err = run_command(args.command, sudo=args.sudo)
        if out:
            print(out, end="")
        if err:
            print(err, file=sys.stderr, end="")
        sys.exit(code)
    else:
        parser.print_help()
