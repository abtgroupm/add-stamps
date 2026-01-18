import fitz  
import os

def insert_stamp_final(input_pdf_path, output_pdf_path, stamp_image_path):
    # Kiểm tra file tồn tại
    if not os.path.exists(stamp_image_path):
        print(f"Lỗi: Không tìm thấy file ảnh tại {stamp_image_path}")
        return

    try:
        doc = fitz.open(input_pdf_path)
        
        # --- CẤU HÌNH KÍCH THƯỚC & VỊ TRÍ ---
        # Bạn có thể điều chỉnh các số này nếu muốn dịch chuyển con dấu
        STAMP_WIDTH_CM = 12.0   # Chiều rộng con dấu (cm)
        STAMP_HEIGHT_CM = 6.0  # Chiều cao con dấu (cm)
        MARGIN_CM = 2.0        # Khoảng cách từ mép giấy (cm)

        # Chuyển đổi cm sang points (1 cm = 28.35 pts)
        s_w = STAMP_WIDTH_CM * 28.35
        s_h = STAMP_HEIGHT_CM * 28.35
        margin = MARGIN_CM * 28.35

        print("Đang xử lý...")

        for page in doc:
            # Lấy vùng hiển thị thực tế (CropBox)
            box = page.cropbox 
            
            # --- LOGIC TÍNH TOÁN VỊ TRÍ ---
            if box.width > box.height:
                # TRƯỜNG HỢP 1: TRANG NGANG (LANDSCAPE)
                # Đặt bên phải, giữa dọc
                x0 = box.x1 - margin - s_w
                y0 = (box.y0 + box.y1) / 2 - (s_h / 2)
                
                rect = fitz.Rect(x0, y0, x0 + s_w, y0 + s_h)
                rotation = 0 

            else:
                # TRƯỜNG HỢP 2: TRANG DỌC (PORTRAIT) - Bản vẽ bị xoay 90 độ
                # Xoay con dấu -90 độ để khớp với hướng nhìn
                
                # Tọa độ X trên giấy (tương ứng trục dọc của bản vẽ)
                x0 = (box.x0 + box.x1) / 2 - (s_h / 2)
                
                # Tọa độ Y trên giấy (tương ứng trục ngang bên phải của bản vẽ)
                y0 = box.y1 - margin - s_w
                
                # Tạo rect (kích thước w và h đảo ngược do xoay)
                rect = fitz.Rect(x0, y0, x0 + s_h, y0 + s_w)
                rotation = -90

            # Chèn ảnh
            page.insert_image(rect, 
                              filename=stamp_image_path, 
                              keep_proportion=True, 
                              overlay=True, 
                              rotate=rotation)

        # Lưu file
        doc.save(output_pdf_path)
        print(f"Hoàn tất! File đã được lưu tại: {output_pdf_path}")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

if __name__ == "__main__":
    # --- ĐƯỜNG DẪN FILE ---
    # Hãy cập nhật đường dẫn chính xác của bạn ở đây
    input_file = r"C:\Users\nguye\stamps\Banve HC NMĐMT PT1_V1.pdf" 
    output_file = r"C:\Users\nguye\stamps\ban_ve_hoan_thien.pdf"
    stamp_file = r"C:\Users\nguye\stamps\BVHC_stamps.png"
    
    insert_stamp_final(input_file, output_file, stamp_file)