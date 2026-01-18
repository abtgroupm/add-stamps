import fitz  
import os

def insert_stamp_adjustable(input_pdf_path, output_pdf_path, stamp_image_path):
    if not os.path.exists(stamp_image_path):
        print(f"Lỗi: Không tìm thấy file ảnh tại {stamp_image_path}")
        return

    try:
        doc = fitz.open(input_pdf_path)
        
        # --- CẤU HÌNH VỊ TRÍ ---
        STAMP_WIDTH_CM = 12.0
        STAMP_HEIGHT_CM = 6.0
        MARGIN_CM = 2.0        # Khoảng cách từ mép giấy vào
        
        # ---  CHỈNH LÊN / XUỐNG TẠI ĐÂY ---
        # 0: Nằm chính giữa
        # Số DƯƠNG (ví dụ 5.0): Dịch XUỐNG dưới 5cm
        # Số ÂM (ví dụ -5.0): Dịch LÊN trên 5cm
        OFFSET_UD_CM = 3.0  
        
        # Chuyển đổi sang points
        s_w = STAMP_WIDTH_CM * 28.35
        s_h = STAMP_HEIGHT_CM * 28.35
        margin = MARGIN_CM * 28.35
        offset_ud = OFFSET_UD_CM * 28.35 # Đổi offset sang points

        print(f"Đang xử lý với độ dịch chuyển: {OFFSET_UD_CM} cm...")

        for page in doc:
            box = page.cropbox 
            
            if box.width > box.height:
                # --- TRANG NGANG (Landscape) ---
                # y0 là trục dọc. Cộng thêm offset để dịch xuống.
                
                x0 = box.x1 - margin - s_w
                # Công thức cũ: (box.y0 + box.y1) / 2 - (s_h / 2)
                # Công thức mới: Thêm + offset_ud
                y0 = ((box.y0 + box.y1) / 2 - (s_h / 2)) + offset_ud
                
                rect = fitz.Rect(x0, y0, x0 + s_w, y0 + s_h)
                rotation = 0 

            else:
                # --- TRANG DỌC (Portrait) ---
                # Với trang dọc (bị xoay), trục dọc nhìn thấy thực chất là trục ngang (x) vật lý.
                # Do đó ta cộng offset vào x0.
                
                # Công thức cũ: (box.x0 + box.x1) / 2 - (s_h / 2)
                # Công thức mới: Thêm + offset_ud
                x0 = ((box.x0 + box.x1) / 2 - (s_h / 2)) + offset_ud
                
                y0 = box.y1 - margin - s_w
                
                rect = fitz.Rect(x0, y0, x0 + s_h, y0 + s_w)
                rotation = -90

            page.insert_image(rect, filename=stamp_image_path, 
                              keep_proportion=True, overlay=True, rotate=rotation)

        doc.save(output_pdf_path)
        print(f"Hoàn tất! File lưu tại: {output_pdf_path}")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

if __name__ == "__main__":
    input_file = r"C:\Users\nguye\stamps\Banve HC NMĐMT PT1.pdf" 
    output_file = r"C:\Users\nguye\stamps\Banve HC NMĐMT PT1_final2.pdf"
    stamp_file = r"C:\Users\nguye\stamps\BVHC_stamps.png"
    
    insert_stamp_adjustable(input_file, output_file, stamp_file)