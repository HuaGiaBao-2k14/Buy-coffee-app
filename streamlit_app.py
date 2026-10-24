# -*- coding: utf-8 -*-
# ============================================================================
#  CHIA TIỀN NHÓM  ·  OD1 Buổi 1  ·  CyberSoft OVERDRIVE THPT (bản giảm tải)
#  Kiến thức: biến · kiểu dữ liệu · ép kiểu · phép toán / // % ** · round
#             f-string {x:,} · hệ cơ số bin/hex
#  BẢN CỦA EM (starter) — điền 8 TODO ở PHẦN 2.  Chạy:  streamlit run app_starter.py
#  Lời giải để so: app.py
#
#  App có 3 PHẦN, đúng như chương trình console em viết trên lớp:
#     PHẦN 1  NHẬP      : lấy dữ liệu từ người dùng   (console dùng input())
#     PHẦN 2  TÍNH      : Python THUẦN, chỉ biến + phép toán (y hệt console)
#     PHẦN 3  HIỂN THỊ  : đưa kết quả lên màn hình     (console dùng print())
#
#  Ghi nhớ: mỗi lần em đổi 1 ô nhập, Streamlit CHẠY LẠI TOÀN BỘ file này
#  từ dòng đầu tới dòng cuối. Vì vậy ta không cần vòng lặp hay nút "Tính".
# ============================================================================
import streamlit as st

st.set_page_config(page_title="Chia Tiền Nhóm", page_icon="🧋", layout="wide")

st.title("🧋 Chia Tiền Nhóm")
st.caption("Nhập hoá đơn, VAT, tiền tip và số người. App tính mỗi người trả bao nhiêu và gợi ý cách đưa tiền.")

# Chia màn hình làm 2 cột: trái để NHẬP, phải để xem KẾT QUẢ
trai, phai = st.columns([1, 1.35], gap="large")

# ----------------------------------------------------------------------------
# PHẦN 1 · NHẬP  (giống input() nhưng là ô trên web) — đặt ở cột trái
# ----------------------------------------------------------------------------
ten_nhom = trai.text_input("Tên nhóm", value="Nhóm 10A1 đi trà sữa")

tong_hoa_don = trai.number_input("Tổng hoá đơn (đồng)", min_value=0, value=685000, step=1000)
vat = trai.number_input("Thuế VAT (%)", min_value=0, max_value=20, value=8, step=1)
tip = trai.slider("Tiền tip cho nhân viên (%)", min_value=0, max_value=20, value=5)
# min_value=1 → không bao giờ chia cho 0 (ZeroDivisionError)
so_nguoi = trai.number_input("Số người", min_value=1, max_value=50, value=7, step=1)

# ----------------------------------------------------------------------------
# PHẦN 2 · TÍNH  ← EM VIẾT PHẦN NÀY (Python thuần, giống bài console)
#   Mỗi dòng "= 0" là một chỗ em phải thay bằng phép tính đúng.
#   Thử từng dòng trong console trước nếu chưa chắc!
# ----------------------------------------------------------------------------
# TODO 1: tiền VAT = tổng hoá đơn nhân vat rồi chia 100
tien_vat = tong_hoa_don * vat // 100
# TODO 2: tiền tip, làm giống TODO 1 nhưng dùng biến tip
tien_tip = tong_hoa_don * tip // 100

# TODO 3: tổng phải trả = hoá đơn + VAT + tip
tong_phai_tra = tong_hoa_don + vat + tip
# TODO 4: mỗi người = tổng phải trả chia (/) cho số người
moi_nguoi = tong_phai_tra / so_nguoi

# TODO 5: làm tròn LÊN tới hàng nghìn:  (int(moi_nguoi) + 999) // 1000 * 1000
moi_nguoi_tron = (int(moi_nguoi) + 999) // 1000 * 1000

# TODO 6: tổng thu = moi_nguoi_tron nhân số người;  quỹ nhóm = tổng thu − tổng phải trả
tong_thu = moi_nguoi_tron * so_nguoi
quy_nhom = tong_hoa_don - tong_phai_tra

# TODO 7: đổi moi_nguoi_tron ra số tờ 50k, 10k, 1k   (dùng // để lấy số tờ, % để lấy phần còn lại)
to_50k = moi_nguoi_tron // 50000
con_lai = moi_nguoi_tron % 50000
to_10k = ((moi_nguoi_tron // 50000) * 50000) // 10000
to_1k = ((moi_nguoi_tron // 50000) * 50000) - (((moi_nguoi_tron // 50000) * 50000) // 10000) * 10000

# TODO 8: đổi so_nguoi sang hệ nhị phân bằng bin(...), thập lục phân bằng hex(...)
so_nguoi_nhi_phan = bin(so_nguoi)
so_nguoi_hex = hex(so_nguoi)

# ----------------------------------------------------------------------------
# PHẦN 3 · HIỂN THỊ  (giống print() nhưng đẹp hơn) — đặt ở cột phải
# ----------------------------------------------------------------------------
phai.subheader(f"📋 {ten_nhom}")

c1, c2, c3 = phai.columns(3)
c1.metric("Tổng phải trả", f"{tong_phai_tra:,.0f} đ")
c2.metric("Mỗi người (chính xác)", f"{moi_nguoi:,.2f} đ")
c3.metric("Mỗi người đưa", f"{moi_nguoi_tron:,} đ")

phai.write(f"Hoá đơn **{tong_hoa_don:,} đ** + VAT {vat}% (**{tien_vat:,.0f} đ**)"
         f" + tip {tip}% (**{tien_tip:,.0f} đ**) = **{tong_phai_tra:,.0f} đ**.")
phai.write(f"Mỗi người đưa **{moi_nguoi_tron:,} đ** → nhóm thu {tong_thu:,} đ,"
         f" dư **{quy_nhom:,.0f} đ** bỏ vào quỹ nhóm.")

phai.info(f"💵 Mỗi người đưa: **{to_50k}** tờ 50.000 · **{to_10k}** tờ 10.000 · **{to_1k}** tờ 1.000")

hop = phai.expander("🧠 Góc máy tính: Python đã làm gì?")   # hộp gập/mở
hop.code(f"tong_phai_tra = {tong_hoa_don} + {tien_vat} + {tien_tip} = {tong_phai_tra}\n"
         f"moi_nguoi     = {tong_phai_tra} / {so_nguoi} = {moi_nguoi}\n"
         f"type(moi_nguoi) → {type(moi_nguoi).__name__}\n"
         f"so_nguoi = {so_nguoi} = {so_nguoi_nhi_phan} (nhị phân) = {so_nguoi_hex} (thập lục phân)",
         language="text")

st.divider()
st.caption("CyberSoft OVERDRIVE THPT · OD1 Buổi 1 · hotline 0961 05 10 14 · junior.cybersoft.edu.vn")

