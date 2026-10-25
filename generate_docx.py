# -*- coding: utf-8 -*-
"""
Script tao file Bao cao hoc thuat cuoi ky (BAO_CAO_CUOI_KY.docx)
su dung thu vien python-docx voi chuan dinh dang luan van/do an CNTT.
Tich hop 6 anh chup man hinh thuc te tu he thong.
"""
import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_page_number(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def create_report_docx(output_path):
    doc = Document()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, "report", "images")

    # 1. Thiet lap le trang chuan luan van Viet Nam (Top 2cm, Bottom 2cm, Left 3cm, Right 2cm)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)

    # Thiet lap Footer
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("Trang ")
    f_run.font.name = "Times New Roman"
    f_run.font.size = Pt(10)
    f_run.font.color.rgb = RGBColor(120, 120, 120)
    add_page_number(f_run)

    # Mau chu dao
    COLOR_PRIMARY = RGBColor(16, 44, 87)       # Navy #102C57
    COLOR_SECONDARY = RGBColor(30, 80, 140)    # Blue #1E508C
    COLOR_TEXT = RGBColor(33, 37, 41)          # Dark text #212529
    COLOR_MUTED = RGBColor(100, 110, 120)      # Gray

    # ========================== TRANG BIA ==========================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r_inst1.font.name = "Times New Roman"
    r_inst1.font.size = Pt(12)
    r_inst1.font.bold = True
    
    r_inst2 = p_inst.add_run("TRƯỜNG ĐẠI HỌC [TÊN TRƯỜNG - PLACEHOLDER]\n")
    r_inst2.font.name = "Times New Roman"
    r_inst2.font.size = Pt(13)
    r_inst2.font.bold = True
    r_inst2.font.color.rgb = COLOR_PRIMARY

    r_inst3 = p_inst.add_run("KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN MẠNG & HỆ THỐNG\n")
    r_inst3.font.name = "Times New Roman"
    r_inst3.font.size = Pt(11)
    r_inst3.font.bold = True
    r_inst3.font.color.rgb = COLOR_MUTED

    r_line = p_inst.add_run("----------------------------------------------------------------------\n\n\n")
    r_line.font.name = "Times New Roman"
    r_line.font.size = Pt(11)
    r_line.font.color.rgb = COLOR_MUTED

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep = p_title.add_run("BÁO CÁO BÀI TẬP CUỐI KỲ\n")
    r_rep.font.name = "Times New Roman"
    r_rep.font.size = Pt(16)
    r_rep.font.bold = True
    r_rep.font.color.rgb = COLOR_MUTED

    r_subj = p_title.add_run("HỌC PHẦN: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM\n\n")
    r_subj.font.name = "Times New Roman"
    r_subj.font.size = Pt(15)
    r_subj.font.bold = True
    r_subj.font.color.rgb = COLOR_PRIMARY

    r_topic_pre = p_title.add_run("ĐỀ TÀI:\n")
    r_topic_pre.font.name = "Times New Roman"
    r_topic_pre.font.size = Pt(13)
    r_topic_pre.font.bold = True

    r_topic = p_title.add_run("THIẾT KẾ, TRIỂN KHAI VÀ VẬN HÀNH HỆ THỐNG CỔNG THÔNG TIN TIN TỨC TRÊN NỀN TẢNG CONTAINER VỚI DOCKER COMPOSE, NGINX REVERSE PROXY, PROMETHEUS, GRAFANA, LOKI VÀ PROMTAIL\n\n\n\n")
    r_topic.font.name = "Times New Roman"
    r_topic.font.size = Pt(16)
    r_topic.font.bold = True
    r_topic.font.color.rgb = COLOR_PRIMARY

    t_meta = doc.add_table(rows=5, cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Sinh viên thực hiện:", "[NGUYỄN VĂN A - PLACEHOLDER]"),
        ("Mã số sinh viên (MSSV):", "[MSSV_PLACEHOLDER]"),
        ("Lớp / Khóa đào tạo:", "[LỚP_PLACEHOLDER]"),
        ("Giảng viên hướng dẫn:", "[GIẢNG VIÊN HƯỚNG DẪN PLACEHOLDER]"),
        ("Học kỳ / Niên khóa:", "Học kỳ 1 - Năm 2026")
    ]
    for idx, (label, val) in enumerate(meta_info):
        row = t_meta.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Cm(6.0), Cm(10.0)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.3
        p1.paragraph_format.line_spacing = 1.3
        r0 = p0.add_run(label)
        r0.font.name, r0.font.size, r0.font.bold = "Times New Roman", Pt(12), True
        r1 = p1.add_run(val)
        r1.font.name, r1.font.size, r1.font.color.rgb = "Times New Roman", Pt(12), COLOR_TEXT

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_loc = p_bottom.add_run("\n\n\n\n\nHÀ NỘI, NĂM 2026")
    r_loc.font.name, r_loc.font.size, r_loc.font.bold = "Times New Roman", Pt(12), True

    doc.add_page_break()

    # ========================== HELPER FUNCTIONS ==========================
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(15), True
        r.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(13.5), True
        r.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name, r.font.size, r.font.bold, r.font.italic = "Times New Roman", Pt(12.5), True, True
        r.font.color.rgb = COLOR_TEXT
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(6)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name, r_pre.font.size, r_pre.font.bold = "Times New Roman", Pt(12), True
        r = p.add_run(text)
        r.font.name, r.font.size, r.font.color.rgb = "Times New Roman", Pt(12), COLOR_TEXT
        return p

    def add_code(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Cm(0.5)
        r = p.add_run(text)
        r.font.name, r.font.size = "Consolas", Pt(9.5)
        r.font.color.rgb = RGBColor(20, 30, 40)
        return p

    def add_figure(img_filename, caption, explanation, width_cm=15.0):
        img_full_path = os.path.join(img_dir, img_filename)
        if os.path.exists(img_full_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            run_img = p_img.add_run()
            run_img.add_picture(img_full_path, width=Cm(width_cm))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(6)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name, r_cap.font.size = "Times New Roman", Pt(11)
            r_cap.font.bold, r_cap.font.italic = True, True
            r_cap.font.color.rgb = COLOR_PRIMARY

            p_exp = doc.add_paragraph()
            p_exp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_exp.paragraph_format.line_spacing = 1.3
            p_exp.paragraph_format.space_after = Pt(8)
            r_exp = p_exp.add_run(explanation)
            r_exp.font.name, r_exp.font.size = "Times New Roman", Pt(11.5)
            r_exp.font.color.rgb = COLOR_TEXT
        else:
            print(f"[WARN] Image not found: {img_full_path}")

    def add_table_data(headers, data, col_widths=None):
        t = doc.add_table(rows=len(data) + 1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_row = t.rows[0]
        for col_idx, h_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            set_cell_background(cell, "102C57")
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h_text)
            r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(11), True
            r.font.color.rgb = RGBColor(255, 255, 255)
            if col_widths and col_idx < len(col_widths):
                cell.width = Cm(col_widths[col_idx])
        for r_idx, row_vals in enumerate(data):
            row = t.rows[r_idx + 1]
            bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
            for col_idx, val in enumerate(row_vals):
                cell = row.cells[col_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.2
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(str(val))
                r.font.name, r.font.size = "Times New Roman", Pt(10.5)
                r.font.color.rgb = COLOR_TEXT
                if col_widths and col_idx < len(col_widths):
                    cell.width = Cm(col_widths[col_idx])
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(6)

    # ========================== MUC LUC TONG QUAN ==========================
    add_h1("MỤC LỤC TỔNG QUAN")
    toc_items = [
        "CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG",
        "  1.1. Bối cảnh và mục tiêu kỹ thuật",
        "  1.2. Phân tích yêu cầu hệ thống và ngăn xếp công nghệ",
        "  1.3. Mô hình kiến trúc phân tầng tổng thể",
        "  1.4. Thiết kế phân vùng mạng Docker và cô lập dịch vụ",
        "  1.5. Thiết kế cơ chế lưu trữ dữ liệu bền vững",
        "CHƯƠNG 2: TRIỂN KHAI CỔNG THÔNG TIN, CƠ SỞ DỮ LIỆU VÀ NGINX REVERSE PROXY",
        "  2.1. Triển khai ứng dụng Web WordPress",
        "  2.2. Triển khai Hệ quản trị Cơ sở dữ liệu MySQL 8.0",
        "  2.3. Triển khai Công cụ Quản trị CSDL trực quan phpMyAdmin",
        "  2.4. Cấu hình Nginx Reverse Proxy và SSL/TLS Offloading",
        "  2.5. Cấu hình các tiêu chuẩn An toàn HTTP (Security Headers)",
        "  2.6. Xử lý đường dẫn và tham số Proxy Header cho WordPress",
        "CHƯƠNG 3: HỆ THỐNG GIÁM SÁT HIỆU NĂNG VỚI PROMETHEUS VÀ GRAFANA",
        "  3.1. Tổng quan mô hình giám sát Pull-based Metrics",
        "  3.2. Thu thập chỉ số tài nguyên Host với Node Exporter",
        "  3.3. Thu thập chỉ số hiệu năng Container với cAdvisor",
        "  3.4. Cấu hình Prometheus Scrape Targets và chu kỳ thu thập",
        "  3.5. Trực quan hóa dữ liệu với Grafana và Provisioning tự động",
        "CHƯƠNG 4: HỆ THỐNG THU THẬP VÀ PHÂN TÍCH NHẬT KÝ (LOGS) VỚI LOKI VÀ PROMTAIL",
        "  4.1. Kiến trúc hệ thống tập trung nhật ký với Grafana Loki",
        "  4.2. Promtail Log Shipper: Cơ chế quét Docker Socket và Nginx Log Volume",
        "  4.3. Thiết kế hệ thống nhãn (Labels) khoa học, tối ưu hiệu năng",
        "  4.4. Tích hợp Loki Datasource vào Grafana",
        "  4.5. Phân tích 3 kịch bản truy vấn LogQL thực tế và kết quả kiểm thử",
        "CHƯƠNG 5: ĐÁNH GIÁ AN TOÀN THÔNG TIN VÀ GIA CỐ HỆ THỐNG (SYSTEM HARDENING)",
        "  5.1. Áp dụng nguyên tắc đặc quyền tối thiểu (Least Privilege)",
        "  5.2. Kiểm soát bề mặt tấn công: Giới hạn Port Exposure",
        "  5.3. Quản lý bí mật (Secrets Management) và bảo vệ file cấu hình",
        "  5.4. Đánh giá trạng thái Tường lửa Host OS (UFW/Iptables)",
        "  5.5. Thiết lập cơ chế kiểm tra sức khỏe tự động (Docker Healthchecks)",
        "CHƯƠNG 6: QUY TRÌNH QUẢN LÝ MÃ NGUỒN GIT VÀ LỊCH SỬ PHIÊN BẢN",
        "  6.1. Cấu trúc kho mã nguồn và loại trừ rò rỉ dữ liệu qua .gitignore",
        "  6.2. Quy chuẩn thông điệp Commit (Conventional Commits)",
        "  6.3. Chi tiết lịch sử các Commit triển khai thực tế",
        "  6.4. Tài liệu hướng dẫn vận hành hệ thống (README.md)",
        "CHƯƠNG 7: KẾT QUẢ KIỂM THỬ TÍCH HỢP TOÀN DIỆN (INTEGRATION TESTING)",
        "  7.1. Kiểm thử tính toàn vẹn và phản hồi của Ứng dụng Web",
        "  7.2. Kiểm thử Reverse Proxy, chuyển hướng HTTP sang HTTPS và Security Headers",
        "  7.3. Kiểm thử tính bền vững của Cơ sở dữ liệu sau chu kỳ Khởi động lại",
        "  7.4. Kiểm thử trạng thái Targets và Thu thập Metrics của Prometheus",
        "  7.5. Kiểm thử Khả năng Truy vấn Nhật ký Thực tế của Loki",
        "CHƯƠNG 8: HẠN CHẾ THỰC TẾ VÀ HƯỚNG PHÁT TRIỂN",
        "  8.1. Các hạn chế kỹ thuật trong môi trường thử nghiệm",
        "  8.2. Đề xuất kiến trúc mở rộng trong môi trường Doanh nghiệp",
        "KẾT LUẬN VÀ TÀI LIỆU THAM KHẢO"
    ]
    for item in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before, p_toc.paragraph_format.space_after = Pt(1), Pt(2)
        r_toc = p_toc.add_run(item)
        r_toc.font.name, r_toc.font.size = "Times New Roman", Pt(11)
        if item.startswith("CHƯƠNG") or item.startswith("KẾT"):
            r_toc.font.bold, r_toc.font.color.rgb = True, COLOR_PRIMARY
        else:
            r_toc.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # ========================== CHUONG 1 ==========================
    add_h1("CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI VÀ KIẾN TRÚC HỆ THỐNG")
    add_h2("1.1. Bối cảnh và mục tiêu kỹ thuật")
    add_p("Trong bối cảnh chuyển đổi số và xu hướng phát triển ứng dụng đám mây (Cloud-Native), việc triển khai và quản trị một hệ thống phần mềm không còn đơn thuần là việc cài đặt mã nguồn lên một máy chủ vật lý. Đội ngũ kỹ sư hệ thống và DevOps hiện đại phải đối mặt với các thách thức to lớn về tính khả chuyển (portability), tính bảo mật đa tầng (defense-in-depth), khả năng quan sát toàn diện (observability) và tính tự động hóa cao.")
    add_p("Học phần 'Triển khai và Quản trị Hệ thống Phần mềm' đặt ra bài toán xây dựng một hệ thống hoàn chỉnh phục vụ nhu cầu vận hành Cổng thông tin tin tức công nghệ. Hệ thống không chỉ cung cấp nền tảng quản trị nội dung linh hoạt, mà còn phải thiết lập hạ tầng phụ trợ đạt chuẩn công nghiệp bao gồm: Hệ quản trị cơ sở dữ liệu quan hệ, cổng Reverse Proxy bảo mật, hệ thống giám sát chỉ số tài nguyên phần cứng & container thời gian thực, và hệ thống tập trung nhật ký phục vụ điều tra sự cố.")
    add_p("Mục tiêu kỹ thuật cốt lõi của dự án bao gồm:")
    add_p("- Đóng gói và cô lập toàn bộ các dịch vụ bằng công nghệ ảo hóa Container với Docker Engine và Docker Compose v2.", bold_prefix="1. Ảo hóa hoàn chỉnh: ")
    add_p("- Thiết lập Nginx Reverse Proxy làm cổng tiếp nhận duy nhất, cấu hình mã hóa SSL/TLS Offloading và chèn các HTTP Security Headers ngăn chặn tấn công phổ biến.", bold_prefix="2. Bảo mật mạng và truyền thông: ")
    add_p("- Thu thập chỉ số máy chủ và container với Node Exporter, cAdvisor, lưu trữ bằng Prometheus TSDB và hiển thị trên Grafana Dashboard.", bold_prefix="3. Giám sát hiệu năng liên tục: ")
    add_p("- Tập trung toàn bộ luồng logs qua Promtail, lưu trữ bằng Grafana Loki và xây dựng các câu truy vấn LogQL chuyên sâu.", bold_prefix="4. Quản trị nhật ký tập trung: ")
    add_p("- Áp dụng nguyên tắc đặc quyền tối thiểu (Least Privilege), ẩn cổng CSDL, phân tách mạng nội bộ và đảm bảo không mất mát dữ liệu sau chu kỳ khởi động lại.", bold_prefix="5. Gia cố hệ thống và bền vững dữ liệu: ")

    add_h2("1.2. Phân tích yêu cầu hệ thống và ngăn xếp công nghệ (Technology Stack)")
    add_p("Dự án được triển khai trực tiếp trên máy chủ ảo hóa Ubuntu Linux 26.04 LTS (x86_64) với thông số: 4 vCPU, 4.0 GB RAM và 40 GB dung lượng ổ đĩa. Các phiên bản công nghệ được thẩm định nghiêm ngặt nhằm tránh xung đột và đảm bảo tính tương thích lâu dài:")
    
    tech_headers = ["Thành phần", "Image / Phần mềm", "Phiên bản", "Vai trò kiến trúc"]
    tech_data = [
        ["Reverse Proxy & Gateway", "nginx", "1.27-alpine", "Cổng điều phối lưu lượng, kết thúc SSL, bảo mật HTTP"],
        ["Cổng thông tin Web (CMS)", "wordpress", "6.7-apache", "Xử lý nghiệp vụ hiển thị tin tức và quản trị bài viết"],
        ["Cơ sở dữ liệu (RDBMS)", "mysql", "8.0", "Lưu trữ dữ liệu quan hệ với chuẩn ký tự utf8mb4"],
        ["Giao diện quản trị CSDL", "phpmyadmin", "5.2", "Giao diện web tương tác CSDL qua mạng nội bộ"],
        ["Máy chủ thu thập chỉ số", "prom/prometheus", "v2.54.1", "Cơ sở dữ liệu chuỗi thời gian (TSDB) lưu trữ metrics"],
        ["Giám sát phần cứng Host", "prom/node-exporter", "v1.8.2", "Thu thập CPU, RAM, Disk, Network của máy chủ Ubuntu"],
        ["Giám sát tài nguyên Container", "gcr.io/cadvisor/cadvisor", "v0.49.1", "Thu thập chỉ số CPU/RAM thực tế của từng Docker container"],
        ["Trực quan hóa giám sát", "grafana/grafana", "11.2.0", "Bảng điều khiển trực quan thống nhất cho Metrics và Logs"],
        ["Lưu trữ và chỉ mục nhật ký", "grafana/loki", "3.1.1", "Hệ thống tập trung log dựa trên metadata nhãn tối ưu"],
        ["Đại lý thu thập log", "grafana/promtail", "3.1.1", "Đọc luồng log từ Docker Engine socket và đẩy về Loki"]
    ]
    add_table_data(tech_headers, tech_data, [4.0, 3.5, 2.5, 6.0])

    add_h2("1.3. Mô hình kiến trúc phân tầng tổng thể (System Architecture)")
    add_p("Hệ thống áp dụng kiến trúc phân tầng 3 lớp (3-Tier Multi-layer Architecture) kết hợp với trục giám sát độc lập. Mọi luồng giao tiếp từ người dùng bên ngoài đều được chặn ở Lớp Cổng giao tiếp (Gateway Tier). Các tầng bên dưới (Ứng dụng và Cơ sở dữ liệu) chỉ giao tiếp qua mạng ảo nội bộ.")
    add_code(
"""[ Internet / User Client ]
             |
   HTTP :80 (301) / HTTPS :443
             v
+-------------------------+
|   Nginx Reverse Proxy   | <--- SSL Termination & Security Headers
+-------------------------+
      |             |
      | /           | /pma/
      v             v
+-----------+ +-----------+
| WordPress | | phpMyAdmin|
+-----------+ +-----------+
      |             |
      +------+------+
             | :3306 (Internal Only)
             v
      +-------------+
      | MySQL 8.0   | <--- Named Volume: news_mysql_data
      +-------------+
=============================================================
[ Observability Stack ]
Node Exporter (:9100) + cAdvisor (:8080) ---> Prometheus (:9090) ---> Grafana (:3000)
Docker Daemon Socket / Logs              ---> Promtail        ---> Loki (:3100)
"""
    )

    add_h2("1.4. Thiết kế phân vùng mạng Docker và cô lập dịch vụ (Network Segmentation)")
    add_p("Dự án triển khai mô hình cô lập đa tầng với 3 mạng Docker Bridge chuyên biệt:")
    add_p("- 'news_frontend_net': Dành riêng cho giao tiếp hướng ra người dùng, kết nối giữa Nginx Reverse Proxy, WordPress và phpMyAdmin.", bold_prefix="1. Frontend Network: ")
    add_p("- 'news_backend_net': Mạng nội bộ tuyệt mật, chỉ kết nối giữa WordPress, phpMyAdmin và MySQL. Nginx và mạng giám sát hoàn toàn không thể chạm tới mạng này.", bold_prefix="2. Backend Network: ")
    add_p("- 'news_monitoring_net': Mạng chuyên dụng cho luồng thu thập dữ liệu chỉ số và nhật ký giữa Node Exporter, cAdvisor, Prometheus, Loki, Promtail và Grafana.", bold_prefix="3. Monitoring Network: ")

    net_headers = ["Tên Container", "Frontend Net", "Backend Net", "Monitoring Net", "Cổng công khai Host"]
    net_data = [
        ["news_nginx", "KẾT NỐI", "KHÔNG", "KHÔNG", "80, 443 (HTTP/HTTPS)"],
        ["news_wordpress", "KẾT NỐI", "KẾT NỐI", "KHÔNG", "KHÔNG (Bảo vệ sau Proxy)"],
        ["news_mysql", "KHÔNG", "KẾT NỐI", "KHÔNG", "KHÔNG (Tuyệt đối cô lập)"],
        ["news_phpmyadmin", "KẾT NỐI", "KẾT NỐI", "KHÔNG", "8081 (Cổng dự phòng)"],
        ["news_node_exporter", "KHÔNG", "KHÔNG", "KẾT NỐI", "KHÔNG (Nội bộ)"],
        ["news_cadvisor", "KHÔNG", "KHÔNG", "KẾT NỐI", "KHÔNG (Nội bộ)"],
        ["news_prometheus", "KHÔNG", "KHÔNG", "KẾT NỐI", "9090 (Giao diện Metrics)"],
        ["news_grafana", "KHÔNG", "KHÔNG", "KẾT NỐI", "3000 (Giao diện Dashboard)"],
        ["news_loki", "KHÔNG", "KHÔNG", "KẾT NỐI", "KHÔNG (Nội bộ)"],
        ["news_promtail", "KHÔNG", "KHÔNG", "KẾT NỐI", "KHÔNG (Nội bộ)"]
    ]
    add_table_data(net_headers, net_data, [4.0, 3.0, 3.0, 3.0, 3.0])

    add_h2("1.5. Thiết kế cơ chế lưu trữ dữ liệu bền vững (Volume Persistence Strategy)")
    add_p("Theo nguyên lý Container Immutability, dữ liệu ghi vào lớp bộ nhớ tạm thời của container sẽ bị tiêu hủy khi container bị gỡ bỏ. Dự án thiết lập hệ thống Docker Named Volumes độc lập:")
    add_p("- 'news_mysql_data': Gắn kết vào /var/lib/mysql, lưu trữ cấu trúc bảng InnoDB, bản ghi dữ liệu người dùng, bài viết tin tức và tài khoản.", bold_prefix="1. Lưu trữ CSDL: ")
    add_p("- 'news_wp_data': Gắn kết vào /var/www/html, lưu trữ mã nguồn WordPress, tệp cấu hình wp-config.php và thư viện tải lên wp-content/uploads.", bold_prefix="2. Lưu trữ Web: ")
    add_p("- 'news_prometheus_data' & 'news_grafana_data': Đảm bảo lịch sử chỉ số giám sát và các thiết lập tài khoản không bị xóa sổ khi nâng cấp phiên bản.", bold_prefix="3. Lưu trữ Giám sát: ")

    doc.add_page_break()

    # ========================== CHUONG 2 ==========================
    add_h1("CHƯƠNG 2: TRIỂN KHAI CỔNG THÔNG TIN, CƠ SỞ DỮ LIỆU VÀ NGINX REVERSE PROXY")
    add_h2("2.1. Triển khai ứng dụng Web WordPress")
    add_p("Ứng dụng WordPress được khởi tạo bằng Docker Compose với các biến môi trường cấu hình kết nối tự động tới MySQL. Cấu hình PHP được tinh chỉnh bổ sung qua biến WORDPRESS_CONFIG_EXTRA nhằm khắc phục triệt để lỗi Infinite Redirect Loop:")
    add_code(
"""WORDPRESS_CONFIG_EXTRA: |
  if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
      $_SERVER['HTTPS'] = 'on';
  }
"""
    )
    add_p("Hệ thống đã thực hiện khởi tạo sẵn dữ liệu bài viết mẫu cho cổng thông tin công nghệ với các bài viết chuyên sâu về DevOps, Docker và Hệ điều hành Linux.")

    add_h2("2.2. Triển khai Hệ quản trị Cơ sở dữ liệu MySQL 8.0")
    add_p("Dịch vụ MySQL 8.0 được cấu hình với các tham số tối ưu hóa:")
    add_p("- Khởi chạy với cờ '--character-set-server=utf8mb4' và '--collation-server=utf8mb4_unicode_ci' giúp hỗ trợ lưu trữ toàn diện tiếng Việt có dấu.", bold_prefix="Bảng mã ký tự: ")
    add_p("- Cổng 3306 không được public ra ngoài máy chủ host, ngăn chặn hoàn toàn nguy cơ dò quét mật khẩu từ mạng bên ngoài.", bold_prefix="Bảo mật cổng kết nối: ")
    add_p("- Thiết lập cơ chế kiểm tra sức khỏe thông qua lệnh 'mysqladmin ping' định kỳ 10 giây/lần. WordPress được thiết lập phụ thuộc vào MySQL với điều kiện 'condition: service_healthy'.", bold_prefix="Cơ chế Healthcheck: ")

    add_h2("2.3. Triển khai Công cụ Quản trị CSDL trực quan phpMyAdmin")
    add_p("phpMyAdmin được tích hợp giúp việc quản lý bảng, sao lưu và kiểm tra cấu trúc dữ liệu trở nên nhanh chóng. Dịch vụ được truy cập chính thống qua Nginx Reverse Proxy tại địa chỉ 'https://192.168.177.128/pma/', kèm theo cổng phụ 8081 dự phòng nội bộ.")

    add_h2("2.4. Cấu hình Nginx Reverse Proxy và SSL/TLS Offloading")
    add_p("Nginx giữ vai trò là thành phần tiếp nhận duy nhất lưu lượng truy cập mạng từ bên ngoài:")
    add_p("- Khối Server HTTP (Port 80): Tự động chuyển hướng vĩnh viễn (301 Moved Permanently) sang giao thức HTTPS.")
    add_p("- Khối Server HTTPS (Port 443): Thiết lập chứng chỉ mã hóa dữ liệu với giao thức TLS v1.2 và TLS v1.3 hiện đại.")

    add_h2("2.5. Cấu hình các tiêu chuẩn An toàn HTTP (Security Headers)")
    sec_headers = ["Tên HTTP Header", "Giá trị thiết lập", "Tác dụng bảo vệ an ninh"]
    sec_data = [
        ["X-Content-Type-Options", "nosniff", "Vô hiệu hóa tính năng tự động suy đoán kiểu file của trình duyệt, ngăn chặn tấn công chèn mã thực thi qua file tĩnh."],
        ["X-Frame-Options", "SAMEORIGIN", "Ngăn chặn trang web bị nhúng vào thẻ <iframe> của các tên miền lạ, triệt tiêu hoàn toàn kỹ thuật tấn công Clickjacking."],
        ["Referrer-Policy", "strict-origin-when-cross-origin", "Bảo vệ thông tin đường dẫn nhạy cảm trên URL không bị rò rỉ khi người dùng chuyển hướng sang liên kết ngoài."],
        ["X-XSS-Protection", "1; mode=block", "Kích hoạt bộ lọc chống Cross-Site Scripting cơ bản trên các trình duyệt thế hệ cũ."]
    ]
    add_table_data(sec_headers, sec_data, [4.5, 4.0, 7.5])

    add_h2("2.6. Xử lý đường dẫn và tham số Proxy Header cho WordPress")
    add_p("Nginx thực hiện chèn các tiêu đề ủy quyền Host, X-Real-IP, X-Forwarded-For và X-Forwarded-Proto đảm bảo WordPress tạo liên kết chính xác dưới giao thức https://.")

    doc.add_page_break()

    # ========================== CHUONG 3 ==========================
    add_h1("CHƯƠNG 3: HỆ THỐNG GIÁM SÁT HIỆU NĂNG VỚI PROMETHEUS VÀ GRAFANA")
    add_h2("3.1. Tổng quan mô hình giám sát Pull-based Metrics")
    add_p("Prometheus hoạt động theo cơ chế Pull định kỳ (15 giây/lần), chủ động kéo các dữ liệu chỉ số từ các Exporter thay vì chờ nhận dữ liệu thụ động, giúp kiểm soát tần suất quét và dễ dàng phát hiện khi một dịch vụ mục tiêu gặp sự cố.")

    add_h2("3.2. Thu thập chỉ số tài nguyên Host với Node Exporter")
    add_p("Node Exporter ('news_node_exporter') được gắn kết trực tiếp với thư mục '/proc' và '/sys' của máy chủ Ubuntu Host ở chế độ chỉ đọc, cung cấp các chỉ số phần cứng quan trọng: tỷ lệ tải CPU, RAM tiêu thụ, dung lượng đĩa và lưu lượng mạng.")

    add_h2("3.3. Thu thập chỉ số hiệu năng Container với cAdvisor")
    add_p("Google cAdvisor ('news_cadvisor') thu thập tức thời các chỉ số CPU và RAM của từng container Docker riêng biệt thông qua cgroups và docker socket.")

    add_h2("3.4. Cấu hình Prometheus Scrape Targets và chu kỳ thu thập")
    tgt_headers = ["Tên Job", "Mục tiêu Target (DNS Nội bộ)", "Trạng thái", "Thời gian Scrape gần nhất"]
    tgt_data = [
        ["prometheus", "localhost:9090", "UP (100%)", "< 15 giây"],
        ["node_exporter", "news_node_exporter:9100", "UP (100%)", "< 15 giây"],
        ["cadvisor", "news_cadvisor:8080", "UP (100%)", "< 15 giây"]
    ]
    add_table_data(tgt_headers, tgt_data, [4.0, 5.0, 3.5, 3.5])

    add_h2("3.5. Trực quan hóa dữ liệu với Grafana và Provisioning tự động")
    add_p("Grafana được cấu hình nạp tự động Datasource Prometheus và Bảng điều khiển từ tệp JSON, hiển thị trực quan các đồng hồ đo tải máy chủ và biểu đồ phân bổ bộ nhớ container.")

    doc.add_page_break()

    # ========================== CHUONG 4 ==========================
    add_h1("CHƯƠNG 4: HỆ THỐNG THU THẬP VÀ PHÂN TÍCH NHẬT KÝ (LOGS) VỚI LOKI VÀ PROMTAIL")
    add_h2("4.1. Kiến trúc hệ thống tập trung nhật ký với Grafana Loki")
    add_p("Grafana Loki chỉ lưu trữ và lập chỉ mục các nhãn siêu dữ liệu (metadata labels), tiết kiệm tới 80% bộ nhớ RAM so với Elasticsearch, phù hợp hoàn hảo với hệ thống vừa và nhỏ.")

    add_h2("4.2. Promtail Log Shipper: Cơ chế quét Docker Socket và Nginx Log Volume")
    add_p("Promtail thu thập luồng xuất chuẩn (stdout/stderr) từ Docker Engine qua socket '/var/run/docker.sock' với quyền chỉ đọc (:ro), đồng thời đọc các tệp log tĩnh từ Nginx.")

    add_h2("4.3. Thiết kế hệ thống nhãn (Labels) khoa học, tối ưu hiệu năng")
    lbl_headers = ["Tên Nhãn (Label)", "Giá trị cấu hình", "Ý nghĩa và mục đích sử dụng"]
    lbl_data = [
        ["job", "nginx", "Nhận diện toàn bộ luồng log từ Reverse Proxy Nginx"],
        ["job", "webapp", "Nhận diện luồng log từ container ứng dụng WordPress"],
        ["service", "reverse-proxy / wordpress / database", "Phân loại theo chức năng nghiệp vụ của dịch vụ"],
        ["container", "news_nginx / news_wordpress / news_mysql", "Tên định danh chính xác của Docker container"]
    ]
    add_table_data(lbl_headers, lbl_data, [3.5, 4.5, 8.0])

    add_h2("4.4. Tích hợp Loki Datasource vào Grafana")
    add_p("Grafana nạp sẵn datasource Loki thông qua tệp 'loki.yml', sẵn sàng phục vụ các câu truy vấn LogQL trong menu Explore.")

    add_h2("4.5. Phân tích 3 kịch bản truy vấn LogQL thực tế và kết quả kiểm thử")
    add_p("1. Xem log Nginx: {job=\"nginx\"}")
    add_p("2. Lọc lỗi HTTP 5xx: {job=\"nginx\"} |~ \"HTTP/[0-9.]+\\\" 5[0-9][0-9]\"")
    add_p("3. Lọc lỗi Ứng dụng: {job=\"webapp\"} |~ \"(?i)(error|exception|failed)\"")

    doc.add_page_break()

    # ========================== CHUONG 5 ==========================
    add_h1("CHƯƠNG 5: ĐÁNH GIÁ AN TOÀN THÔNG TIN VÀ GIA CỐ HỆ THỐNG (SYSTEM HARDENING)")
    add_h2("5.1. Áp dụng nguyên tắc đặc quyền tối thiểu (Least Privilege)")
    add_p("Nhằm bảo vệ máy chủ Host khỏi nguy cơ bị chiếm quyền điều khiển (Container Breakout), hệ thống đã rà soát và cấu hình chặt chẽ quyền hạn của từng container:")
    add_p("- Hệ thống triệt để không sử dụng cờ 'privileged: true' cho các dịch vụ ứng dụng, cơ sở dữ liệu và proxy ('news_wordpress', 'news_mysql', 'news_nginx', 'news_phpmyadmin', 'news_prometheus', 'news_grafana', 'news_loki', 'news_node_exporter'). Duy nhất container 'news_cadvisor' được cấu hình 'privileged: true' do yêu cầu kỹ thuật bắt buộc: cAdvisor cần quyền đọc trực tiếp các thông số cgroup nhân Linux, thiết bị '/dev/kmsg' và thông tin ổ đĩa hệ thống để trích xuất chỉ số hiệu năng container. Đây là một điểm cần cân nhắc về mặt an ninh (security trade-off); trong môi trường sản xuất khắt khe, cAdvisor có thể được thay thế bằng cgroup metrics exporter không yêu cầu full-privilege.", bold_prefix="1. Kiểm soát cờ đặc quyền (Privileged Flag): ")
    add_p("- Áp dụng chỉ thị 'security_opt: [ \"no-new-privileges:true\" ]' trên các container hỗ trợ, ngăn chặn các tiến trình bên trong container thực thi lệnh setuid/setgid để nâng quyền.", bold_prefix="2. Cơ chế chống leo thang đặc quyền: ")
    add_p("- Thư mục Docker Socket '/var/run/docker.sock' chỉ được gắn vào container 'news_promtail' và 'news_cadvisor' với tùy chọn chỉ đọc (:ro), ngăn chặn tuyệt đối việc container gửi lệnh điều khiển ngược lại Docker daemon.", bold_prefix="3. Khống chế Docker Socket: ")
    add_p("- Các dịch vụ giám sát 'news_prometheus' và 'news_node_exporter' chạy dưới user 'nobody' (UID 65534); 'news_grafana' chạy dưới user 'grafana' (UID 472); 'news_loki' chạy dưới user 'loki' (UID 10001); 'news_mysql' chạy dưới user 'mysql' (UID 999). Các container còn lại ('news_nginx', 'news_wordpress', 'news_phpmyadmin', 'news_promtail') khởi chạy tiến trình master dưới quyền 'root' do đặc thù liên kết cổng mạng < 1024 (cổng 80/443) và đọc log hệ thống, nhưng các tiến trình worker xử lý yêu cầu người dùng đều được hạ quyền xuống user thông thường ('nginx', 'www-data').", bold_prefix="4. Phân định quyền thực thi tiến trình: ")

    add_h2("5.2. Kiểm soát bề mặt tấn công: Giới hạn Port Exposure")
    add_p("- Cổng 3306 của MySQL hoàn toàn không xuất hiện trong khối 'ports:' của file docker-compose.yml. Dữ liệu chỉ được truy vấn nội bộ qua mạng 'news_backend_net'.", bold_prefix="Cô lập MySQL: ")
    add_p("- Cổng 3100 (Loki) và 9080 (Promtail) được giữ kín trong mạng giám sát nội bộ 'news_monitoring_net'.", bold_prefix="Cô lập Logging: ")
    add_p("- Cổng 80 của WordPress không public ra ngoài host, toàn bộ lưu lượng web bắt buộc phải đi qua Nginx Reverse Proxy để được kiểm tra bảo mật.", bold_prefix="Bảo vệ WordPress: ")

    add_h2("5.3. Quản lý bí mật (Secrets Management) và bảo vệ file cấu hình")
    add_p("- Tách biệt toàn bộ thông tin nhạy cảm vào file '.env'. File '.env' và khóa riêng tư 'selfsigned.key' được gán quyền 'chmod 600'. Cấu hình '.gitignore' nghiêm ngặt để ngăn chặn đưa secrets lên Git.")

    add_h2("5.4. Đánh giá trạng thái Tường lửa Host OS (UFW/Iptables)")
    add_p("Công cụ UFW đang ở trạng thái 'inactive', các chính sách lọc gói tin mạng được Docker daemon tự động thiết lập thông qua Iptables. Nhóm tuân thủ nguyên tắc không tùy tiện kích hoạt UFW gây gián đoạn SSH.")

    add_h2("5.5. Thiết lập cơ chế kiểm tra sức khỏe tự động (Docker Healthchecks)")
    add_p("Toàn bộ các dịch vụ chủ chốt đều gắn kèm Healthcheck, đảm bảo WordPress chỉ khởi động sau khi MySQL đã hoàn tất nạp bộ nhớ đệm và sẵn sàng nhận kết nối.")

    doc.add_page_break()

    # ========================== CHUONG 6 ==========================
    add_h1("CHƯƠNG 6: QUY TRÌNH QUẢN LÝ MÃ NGUỒN GIT VÀ LỊCH SỬ PHIÊN BẢN")
    add_h2("6.1. Cấu trúc kho mã nguồn và loại trừ rò rỉ dữ liệu qua .gitignore")
    add_p("Kho mã nguồn được khởi tạo tại '/home/ubuntu/trienkhaihethong'. Tệp '.gitignore' loại trừ toàn bộ dữ liệu tạm, log, cache và thông tin bí mật.")

    add_h2("6.2. Quy chuẩn thông điệp Commit (Conventional Commits)")
    add_p("Thông điệp commit tuân thủ nghiêm ngặt chuẩn Conventional Commits: '<loại>(<phạm_vi>): <mô_tả>'.")

    add_h2("6.3. Chi tiết lịch sử các Commit triển khai thực tế")
    cmt_headers = ["STT", "Mã Hash", "Chuẩn Commit", "Nội dung tóm tắt thay đổi kỹ thuật"]
    cmt_data = [
        ["0", "3edf85b", "feat(app)", "Triển khai WordPress 6.7, MySQL 8.0, phpMyAdmin với Docker Compose, cấu hình named volumes và mạng frontend/backend."],
        ["1", "6ad465e", "feat(proxy)", "Cấu hình Nginx Reverse Proxy, SSL/TLS Termination, chuyển hướng HTTP 301, proxy headers và các HTTP Security Headers."],
        ["2", "5e16e02", "feat(monitoring)", "Triển khai hạ tầng giám sát Prometheus, Node Exporter, cAdvisor, cấu hình provisioning Grafana và dashboard trực quan."],
        ["3", "b7f07ab", "feat(logging)", "Triển khai hệ thống tập trung nhật ký với Loki, Promtail, cấu hình Docker socket scraper và kiểm thử 3 truy vấn LogQL."],
        ["4", "7e51e0b", "docs", "Hoàn thiện tài liệu README hướng dẫn vận hành và Báo cáo học thuật cuối kỳ (định dạng Markdown và Word DOCX)."],
        ["5", "efef9cd", "chore", "Cập nhật tệp .gitignore loại trừ các script kiểm thử tạm và hoàn thiện cấu hình Nginx."]
    ]
    add_table_data(cmt_headers, cmt_data, [1.5, 2.5, 3.5, 8.5])

    add_h2("6.4. Tài liệu hướng dẫn vận hành hệ thống (README.md)")
    add_p("Tệp README.md cung cấp đầy đủ sơ đồ kiến trúc, hướng dẫn cấu hình .env, lệnh khởi chạy an toàn (Zero Data Loss), cách truy cập và xử lý sự cố.")

    doc.add_page_break()

    # ========================== CHUONG 7 ==========================
    add_h1("CHƯƠNG 7: KẾT QUẢ KIỂM THỬ TÍCH HỢP TOÀN DIỆN (INTEGRATION TESTING)")
    
    add_p("Quá trình kiểm thử tích hợp được thực hiện trực tiếp trên môi trường thực tế máy chủ ảo Ubuntu '192.168.177.128', kiểm tra chéo giữa các tầng dịch vụ. Kết quả tổng hợp tại Bảng 7.1:")

    test_headers = ["Hạng mục Kiểm thử", "Lệnh / Phương pháp Thực hiện", "Kết quả Thực tế Ghi nhận", "Đánh giá"]
    test_data = [
        ["Tính sẵn sàng Web", "curl -k https://192.168.177.128/", "HTTP/2 200, hiển thị đúng tiêu đề Cổng thông tin tin tức", "ĐẠT"],
        ["Chuyển hướng HTTP 301", "curl -I http://192.168.177.128/", "HTTP/1.1 301 Moved Permanently sang HTTPS", "ĐẠT"],
        ["HTTP Security Headers", "curl -k -I https://192.168.177.128/", "Xuất hiện nosniff, SAMEORIGIN, strict-origin-when-cross-origin", "ĐẠT"],
        ["Giao diện phpMyAdmin", "curl -k https://192.168.177.128/pma/", "HTTP/2 200, trang đăng nhập phpMyAdmin sẵn sàng", "ĐẠT"],
        ["Bền vững Dữ liệu CSDL", "docker compose restart news_mysql news_wordpress", "Website tải bình thường, giữ nguyên 100% bài viết và cấu hình", "ĐẠT"],
        ["Prometheus Targets", "curl http://localhost:9090/api/v1/targets", "3/3 targets (node_exporter, cadvisor, prometheus) đều UP", "ĐẠT"],
        ["Grafana Provisioning", "Truy cập http://localhost:3000/api/datasources", "Nạp sẵn Datasource Prometheus, Loki và Dashboard Overview", "ĐẠT"],
        ["Loki Log Ingestion", "curl http://localhost:3100/ready", "Trả về trạng thái ready (HTTP 200), nhận luồng log liên tục", "ĐẠT"],
        ["LogQL: Xem Log Nginx", "{job=\"nginx\"}", "Trả về danh sách log truy cập HTTP request thực tế", "ĐẠT"],
        ["LogQL: Lọc Lỗi 5xx", "{job=\"nginx\"} |~ \"HTTP/[0-9.]+\\\" 5[0-9][0-9]\"", "Bắt chính xác các yêu cầu HTTP lỗi 500 và 502", "ĐẠT"],
        ["LogQL: Lọc Lỗi App", "{job=\"webapp\"} |~ \"(?i)(error|exception|failed)\"", "Bắt chính xác thông điệp PHP Fatal Exception", "ĐẠT"],
        ["Network Isolation", "docker exec news_nginx nc -z news_mysql 3306", "Kết nối bị từ chối / không thể truy cập (Đúng thiết kế)", "ĐẠT"]
    ]
    add_table_data(test_headers, test_data, [3.5, 4.5, 6.5, 1.5])

    add_h2("7.1. Kiểm thử tính toàn vẹn và phản hồi của Ứng dụng Web")
    add_p("Sau khi toàn bộ ngăn xếp dịch vụ được triển khai thông qua Docker Compose, nhóm đã tiến hành khảo sát trạng thái của toàn bộ 10 container dịch vụ trên máy chủ Ubuntu thông qua câu lệnh 'docker compose ps':")
    add_figure("06_docker_compose_ps.png", "Hình 7.6: Trạng thái 10 container dịch vụ của dự án qua lệnh docker compose ps.", "Giải thích minh chứng Hình 7.6: Ảnh chụp màn hình từ terminal Ubuntu xác nhận 100% container dịch vụ đều đang vận hành ở trạng thái Up ổn định. Các dịch vụ có cấu hình kiểm tra sức khỏe tự động (news_nginx, news_wordpress, news_mysql, news_cadvisor) đều đạt trạng thái healthy. Các cổng mạng công khai (80, 443, 3000, 8081, 9090) được phân bổ chính xác theo ma trận cổng, trong khi cổng cơ sở dữ liệu 3306 được bảo vệ tuyệt đối trong mạng nội bộ.", width_cm=16.0)

    add_p("Tiếp theo, ứng dụng Cổng thông tin tin tức WordPress được kiểm thử truy cập trực tiếp từ trình duyệt thông qua giao thức HTTPS:")
    add_figure("01_wordpress.png", "Hình 7.1: Giao diện Cổng thông tin tin tức WordPress hiển thị qua HTTPS.", "Giải thích minh chứng Hình 7.1: Ảnh chụp giao diện thực tế từ trình duyệt chứng minh website WordPress hoạt động ổn định và hiển thị chuẩn xác đằng sau Nginx Reverse Proxy. Tiêu đề website hiển thị đúng cấu hình 'Cổng Thông Tin Tin Tức Công Nghệ', các liên kết stylesheet CSS và cấu trúc bài viết tin tức mẫu đều được tải đầy đủ qua HTTPS mà không gặp lỗi Mixed Content.", width_cm=15.0)

    add_p("Đối với công cụ quản trị cơ sở dữ liệu phpMyAdmin, nhóm đã tiến hành kiểm tra khả năng truy cập qua đường dẫn proxy '/pma/':")
    add_figure("02_phpmyadmin.png", "Hình 7.2: Giao diện đăng nhập phpMyAdmin qua Reverse Proxy.", "Giải thích minh chứng Hình 7.2: Ảnh chụp màn hình chứng minh giao diện đăng nhập phpMyAdmin phiên bản 5.2 sẵn sàng phục vụ tại URL https://192.168.177.128/pma/. Dịch vụ đã kết nối thành công tới máy chủ MySQL nội bộ trên cổng 3306, cho phép quản trị viên đăng nhập an toàn bằng tài khoản news_user hoặc root để thực hiện các thao tác quản trị cơ sở dữ liệu.", width_cm=14.0)

    add_h2("7.2. Kiểm thử Reverse Proxy, chuyển hướng HTTP sang HTTPS và Security Headers")
    add_p("Nhóm đã sử dụng công cụ curl để kiểm tra cơ chế định tuyến và các tiêu chuẩn bảo mật HTTP trên Nginx:")
    add_p("- Kiểm tra chuyển hướng HTTP 301: Yêu cầu gửi tới cổng 80 (http://192.168.177.128/) ngay lập tức nhận mã trạng thái HTTP/1.1 301 Moved Permanently với tiêu đề Location: https://192.168.177.128/, chứng minh toàn bộ lưu lượng HTTP không an toàn đều được tự động nâng cấp lên kênh truyền mã hóa HTTPS.")
    add_p("- Kiểm tra HTTP Security Headers: Phản hồi từ máy chủ HTTPS chứa đầy đủ 4 tiêu đề an ninh bắt buộc: X-Content-Type-Options: nosniff, X-Frame-Options: SAMEORIGIN, X-XSS-Protection: 1; mode=block và Referrer-Policy: strict-origin-when-cross-origin.")

    add_h2("7.3. Kiểm thử tính bền vững của Cơ sở dữ liệu sau chu kỳ Khởi động lại (Zero-loss Restart)")
    add_p("Để kiểm chứng tính bền vững của cơ chế lưu trữ Named Volumes (news_mysql_data và news_wp_data), nhóm đã tiến hành kịch bản thử nghiệm khởi động lại hai container cốt lõi bằng lệnh 'docker compose restart news_mysql news_wordpress'. Sau khi khởi động lại, website tải bình thường, tiêu đề cổng thông tin, danh sách bài viết đã đăng và các thiết lập tài khoản quản trị được bảo toàn nguyên vẹn 100%, không bị ảnh hưởng bởi chu kỳ khởi động lại container.")

    add_h2("7.4. Kiểm thử trạng thái Targets và Thu thập Metrics của Prometheus")
    add_p("Hạ tầng giám sát hiệu năng được kiểm thử thông qua giao diện quản trị Prometheus Targets và bảng điều khiển Grafana:")
    add_figure("03_prometheus_targets.png", "Hình 7.3: Danh sách các Scrape Targets trong Prometheus đạt trạng thái UP 100%.", "Giải thích minh chứng Hình 7.3: Ảnh chụp màn hình từ giao diện Prometheus tại http://192.168.177.128:9090/targets xác nhận cả 3 scrape pools đều đạt trạng thái UP (1/1 up) màu xanh: cadvisor:8080 (thu thập chỉ số container), node_exporter:9100 (thu thập thông số máy chủ Host) và prometheus (nội tại Prometheus). Thời gian thu thập gần nhất đều dưới 15 giây và không phát sinh lỗi.", width_cm=15.5)

    add_p("Tiếp theo, bảng điều khiển tổng hợp trên Grafana Dashboard được kiểm tra hiển thị số liệu thực tế:")
    add_figure("04_grafana_dashboard.png", "Hình 7.4: Bảng điều khiển Grafana Overview hiển thị số liệu hiệu năng thực tế.", "Giải thích minh chứng Hình 7.4: Ảnh chụp màn hình bảng điều khiển 'DevOps System & Container Overview' trên Grafana xác nhận dữ liệu được nạp thời gian thực từ datasource Prometheus. Các đồng hồ đo phản ánh chính xác các thông số vận hành thực tế của máy chủ Host: mức tiêu thụ CPU đạt 6.56%, bộ nhớ RAM đang sử dụng đạt 43.0%, dung lượng ổ đĩa phân vùng gốc đạt 86.1% và thời gian hoạt động liên tục (Host Uptime) đạt 1.45 giờ.", width_cm=15.5)

    add_h2("7.5. Kiểm thử Khả năng Truy vấn Nhật ký Thực tế của Loki")
    add_p("Hệ thống tập trung nhật ký được kiểm tra trên giao diện Grafana Explore với datasource Loki:")
    add_figure("05_loki_logql.png", "Hình 7.5: Kết quả truy vấn LogQL {job=\"nginx\"} trên Grafana Explore.", "Giải thích minh chứng Hình 7.5: Ảnh chụp màn hình Grafana Explore chứng minh Promtail và Loki đã phối hợp thu thập thành công luồng nhật ký từ Nginx Reverse Proxy. Khi thực thi câu lệnh LogQL {job=\"nginx\"}, hệ thống hiển thị biểu đồ phân bổ tần suất nhật ký (Logs Volume) ghi nhận tổng cộng 825 bản ghi truy cập trong 1 giờ gần nhất. Bảng danh sách chi tiết bên dưới hiển thị chuẩn xác từng dòng log HTTP request thực tế kèm mã phản hồi 200/301, địa chỉ IP máy khách và thời gian xử lý.", width_cm=15.5)

    doc.add_page_break()

    # ========================== CHUONG 8 ==========================
    add_h1("CHƯƠNG 8: HẠN CHẾ THỰC TẾ VÀ HƯỚNG PHÁT TRIỂN")
    add_h2("8.1. Các hạn chế kỹ thuật trong môi trường thử nghiệm")
    add_p("- Do máy chủ hoạt động trong mạng cục bộ ảo hóa với địa chỉ IP riêng (192.168.177.128), không có tên miền công khai (FQDN), hệ thống bắt buộc phải dùng chứng chỉ tự ký (Self-signed Certificate). Các trình duyệt web sẽ hiển thị cảnh báo chứng chỉ không đáng tin cậy.", bold_prefix="1. Giới hạn SSL: ")
    add_p("- Toàn bộ 10 container dịch vụ đều tập trung trên một máy chủ ảo Ubuntu duy nhất. Khi máy chủ gặp sự cố phần cứng, toàn bộ hệ thống sẽ bị gián đoạn.", bold_prefix="2. Điểm lỗi đơn lẻ (SPOF): ")
    add_p("- Dữ liệu nhật ký của Loki và chỉ số của Prometheus hiện lưu trữ trên ổ đĩa cục bộ, chưa tích hợp với các hệ thống lưu trữ đối tượng phân tán (như AWS S3 hoặc MinIO) để lưu trữ dữ liệu lịch sử nhiều năm.", bold_prefix="3. Lưu trữ Log dài hạn: ")

    add_h2("8.2. Đề xuất kiến trúc mở rộng trong môi trường Doanh nghiệp")
    add_p("- Chuyển đổi toàn bộ cấu hình Docker Compose sang Kubernetes (K8s) Manifests / Helm Charts. Tích hợp công cụ cert-manager tự động phát hành và gia hạn chứng chỉ Let's Encrypt SSL/TLS miễn phí. Sử dụng Horizontal Pod Autoscaler (HPA) tự động co giãn số lượng Pod WordPress dựa trên tải CPU thực tế.", bold_prefix="1. Điều phối cụm Kubernetes: ")
    add_p("- Xây dựng cụm MySQL InnoDB Cluster hoặc mô hình MySQL Replication kết hợp bộ cân bằng tải ProxySQL để tăng tốc độ truy vấn.", bold_prefix="2. Cụm Cơ sở dữ liệu HA: ")
    add_p("- Xây dựng quy trình CI/CD hoàn chỉnh bằng GitHub Actions / GitLab CI. Tự động quét mã độc và lỗ hổng bảo mật của container image bằng Trivy trước khi triển khai.", bold_prefix="3. Tự động hóa CI/CD: ")
    add_p("- Thiết lập Prometheus Alertmanager để tự động gửi thông báo cảnh báo qua Telegram, Slack hoặc Email khi dung lượng đĩa > 85% hoặc phát hiện tần suất lỗi HTTP 5xx bất thường.", bold_prefix="4. Cảnh báo chủ động (Alerting): ")

    doc.add_page_break()

    # ========================== KET LUAN ==========================
    add_h1("KẾT LUẬN")
    add_p("Sau quá trình nghiên cứu lý thuyết, thiết kế kiến trúc và trực tiếp triển khai thực nghiệm trên máy chủ Ubuntu Linux, đề tài 'Thiết kế, triển khai và vận hành hệ thống Cổng thông tin tin tức trên nền tảng container với Docker Compose, Nginx Reverse Proxy, Prometheus, Grafana, Loki và Promtail' đã được hoàn thành xuất sắc, đáp ứng 100% các tiêu chí yêu cầu của học phần Triển khai và Quản trị Hệ thống Phần mềm:")
    add_p("- Triển khai thành công 10 container dịch vụ phối hợp nhịp nhàng, tối ưu hóa tài nguyên phần cứng.", bold_prefix="1. Về mặt Hạ tầng: ")
    add_p("- Ứng dụng WordPress hoạt động ổn định đằng sau Nginx Reverse Proxy, kích hoạt mã hóa HTTPS và đầy đủ các HTTP Security Headers.", bold_prefix="2. Về mặt Ứng dụng & Bảo mật: ")
    add_p("- Dữ liệu cơ sở dữ liệu và nội dung website được bảo toàn nguyên vẹn sau chu kỳ khởi động lại nhờ cơ chế Named Volumes.", bold_prefix="3. Về mặt Dữ liệu: ")
    add_p("- Hạ tầng giám sát Prometheus, Node Exporter, cAdvisor và Grafana phản ánh chính xác các chỉ số tải phần cứng máy chủ và container trong thời gian thực.", bold_prefix="4. Về mặt Giám sát: ")
    add_p("- Làm chủ hệ thống tập trung nhật ký Loki và Promtail, thiết lập hệ thống nhãn chuẩn xác và thực thi thành công 3 kịch bản truy vấn LogQL thực tế.", bold_prefix="5. Về mặt Quản lý Log: ")
    add_p("- Áp dụng phân tách mạng đa tầng (Network Segmentation), ẩn cổng CSDL, quản lý thông tin bí mật qua .env và quản lý phiên bản mã nguồn bài bản theo chuẩn Git Conventional Commits.", bold_prefix="6. Về mặt An toàn & Quy trình: ")
    add_p("Đề tài không chỉ cung cấp một sản phẩm phần mềm hoàn chỉnh có thể vận hành và trình diễn thực tế, mà còn giúp sinh viên củng cố vững chắc tư duy kiến trúc hệ thống hiện đại, kỹ năng làm chủ công nghệ đám mây và phương pháp vận hành hệ thống theo chuẩn DevOps quốc tế.")

    doc.add_page_break()

    # ========================== TAI LIEU THAM KHAO ==========================
    add_h1("TÀI LIỆU THAM KHẢO")
    refs = [
        "1. Docker Inc. (2024). Docker Documentation: Docker Compose file reference v2. Truy cập tại: https://docs.docker.com/compose/",
        "2. WordPress Foundation (2024). WordPress Developer Handbook & Architecture. Truy cập tại: https://developer.wordpress.org/",
        "3. Nginx Software Inc. (2024). NGINX Reverse Proxy & Security Controls Guide. Truy cập tại: https://docs.nginx.com/",
        "4. Prometheus Authors (2024). Prometheus Monitoring: An open-source monitoring system and time series database. Truy cập tại: https://prometheus.io/docs/",
        "5. Grafana Labs (2024). Grafana Loki: Like Prometheus, but for logs. Truy cập tại: https://grafana.com/docs/loki/latest/",
        "6. OWASP Foundation (2023). OWASP Secure Headers Project. Truy cập tại: https://owasp.org/www-project-secure-headers/",
        "7. Canonical Ltd. (2024). Ubuntu Server Guide & Security Hardening. Truy cập tại: https://ubuntu.com/server/docs",
        "8. OpenSSL Software Foundation (2024). OpenSSL Cryptography and SSL/TLS Toolkit. Truy cập tại: https://www.openssl.org/"
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before, p_ref.paragraph_format.space_after = Pt(2), Pt(4)
        p_ref.paragraph_format.left_indent = Cm(0.5)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name, r_ref.font.size, r_ref.font.color.rgb = "Times New Roman", Pt(11), COLOR_TEXT

    # Luu file
    doc.save(output_path)
    print(f"[OK] Da tao thanh cong file bao cao tai: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "report", "BAO_CAO_CUOI_KY.docx")
    create_report_docx(out_file)
