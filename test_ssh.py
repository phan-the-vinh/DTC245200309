import sys
import socket
import paramiko

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

HOST = "192.168.177.128"
PORT = 22
USER = "ubuntu"
PASS = "ubuntu"

def check_port(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def connect_ssh(host, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {user}@{host}:{port} ...")
    client.connect(host, port=port, username=user, password=password, timeout=10)
    print("SSH connection successful!")
    
    stdin, stdout, stderr = client.exec_command("uname -a && lsb_release -a && whoami")
    print("\n--- Command Output ---")
    print(stdout.read().decode('utf-8'))
    client.close()

if __name__ == "__main__":
    print(f"Kiểm tra kết nối port {PORT} tới {HOST}...")
    if check_port(HOST, PORT):
        print(f"Port {PORT} đang MỞ. Đang thử kết nối SSH...")
        connect_ssh(HOST, PORT, USER, PASS)
    else:
        print(f"Port {PORT} hiện CHƯA THỂ KẾT NỐI (Máy ảo chưa bật nguồn).")
