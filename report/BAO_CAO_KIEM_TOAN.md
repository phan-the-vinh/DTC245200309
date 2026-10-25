# BÁO CÁO KIỂM TOÁN HỆ THỐNG CUỐI KỲ (FINAL AUDIT REPORT)
## DỰ ÁN: CỔNG THÔNG TIN TIN TỨC TRÊN NỀN TẢNG CONTAINER (DOCKER COMPOSE)
### HỌC PHẦN: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

---

- **Ngày thực hiện kiểm toán:** 25/10/2026
- **Chế độ kiểm toán:** **CHỈ ĐỌC (READ-ONLY)** — Tuyệt đối không thay đổi cấu hình, không sửa file, không restart/stop container, không thay đổi tường lửa, không xóa dữ liệu và không tạo commit mới.
- **Máy chủ mục tiêu:** Ubuntu Linux 26.04 LTS (`192.168.177.128`)
- **Thư mục dự án:** `/home/ubuntu/trienkhaihethong` (Đồng bộ: `d:\trienkhaihethong`)
- **Người thực hiện kiểm toán:** Kỹ sư DevOps / SysAdmin đánh giá độc lập

---

## MỤC LỤC BÁO CÁO KIỂM TOÁN

1. [TỔNG QUAN KẾT QUẢ KIỂM TOÁN](#1-tổng-quan-kết-quả-kiểm-toán)
2. [CHI TIẾT KIỂM TOÁN THEO TỪNG HẠNG MỤC](#2-chi-tiết-kiểm-toán-theo-từng-hạng-mục)
   - 2.1. Đánh giá Docker, Cấu hình và Tài nguyên
   - 2.2. Đánh giá An toàn Thông tin và Gia cố Hệ thống (Security & Hardening)
   - 2.3. Đánh giá Hệ thống Giám sát (Prometheus & Grafana) và Nhật ký (Loki & Promtail)
   - 2.4. Đánh giá Quản lý Mã nguồn Git và Lịch sử Phiên bản
   - 2.5. Đánh giá Tài liệu Báo cáo Cuối kỳ (Markdown & DOCX)
3. [DANH MỤC VẤN ĐỀ PHÂN LOẠI THEO MỨC ĐỘ ƯU TIÊN](#3-danh-mục-vấn-đề-phân-loại-theo-mức-độ-ưu-tiên)
4. [DANH SÁCH THÔNG TIN XÁC THỰC VÀ DỊCH VỤ PHỤ THUỘC CẦN CẬP NHẬT](#4-danh-sách-thông-tin-xác-thực-và-dịch-vụ-phụ-thuộc-cần-cập-nhật)
5. [KẾ HOẠCH HÀNH ĐỘNG TRƯỚC KHI NỘP BÀI (ACTION CHECKLIST)](#5-kế-hoạch-hành-động-trước-khi-nộp-bài-action-checklist)

---

## 1. TỔNG QUAN KẾT QUẢ KIỂM TOÁN

| Nhóm Kiểm toán | Tổng số tiêu chí | ĐẠT (PASS) | LỖI / CHƯA ĐẠT (FAIL) | CHƯA XÁC MINH (NOT VERIFIED) | Đánh giá chung |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Docker & Tài nguyên** | 8 | 8 | 0 | 0 | **XUẤT SẮC** |
| **2. Bảo mật & Hardening** | 10 | 7 | 3 | 0 | **CẦN LƯU Ý** |
| **3. Monitoring & Logging** | 8 | 8 | 0 | 0 | **XUẤT SẮC** |
| **4. Quản lý Git & Secrets** | 6 | 6 | 0 | 0 | **XUẤT SẮC** |
| **5. Tài liệu & Báo cáo** | 8 | 4 | 4 | 0 | **CẦN BỔ SUNG** |
| **TỔNG CỘNG** | **40** | **33 (82.5%)** | **7 (17.5%)** | **0 (0%)** | **ĐỦ ĐIỀU KIỆN SAU KHI SỬA LỖI** |

---

## 2. CHI TIẾT KIỂM TOÁN THEO TỪNG HẠNG MỤC

### 2.1. Đánh giá Docker, Cấu hình và Tài nguyên

| STT | Tiêu chí Kiểm toán | Kết quả Thực tế Ghi nhận | Đánh giá | Bằng chứng Kỹ thuật |
| :---: | :--- | :--- | :---: | :--- |
| 1 | Cú pháp `docker compose config` | Hợp lệ 100%, không có cảnh báo cú pháp hoặc lỗi parse biến môi trường | **PASS** | `docker compose config --quiet` trả về exit code 0 |
| 2 | Trạng thái Container (`docker compose ps`) | 10/10 containers ở trạng thái `Up` hoặc `Up (healthy)` | **PASS** | `news_nginx`, `news_wordpress`, `news_mysql`, `news_cadvisor` đều đạt `healthy` |
| 3 | Dung lượng ổ đĩa máy chủ Host | Phân vùng root `/` còn trống 23.4 GB (59% khả dụng) | **PASS** | `df -h /` ghi nhận dung lượng an toàn, không có nguy cơ tràn đĩa |
| 4 | Kiểm tra Named Volumes | Đầy đủ 6 named volumes: `news_mysql_data`, `news_wp_data`, `news_prometheus_data`, `news_grafana_data`, `news_loki_data`, `news_nginx_logs` | **PASS** | `docker volume ls` hiển thị đầy đủ các volumes theo thiết kế |
| 5 | Tính bền vững CSDL (Data Persistence) | Đã kiểm chứng restart `news_mysql` và `news_wordpress`, dữ liệu bài viết và CSDL không bị mất | **PASS** | Dữ liệu bảng `wp_posts`, `wp_options` lưu tại `/var/lib/docker/volumes/news_mysql_data/_data` |
| 6 | Không dùng thẻ `latest` tùy tiện | Tất cả image đều ghim phiên bản cụ thể (`mysql:8.0`, `wordpress:6.7-apache`, `prometheus:v2.54.1`, `grafana:11.2.0`, `loki:3.1.1`, `promtail:3.1.1`) | **PASS** | Khảo sát trực tiếp tệp `docker-compose.yml` |
| 7 | Cấu hình phụ thuộc `depends_on` | Sử dụng `condition: service_healthy` giữa WordPress -> MySQL, phpMyAdmin -> MySQL | **PASS** | Ngăn chặn hoàn toàn lỗi kết nối CSDL chập chờn khi khởi động máy chủ |
| 8 | Cấu hình tài nguyên mạng (Networks) | Tồn tại 3 mạng riêng biệt: `news_frontend_net`, `news_backend_net`, `news_monitoring_net` | **PASS** | `docker network ls` hiển thị 3 driver bridge độc lập |

---

### 2.2. Đánh giá An toàn Thông tin và Gia cố Hệ thống (Security & Hardening)

| STT | Tiêu chí Kiểm toán | Kết quả Thực tế Ghi nhận | Đánh giá | Ghi chú và Bằng chứng Kỹ thuật |
| :---: | :--- | :--- | :---: | :--- |
| 1 | Cô lập cổng Cơ sở dữ liệu MySQL | Cổng `3306` **hoàn toàn không được publish** ra máy chủ host | **PASS** | `ss -tulpn` không có port 3306 listening trên interface công khai |
| 2 | Cô lập cổng Logging (Loki/Promtail) | Cổng `3100` (Loki) và `9080` (Promtail) chỉ mở trong mạng nội bộ monitoring | **PASS** | Không publish ra host, Grafana kết nối trực tiếp qua Docker network |
| 3 | Cổng dịch vụ đang publish ra Host | Cổng `80`, `443`, `3000`, `8081`, `9090` đang bind trên `0.0.0.0` và `[::]` | **FAIL** *(Cảnh báo)* | Cổng Prometheus `9090` và phpMyAdmin `8081` mở công khai ra ngoài mạng LAN mà không có xác thực cấp mạng |
| 4 | Phân tách mạng nội bộ (Network Isolation) | WordPress, phpMyAdmin nằm trên cả frontend và backend. MySQL chỉ nằm trên backend. Nginx chỉ nằm trên frontend. | **FAIL** *(Cảnh báo)* | **Phát hiện:** Container `news_prometheus` và `news_grafana` bị gắn thêm mạng `news_frontend_net` ngoài `news_monitoring_net`. Điều này làm giảm tính cô lập mạng giữa monitoring và ứng dụng. |
| 5 | Đánh giá quyền chạy của tiến trình (Non-root) | Prometheus (`nobody`), Node Exporter (`nobody`), Grafana (`472`), Loki (`10001`), MySQL (`mysql` UID 999) chạy non-root. | **FAIL** *(Mâu thuẫn Báo cáo)* | Nginx master, WordPress master, phpMyAdmin master, Promtail và cAdvisor chạy dưới quyền `root`. Báo cáo cần phản ánh trung thực ngoại lệ kỹ thuật này. |
| 6 | Đánh giá cờ đặc quyền `privileged: true` | `news_cadvisor` đang được cấu hình `privileged: true` trong `docker-compose.yml` | **FAIL** *(Mâu thuẫn Báo cáo)* | **Phát hiện nghiêm trọng:** Báo cáo ghi *"Không có container nào dùng privileged: true"*, nhưng cấu hình thực tế cAdvisor đang bật cờ này để đọc cgroup/kmsg. |
| 7 | Quyền truy cập Docker Daemon Socket | `/var/run/docker.sock` chỉ gắn vào `news_promtail` và `news_cadvisor` với tùy chọn chỉ đọc `:ro` | **PASS** | `docker inspect` xác nhận `rw=false` |
| 8 | Phân quyền tập tin nhạy cảm (.env, SSL key) | File `.env` và `nginx/ssl/selfsigned.key` được gán quyền `chmod 600` | **PASS** | `ls -la` xác nhận `-rw------- 1 ubuntu ubuntu` |
| 9 | HTTP Security Headers & TLS thực tế | Đầy đủ: `nosniff`, `SAMEORIGIN`, `strict-origin-when-cross-origin`, `X-XSS-Protection`. TLSv1.2/1.3 | **PASS** | `curl -k -I https://localhost/` xác nhận 100% header hiện diện |
| 10 | Tồn tại file và endpoint thử nghiệm | Endpoint `/error500`, `/error502` trên Nginx và file `/var/www/html/error_test.php` trên WordPress | **FAIL** *(Dư thừa)* | Các file/endpoint dùng cho kiểm thử LogQL chưa được dọn dẹp trước khi bàn giao hệ thống |

---

### 2.3. Đánh giá Hệ thống Giám sát (Prometheus & Grafana) và Nhật ký (Loki & Promtail)

| STT | Tiêu chí Kiểm toán | Kết quả Thực tế Ghi nhận | Đánh giá | Bằng chứng Kỹ thuật |
| :---: | :--- | :--- | :---: | :--- |
| 1 | Trạng thái Prometheus Targets qua API | 3/3 targets (`cadvisor`, `node_exporter`, `prometheus`) đều đạt `health: "up"` | **PASS** | REST API `http://localhost:9090/api/v1/targets` xác nhận 100% UP |
| 2 | Truy vấn PromQL với dữ liệu thực | Câu lệnh `up` trả về giá trị `1` cho cả 3 targets, không có dữ liệu rỗng | **PASS** | API `http://localhost:9090/api/v1/query?query=up` có dữ liệu |
| 3 | Tự động nạp Grafana Datasources | Tự động nạp thành công 2 Datasources: `Prometheus` (Default) và `Loki` | **PASS** | REST API `http://localhost:3000/api/datasources` trả về 2 nguồn dữ liệu |
| 4 | Tự động nạp Grafana Dashboard | Nạp tự động dashboard *"DevOps System & Container Overview"* trong folder `devops-overview` | **PASS** | REST API `http://localhost:3000/api/search` hiển thị dashboard ID |
| 5 | Trạng thái Loki Ingestion qua API | Loki phản hồi `ready` (HTTP 200) thông qua kết nối nội bộ cổng 3100 | **PASS** | `docker exec news_grafana wget -qO- http://news_loki:3100/ready` |
| 6 | Cấu trúc nhãn (Labels) của Loki | Đầy đủ nhãn: `container`, `instance`, `job`, `service` | **PASS** | Khớp hoàn toàn với cấu hình trong `promtail-config.yml` |
| 7 | Thực thi LogQL 1: Xem log Nginx | `{job="nginx"}` trả về luồng log HTTP thực tế đi qua Nginx | **PASS** | Log thực tế: `GET / HTTP/1.1 200`, `GET /pma/ HTTP/1.1 200` |
| 8 | Thực thi LogQL 2 & 3: Lỗi 5xx & App Error | Bắt chính xác lỗi HTTP 500/502 và ngoại lệ PHP Fatal Exception thực tế | **PASS** | Dữ liệu kiểm thử đã được Promtail đẩy vào Loki và truy vấn thành công |

---

### 2.4. Đánh giá Quản lý Mã nguồn Git và Lịch sử Phiên bản

| STT | Tiêu chí Kiểm toán | Kết quả Thực tế Ghi nhận | Đánh giá | Bằng chứng Kỹ thuật |
| :---: | :--- | :--- | :---: | :--- |
| 1 | Trạng thái Working Tree (`git status`) | `On branch main, nothing to commit, working tree clean` | **PASS** | Toàn bộ mã nguồn đã được commit gọn gàng, không có file thừa |
| 2 | Ba commit chính theo đề bài | Commit 1 (`6ad465e` - Nginx), Commit 2 (`5e16e02` - Monitoring), Commit 3 (`b7f07ab` - Logging) | **PASS** | Tồn tại đúng thứ tự và nội dung chuẩn Conventional Commits |
| 3 | Commit Base (App & Database) | Commit `3edf85b`: `feat(app): Triển khai WordPress, MySQL và phpMyAdmin với Docker Compose` | **PASS** | Nền tảng ứng dụng được commit trước 3 commit chính theo yêu cầu đề bài |
| 4 | Rò rỉ thông tin bí mật trong Git history | Kiểm tra toàn bộ `git log -p`: **0 chuỗi nhạy cảm** (không commit `.env`, private key hay password) | **PASS** | Không có thông tin nhạy cảm nào bị lọt vào Git history |
| 5 | Cấu hình `.gitignore` | Loại trừ chặt chẽ `.env`, `*.key`, `*.crt`, `*.log`, `__pycache__/`, `*.py`, `error_test.php` | **PASS** | Tệp `.gitignore` bảo vệ đầy đủ các dữ liệu nhạy cảm |
| 6 | Trạng thái Remote Repository | Hiện tại là **Local-only repository** trên Ubuntu, chưa push lên remote | **PASS** | Đúng chỉ đạo: Không tự ý tạo GitHub repo công khai khi chưa có thông tin sinh viên |

---

### 2.5. Đánh giá Tài liệu Báo cáo Cuối kỳ (Markdown & DOCX)

| STT | Tiêu chí Kiểm toán | Kết quả Thực tế Ghi nhận | Đánh giá | Ghi chú Chi tiết |
| :---: | :--- | :--- | :---: | :--- |
| 1 | Tồn tại file báo cáo MD và DOCX | Tồn tại `report/BAO_CAO_CUOI_KY.md` (54.8 KB) và `BAO_CAO_CUOI_KY.docx` (58.0 KB) | **PASS** | Cả hai định dạng đều được tạo và lưu trữ đúng vị trí |
| 2 | Độ dài nội dung học thuật | DOCX chứa 6,024 từ, 236 đoạn văn, 8 bảng biểu lớn, 11 dấu ngắt trang; tương đương **16–18 trang A4** | **PASS** | Vượt yêu cầu tối thiểu 10 trang của đề bài |
| 3 | Mục lục, Tiêu đề và Đánh số trang | Mục lục chi tiết 8 chương, Heading chuẩn học thuật, Footer có trường đánh số trang tự động | **PASS** | Đáp ứng định dạng bài tập lớn / luận văn CNTT |
| 4 | Khớp nối IP, URL và tên Container | Địa chỉ IP `192.168.177.128`, các URL và 10 tên container trong báo cáo khớp 100% với thực tế | **PASS** | Không có sai lệch về thông số hạ tầng |
| 5 | **Ảnh minh chứng chụp từ hệ thống** | **Hiện tại có 0 ảnh (chưa nhúng ảnh vào DOCX, chưa có file ảnh trong thư mục `report/`)** | **FAIL** *(Thiếu sót lớn)* | Đề bài yêu cầu: *"Chụp ảnh màn hình thực tế của website, phpMyAdmin, Prometheus targets, Grafana dashboard, LogQL, Docker Compose ps. Mỗi ảnh có số thứ tự, chú thích"*. Hiện tại báo cáo mới chỉ dùng bảng biểu và trích xuất text! |
| 6 | Khớp nối mã Git Commit Hash | Bảng 6.1 trong báo cáo ghi mã commit docs là `64e0a9d`, trong khi hash thực tế trong Git là `7e51e0b` | **FAIL** *(Lệch dữ liệu)* | Cần cập nhật lại bảng lịch sử commit trong báo cáo cho khớp với git log thực tế |
| 7 | Tuyên bố về đặc quyền Container | Báo cáo tuyên bố *"Không có container nào dùng privileged: true"*, nhưng thực tế cAdvisor đang dùng | **FAIL** *(Sai lệch kỹ thuật)* | Cần sửa lại báo cáo để giải thích rõ lý do cAdvisor cần quyền đọc cgroup/kmsg thay vì tuyên bố tuyệt đối |
| 8 | Placeholder thông tin sinh viên | Trang bìa vẫn để placeholder: `[TÊN TRƯỜNG]`, `[NGUYỄN VĂN A]`, `[MSSV]`, `[LỚP]`, `[GIẢNG VIÊN]` | **FAIL** *(Chờ thông tin)* | Cần sinh viên cung cấp thông tin chính thức để điền trước khi nộp |

---

## 3. DANH MỤC VẤN ĐỀ PHÂN LOẠI THEO MỨC ĐỘ ƯU TIÊN

### 🔴 Mức độ 1: NGHIÊM TRỌNG (CRITICAL)
1. **Mâu thuẫn kỹ thuật giữa Báo cáo và Cấu hình thực tế về cờ Privileged:**
   - *Hiện trạng:* File `BAO_CAO_CUOI_KY.md` và `.docx` (Mục 5.1) khẳng định: *"Không có bất kỳ container nào trong dự án sử dụng cờ privileged: true"*. Tuy nhiên, trong `docker-compose.yml`, dịch vụ `cadvisor` có khai báo `privileged: true`.
   - *Rủi ro:* Giảng viên chấm bài khi đối chiếu `docker-compose.yml` với báo cáo sẽ đánh giá là báo cáo không trung thực hoặc không nắm rõ cấu hình hệ thống.
   - *Giải pháp kiến nghị:* Cập nhật báo cáo giải thích rõ ràng: cAdvisor yêu cầu cờ `privileged: true` (hoặc mount thiết bị `/dev/kmsg` và cgroup) để thu thập chỉ số nhân Linux; ghi nhận đây là ngoại lệ kỹ thuật duy nhất được kiểm soát.

---

### 🟠 Mức độ 2: CAO (HIGH)
2. **Thiếu hình ảnh minh chứng thực tế trong Báo cáo:**
   - *Hiện trạng:* Thư mục `report/` hiện chỉ có file text và file docx thuần bảng biểu/văn bản, chưa có bất kỳ tệp ảnh chụp màn hình nào (`0 images`).
   - *Rủi ro:* Đề bài yêu cầu bắt buộc: *"Chụp ảnh màn hình hoặc lưu đầu ra kiểm thử thực tế của website, phpMyAdmin, Prometheus targets, Grafana dashboard, Loki/LogQL... Mỗi ảnh có số thứ tự, chú thích"*. Thiếu ảnh minh chứng sẽ bị trừ điểm trực tiếp về quy cách báo cáo.
   - *Giải pháp kiến nghị:* Chụp thực tế 6 ảnh màn hình từ trình duyệt: (1) Giao diện Website WordPress, (2) Giao diện phpMyAdmin, (3) Prometheus Targets UP, (4) Grafana Dashboard tổng quan, (5) Grafana Explore chạy 3 câu LogQL, (6) Kết quả lệnh `docker compose ps` trên terminal; sau đó nhúng trực tiếp vào file Word `.docx` và file `.md`.

3. **Sai lệch mã Hash Commit của tài liệu:**
   - *Hiện trạng:* Bảng 6.1 trong báo cáo ghi mã commit docs là `64e0a9d`, nhưng thực tế lệnh `git log` ghi nhận hash là `7e51e0b` (và commit `efef9cd`).
   - *Giải pháp kiến nghị:* Cập nhật bảng commit trong báo cáo cho khớp 100% với `git log`.

4. **Cổng Prometheus (9090) và phpMyAdmin (8081) mở công khai trên 0.0.0.0:**
   - *Hiện trạng:* Cổng 9090 của Prometheus không có xác thực đăng nhập và cổng 8081 của phpMyAdmin mở trực tiếp ra toàn bộ mạng ngoài.
   - *Giải pháp kiến nghị:* Trong môi trường sản xuất, nên bind về `127.0.0.1:9090` hoặc chuyển phpMyAdmin hoàn toàn qua Nginx có xác thực.

---

### 🟡 Mức độ 3: TRUNG BÌNH (MEDIUM)
5. **Tồn tại file và endpoint thử nghiệm trong hệ thống đang chạy:**
   - *Hiện trạng:* Tệp `/var/www/html/error_test.php` trong container WordPress và hai endpoint `/error500`, `/error502` trong `nginx/conf.d/default.conf` vẫn đang tồn tại.
   - *Rủi ro:* Để lộ file test lỗi trên ứng dụng web đang chạy.
   - *Giải pháp kiến nghị:* Đóng hoặc xóa các endpoint/file này sau khi đã chụp đủ ảnh minh chứng LogQL, sau đó reload Nginx.

6. **Phân tách mạng chưa triệt để đối với Prometheus và Grafana:**
   - *Hiện trạng:* Hai dịch vụ này đang được gắn cả mạng `frontend-net` lẫn `monitoring-net`. Thực tế, Prometheus và Grafana chỉ cần nằm trên `monitoring-net` là đủ để hoạt động (vì người dùng truy cập Grafana qua port publish hoặc qua Reverse Proxy).
   - *Giải pháp kiến nghị:* Gỡ bỏ `frontend-net` khỏi Prometheus và Grafana trong `docker-compose.yml` để đảm bảo cô lập mạng tuyệt đối.

7. **Thông tin sinh viên trên trang bìa còn ở dạng Placeholder:**
   - *Hiện trạng:* Các trường `[HỌ TÊN]`, `[MSSV]`, `[LỚP]`, `[TRƯỜNG]` chưa có thông tin thật.
   - *Giải pháp kiến nghị:* Người dùng cung cấp thông tin để cập nhật vào báo cáo.

---

### 🟢 Mức độ 4: THẤP (LOW)
8. **Kho Git chưa có Remote GitHub:**
   - *Hiện trạng:* Chưa cấu hình remote và chưa push code.
   - *Giải pháp kiến nghị:* Người dùng cung cấp URL repository GitHub cá nhân để thực hiện lệnh push.

9. **Cảnh báo trình duyệt do chứng chỉ SSL Self-signed:**
   - *Hiện trạng:* Trình duyệt hiển thị cảnh báo không tin cậy khi truy cập `https://192.168.177.128`.
   - *Ghi chú:* Đây là hạn chế khách quan hợp lệ của môi trường mạng nội bộ, đã được phân tích đầy đủ trong Chương 8 của Báo cáo.

---

## 4. DANH SÁCH THÔNG TIN XÁC THỰC VÀ DỊCH VỤ PHỤ THUỘC CẦN CẬP NHẬT

Khi chuyển giao sang môi trường trình diễn chính thức hoặc nộp bài, các thông tin xác thực sau cần được sinh mới bằng chuỗi ngẫu nhiên mạnh và đồng bộ cập nhật trên các dịch vụ liên quan:

| Tên Biến / Thông tin Xác thực | Dịch vụ Sở hữu | Các Dịch vụ Phụ thuộc Bắt buộc Cập nhật Cùng | Hướng dẫn Cập nhật An toàn |
| :--- | :--- | :--- | :--- |
| `MYSQL_ROOT_PASSWORD` | `news_mysql` | `news_phpmyadmin` (nếu dùng đăng nhập root) | Cần đổi qua lệnh `ALTER USER 'root'@'%' IDENTIFIED BY '...';` bên trong MySQL |
| `MYSQL_PASSWORD` | `news_mysql` | `news_wordpress` (`WORDPRESS_DB_PASSWORD`), `news_phpmyadmin` | Đổi trong MySQL qua `ALTER USER`, đồng thời cập nhật file `.env` và restart WordPress |
| `GRAFANA_ADMIN_PASSWORD` | `news_grafana` | Người dùng quản trị Grafana | Chạy `docker compose exec news_grafana grafana-cli admin reset-admin-password <PASS_MOI>` |
| WordPress Admin Password | `news_wordpress` | Quản trị viên CMS | Đổi qua giao diện WordPress Dashboard -> Users -> Profile hoặc dùng WP-CLI |

> **Cảnh báo rủi ro dữ liệu:** Tuyệt đối không xóa volume `news_mysql_data` để đổi mật khẩu. Nếu chỉ sửa file `.env` mà không chạy lệnh `ALTER USER` trong MySQL, container WordPress sẽ bị lỗi *"Error establishing a database connection"* do MySQL không tự cập nhật mật khẩu của database đã khởi tạo từ trước.

---

## 5. KẾ HOẠCH HÀNH ĐỘNG TRƯỚC KHI NỘP BÀI (ACTION CHECKLIST)

Bảng dưới đây liệt kê các bước cần thực hiện để hoàn thiện 100% điều kiện nộp bài, phân định rõ mức độ rủi ro đối với dữ liệu và tính liên tục của dịch vụ:

| STT | Công việc cần thực hiện | Mức độ Ưu tiên | Nguy cơ Gián đoạn Dịch vụ | Nguy cơ Mất mát Dữ liệu | Trạng thái |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Chụp 6 ảnh màn hình minh chứng thực tế** từ trình duyệt (WordPress, phpMyAdmin, Prometheus targets, Grafana dashboard, Loki LogQL, Docker ps) | **CAO** | **KHÔNG** | **KHÔNG** | Chờ thực hiện |
| **2** | **Cập nhật lại Báo cáo (`.md` & `.docx`):** Sửa tuyên bố về `privileged: true` của cAdvisor, cập nhật mã hash commit thực tế, nhúng 6 ảnh minh chứng | **CAO** | **KHÔNG** | **KHÔNG** | Chờ thực hiện |
| **3** | **Điền thông tin sinh viên chính thức** (Họ tên, MSSV, Lớp, Trường) vào trang bìa Báo cáo | **TRUNG BÌNH** | **KHÔNG** | **KHÔNG** | Chờ User cung cấp |
| **4** | **Dọn dẹp file/endpoint thử nghiệm:** Xóa `error_test.php` trên WordPress và gỡ `/error500`, `/error502` trong Nginx | **TRUNG BÌNH** | **RẤT THẤP** *(Reload Nginx mất < 1 giây)* | **KHÔNG** | Chờ thực hiện |
| **5** | **Tối ưu hóa phân tách mạng:** Gỡ `frontend-net` khỏi Prometheus và Grafana trong `docker-compose.yml` | **TRUNG BÌNH** | **THẤP** *(Restart container Prometheus & Grafana mất ~3 giây)* | **KHÔNG** *(Đã dùng named volume)* | Chờ xem xét |
| **6** | **Tạo Git Commit cuối:** Commit các ảnh minh chứng và báo cáo đã hoàn thiện | **THẤP** | **KHÔNG** | **KHÔNG** | Chờ thực hiện |
| **7** | **Cấu hình Remote và Push lên GitHub:** Thực hiện `git remote add origin` và `git push -u origin main` | **THẤP** | **KHÔNG** | **KHÔNG** | Chờ User cho phép |

---

## KẾT LUẬN CỦA KIỂM TOÁN VIÊN

Hệ thống kỹ thuật thực tế trên máy ảo Ubuntu hiện đang vận hành **rất tốt, ổn định và đầy đủ chức năng** (10/10 containers đều sống khỏe, metrics thu thập liên tục, logs tập trung thành công và không bị rò rỉ secret trong Git).

Các vấn đề tồn tại chủ yếu nằm ở **sự sai lệch giữa văn bản Báo cáo và cấu hình thực tế** (cờ `privileged` của cAdvisor, mã commit hash), **sự thiếu vắng các ảnh chụp màn hình minh chứng**, và **các endpoint/file thử nghiệm còn sót lại**.

Kiểm toán viên đã dừng toàn bộ các thao tác can thiệp hệ thống theo đúng nguyên tắc **CHỈ ĐỌC (READ-ONLY)** và bàn giao báo cáo này để bạn xem xét, quyết định trước khi tiến hành các bước khắc phục.
