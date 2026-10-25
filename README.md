# CỔNG THÔNG TIN TIN TỨC CÔNG NGHỆ (TECH NEWS PORTAL)
## ĐỒ ÁN CUỐI KỲ: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

Hệ thống được thiết kế và triển khai trên nền tảng **Ubuntu Linux** sử dụng **Docker Compose**, tích hợp đầy đủ kiến trúc Microservices/Containers bao gồm Cổng thông tin (WordPress), Hệ quản trị cơ sở dữ liệu (MySQL), Công cụ quản trị CSDL (phpMyAdmin), Reverse Proxy và SSL Termination (Nginx), Hệ thống Giám sát chỉ số tài nguyên (Prometheus + Node Exporter + cAdvisor + Grafana), và Hệ thống Giám sát & Tập trung Log (Loki + Promtail).

---

## 1. SƠ ĐỒ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

```
                            [ NGƯỜI DÙNG / TRÌNH DUYỆT ]
                                       │
                    HTTP :80 (Redirect 301) / HTTPS :443 (TLS/SSL)
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │     Nginx Reverse Proxy       │
                       │         (news_nginx)          │
                       └──────┬─────────────────┬──────┘
                              │                 │
             / (Proxy Pass)   │                 │   /pma/ (Proxy Pass)
                              ▼                 ▼
              ┌─────────────────────┐   ┌────────────────────────┐
              │  WordPress App      │   │  phpMyAdmin Web UI     │
              │  (news_wordpress)   │   │   (news_phpmyadmin)    │
              └──────────┬──────────┘   └──────────┬─────────────┘
                         │                         │
                         │      MySQL Port :3306   │
                         └────────────┬────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │       MySQL Database      │
                        │        (news_mysql)       │
                        └───────────────────────────┘

========================================================================
[ HỆ THỐNG GIÁM SÁT METRICS ]              [ HỆ THỐNG QUẢN LÝ LOGS ]
┌───────────────────────────┐              ┌───────────────────────────┐
│ Host OS: Node Exporter    │              │ Host / Docker Containers  │
│ (news_node_exporter)      │              │ (docker.sock & log files) │
└─────────────┬─────────────┘              └─────────────┬─────────────┘
              │ :9100 Scrape                             │ Read logs
┌─────────────┴─────────────┐              ┌─────────────▼─────────────┐
│ Container: cAdvisor       │              │ Promtail Log Shipper      │
│ (news_cadvisor)           │              │ (news_promtail)           │
└─────────────┬─────────────┘              └─────────────┬─────────────┘
              │ :8080 Scrape                             │ Push :3100
┌─────────────▼─────────────┐              ┌─────────────▼─────────────┐
│ Prometheus Time-Series DB │              │ Grafana Loki Log DB       │
│ (news_prometheus :9090)   │              │ (news_loki :3100)         │
└─────────────┬─────────────┘              └─────────────┬─────────────┘
              │ Datasource: Prometheus                   │ Datasource: Loki
              └─────────────────────┬────────────────────┘
                                    ▼
                      ┌───────────────────────────┐
                      │  Grafana Visual Dashboard │
                      │   (news_grafana :3000)    │
                      └───────────────────────────┘
```

---

## 2. PHÂN VÙNG MẠNG VÀ DANH SÁCH DỊCH VỤ

Hệ thống được cô lập (Network Segmentation) thành 3 mạng Docker riêng biệt:
1. `news_frontend_net`: Mạng kết nối người dùng bên ngoài với Nginx Proxy, WordPress và phpMyAdmin.
2. `news_backend_net`: Mạng nội bộ chỉ dành cho giao tiếp giữa WordPress, phpMyAdmin và MySQL. Cổng 3306 của MySQL **hoàn toàn không public** ra ngoài host.
3. `news_monitoring_net`: Mạng giám sát nội bộ kết nối Node Exporter, cAdvisor, Prometheus, Loki, Promtail và Grafana.

| Tên Container | Hình ảnh (Image) | Cổng Public (Host) | Cổng Nội bộ (Internal) | Mục đích / Vai trò |
| :--- | :--- | :--- | :--- | :--- |
| `news_nginx` | `nginx:1.27-alpine` | `80`, `443` | `80`, `443` | Reverse Proxy, SSL Offloading, Security Headers |
| `news_wordpress` | `wordpress:6.7-apache` | Không public | `80` | Cổng thông tin tin tức WordPress |
| `news_mysql` | `mysql:8.0` | Không public | `3306` | Hệ quản trị cơ sở dữ liệu MySQL |
| `news_phpmyadmin` | `phpmyadmin/phpmyadmin:5.2` | `8081` (Dự phòng) | `80` | Giao diện quản trị CSDL qua Web |
| `news_prometheus` | `prom/prometheus:v2.54.1` | `9090` | `9090` | Thu thập và lưu trữ Metrics |
| `news_node_exporter` | `prom/node-exporter:v1.8.2` | Không public | `9100` | Xuất chỉ số phần cứng Host OS (CPU, RAM, Disk) |
| `news_cadvisor` | `gcr.io/cadvisor/cadvisor:v0.49.1` | Không public | `8080` | Xuất chỉ số hiệu năng Container Docker |
| `news_grafana` | `grafana/grafana:11.2.0` | `3000` | `3000` | Dashboard trực quan hóa Metrics và Logs |
| `news_loki` | `grafana/loki:3.1.1` | Không public | `3100` | Lưu trữ và lập chỉ mục Logs |
| `news_promtail` | `grafana/promtail:3.1.1` | Không public | `9080` | Đọc log từ Docker Socket và gửi về Loki |

---

## 3. YÊU CẦU MÔI TRƯỜNG (PREREQUISITES)

- **Hệ điều hành Host:** Ubuntu Linux 22.04 LTS / 24.04 LTS / 26.04 LTS (x86_64).
- **Phần cứng khuyến nghị:** Tối thiểu 2 vCPU, 4GB RAM, 20GB dung lượng ổ đĩa khả dụng.
- **Phần mềm yêu cầu:**
  - Docker Engine: `>= 24.0` (đã kích hoạt systemd service).
  - Docker Compose: `v2.x` (plugin tích hợp `docker compose`).
  - OpenSSL: Khởi tạo chứng chỉ SSL self-signed nếu chưa có.
  - curl / git / bash shell.

---

## 4. HƯỚNG DẪN CẤU HÌNH BIẾN MÔI TRƯỜNG (.ENV)

File `.env` chứa toàn bộ mật khẩu, thông tin kết nối và cấu hình bảo mật. **Tuyệt đối không commit file `.env` lên Git.**

1. Sao chép file mẫu:
   ```bash
   cp .env.example .env
   ```
2. Thiết lập quyền bảo vệ file `.env` (chỉ người dùng sở hữu mới có quyền đọc):
   ```bash
   chmod 600 .env
   ```
3. Xem xét và chỉnh sửa các tham số trong file `.env`:
   - `MYSQL_ROOT_PASSWORD`: Mật khẩu tài khoản `root` của MySQL.
   - `MYSQL_DATABASE`: Tên database WordPress (ví dụ: `news_portal_db`).
   - `MYSQL_USER`: Tên tài khoản MySQL cho ứng dụng (ví dụ: `news_user`).
   - `MYSQL_PASSWORD`: Mật khẩu tài khoản MySQL cho ứng dụng.
   - `GRAFANA_ADMIN_PASSWORD`: Mật khẩu quản trị Grafana.
   - `APP_DOMAIN`: Địa chỉ IP hoặc Domain máy chủ (ví dụ: `192.168.177.128` hoặc `demo.local`).

---

## 5. KHỞI CHẠY VÀ QUẢN LÝ DỊCH VỤ

### 5.1. Khởi tạo chứng chỉ SSL Self-signed (nếu chưa có)
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/selfsigned.key \
  -out nginx/ssl/selfsigned.crt \
  -subj "/C=VN/ST=HaNoi/L=HaNoi/O=DevOpsSysAdmin/OU=NewsPortal/CN=192.168.177.128"
chmod 600 nginx/ssl/selfsigned.key
```

### 5.2. Khởi chạy toàn bộ hệ thống
```bash
docker compose up -d
```

### 5.3. Kiểm tra trạng thái toàn bộ containers
```bash
docker compose ps
```
Tất cả các dịch vụ có healthcheck (`news_mysql`, `news_wordpress`, `news_nginx`) phải hiển thị trạng thái `Up (healthy)`.

### 5.4. Xem log hoạt động theo dịch vụ
```bash
# Xem log toàn bộ hệ thống theo thời gian thực
docker compose logs -f

# Xem log riêng của Nginx Reverse Proxy
docker compose logs -f nginx

# Xem log riêng của WordPress
docker compose logs -f wordpress

# Xem log của Promtail để kiểm tra quá trình đẩy log
docker compose logs -f promtail
```

---

## 6. HƯỚNG DẪN TRUY CẬP CÁC DỊCH VỤ

| Dịch vụ | URL Truy cập | Giao thức / Cổng | Tài khoản / Mật khẩu mặc định |
| :--- | :--- | :--- | :--- |
| **Website Tin tức (WordPress)** | `https://<IP_SERVER>/` | HTTPS :443 (Tự chuyển từ HTTP :80) | Xem trong CMS quản trị |
| **Trang Quản trị WordPress** | `https://<IP_SERVER>/wp-admin/` | HTTPS :443 | `admin_news` / *(Cấu hình trong lúc cài đặt)* |
| **phpMyAdmin (Qua Nginx)** | `https://<IP_SERVER>/pma/` | HTTPS :443 | User: `news_user` hoặc `root` |
| **phpMyAdmin (Cổng trực tiếp)** | `http://<IP_SERVER>:8081/` | HTTP :8081 | Quản trị dự phòng |
| **Prometheus Monitoring** | `http://<IP_SERVER>:9090/` | HTTP :9090 | Truy cập trực tiếp (Không yêu cầu auth) |
| **Grafana Dashboard** | `http://<IP_SERVER>:3000/` | HTTP :3000 | `admin` / *(Theo GRAFANA_ADMIN_PASSWORD)* |

> **Lưu ý về SSL Self-Signed:** Khi truy cập bằng trình duyệt qua HTTPS, trình duyệt sẽ hiển thị cảnh báo *"Your connection is not private"* (Cảnh báo chứng chỉ tự ký). Bấm **Advanced -> Proceed to <IP> (unsafe)** để tiếp tục.

---

## 7. TRUY VẤN VÀ PHÂN TÍCH LOG VỚI LOGQL (LOKI)

Truy cập Grafana -> Menu **Explore** -> Chọn Data source là **Loki**. Bạn có thể thực thi 3 truy vấn chuẩn hóa sau:

### Truy vấn 1: Theo dõi toàn bộ Access và Error Log của Nginx
Xem luồng truy cập và kiểm tra hoạt động của Reverse Proxy:
```logql
{job="nginx"}
```
*Kết quả:* Trả về toàn bộ log HTTP request đi qua Nginx Reverse Proxy kèm mã trạng thái, phương thức và thời gian phản hồi.

### Truy vấn 2: Phát hiện các yêu cầu HTTP lỗi 5xx trên Reverse Proxy
Giám sát các sự cố phía máy chủ (Server Error 500, Bad Gateway 502, Gateway Timeout 504):
```logql
{job="nginx"} |~ "HTTP/[0-9.]+\" 5[0-9][0-9]"
```
*Ý nghĩa:* Sử dụng Regex Filter `|~` để bắt chính xác các dòng access log có mã trạng thái bắt đầu bằng số `5`.

### Truy vấn 3: Phát hiện lỗi, Exception và cảnh báo nghiêm trọng từ Ứng dụng Web
Theo dõi lỗi PHP runtime, lỗi truy vấn cơ sở dữ liệu hoặc lỗi khởi động trong WordPress:
```logql
{job="webapp"} |~ "(?i)(error|exception|failed)"
```
*Ý nghĩa:* Thu thập log từ container `news_wordpress`, lọc không phân biệt hoa thường (`(?i)`) chứa các từ khóa `error`, `exception`, hoặc `failed`.

---

## 8. BẢO TRÌ, DỪNG VÀ XỬ LÝ SỰ CỐ KHÔNG MẤT DỮ LIỆU

### 8.1. Dừng và Khởi động lại an toàn (Zero Data Loss)
- Để khởi động lại một dịch vụ cụ thể (ví dụ Nginx sau khi sửa cấu hình):
  ```bash
  docker compose restart nginx
  ```
- Để dừng hệ thống tạm thời mà **vẫn giữ nguyên 100% dữ liệu database và website**:
  ```bash
  docker compose down
  ```
  *(Tuyệt đối KHÔNG thêm cờ `-v` hoặc `--volumes`)*.
- Khởi động lại hệ thống:
  ```bash
  docker compose up -d
  ```

### 8.2. Xử lý sự cố thường gặp (Troubleshooting)
1. **Cổng 80 hoặc 443 bị chiếm dụng:**
   - Kiểm tra tiến trình đang chạy: `sudo ss -tulpn | grep -E ':(80|443)'`
   - Nếu máy chủ Ubuntu đang bật Nginx cục bộ (`systemctl status nginx`), hãy dừng và tắt dịch vụ native:
     ```bash
     sudo systemctl stop nginx
     sudo systemctl disable nginx
     ```
2. **WordPress hiển thị lỗi "Error establishing a database connection":**
   - Kiểm tra trạng thái MySQL: `docker compose ps news_mysql`
   - Kiểm tra log MySQL: `docker compose logs news_mysql`
   - Kiểm tra biến môi trường kết nối trong WordPress: đảm bảo `WORDPRESS_DB_HOST=news_mysql:3306`, tên user và password khớp với MySQL.
3. **Grafana không nhận Datasource Prometheus hoặc Loki:**
   - Kiểm tra kết nối mạng nội bộ giữa các container:
     ```bash
     docker compose exec news_grafana nc -z -v -w3 news_prometheus 9090
     docker compose exec news_grafana nc -z -v -w3 news_loki 3100
     ```
   - Đảm bảo các cấu hình trong `grafana/provisioning/datasources/` trỏ đúng tên service Docker nội bộ (`http://news_prometheus:9090` và `http://news_loki:3100`).

---

## 9. QUẢN LÝ MÃ NGUỒN VÀ LỊCH SỬ COMMIT

Dự án được quản lý phiên bản với Git tuân thủ quy chuẩn Conventional Commits:
- `3edf85b` - `feat(app): Triển khai WordPress, MySQL và phpMyAdmin với Docker Compose`
- `6ad465e` - `feat(proxy): Nginx Reverse Proxy và bảo mật HTTP`
- `5e16e02` - `feat(monitoring): Prometheus và Grafana`
- `b7f07ab` - `feat(logging): Loki và Promtail`
- *(Next)* - `docs: Hoàn thiện README hướng dẫn vận hành và tài liệu báo cáo`
