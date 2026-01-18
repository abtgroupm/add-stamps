from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

stamp_path = "BVHC_stamps.png"
input_pdf  = "Banve HC NMĐMT PT1.pdf"
output_pdf = "Banve HC NMĐMT PT1_s2.pdf"

stamp_w_mm = 120
stamp_h_mm = 65

# Đọc file gốc để lấy kích thước trang thực tế
reader = PdfReader(input_pdf)
first_page = reader.pages[0]
page_width = float(first_page.mediabox.width)
page_height = float(first_page.mediabox.height)

print(f"Page size: {page_width:.2f} x {page_height:.2f} points")
print(f"Stamp size: {stamp_w_mm}mm x {stamp_h_mm}mm")

# Tạo layer dấu với kích thước trang thực tế
packet = BytesIO()
can = canvas.Canvas(packet, pagesize=(page_width, page_height))

# Tính vị trí: giữa mép phải
stamp_w_pt = stamp_w_mm * mm  # Convert mm to points
stamp_h_pt = stamp_h_mm * mm
x_position = page_width - stamp_w_pt - (5 * mm)  # Lùi vào 5mm từ mép phải
y_position = (page_height - stamp_h_pt) / 2  # Giữa theo chiều dọc

print(f"Stamp position: x={x_position:.2f}, y={y_position:.2f}")

can.drawImage(
    ImageReader(stamp_path),
    x=x_position,
    y=y_position,
    width=stamp_w_pt,
    height=stamp_h_pt,
    mask='auto'
)

can.save()
packet.seek(0)

# Đọc stamp layer
stamp_pdf = PdfReader(packet)

# Tạo writer mới
writer = PdfWriter()

# Chèn dấu vào từng trang
for i, page in enumerate(reader.pages):
    page.merge_page(stamp_pdf.pages[0])
    writer.add_page(page)
    print(f"Processed page {i + 1}")

# Lưu kết quả
with open(output_pdf, "wb") as fp:
    writer.write(fp)

print(f"Done! Output: {output_pdf}")