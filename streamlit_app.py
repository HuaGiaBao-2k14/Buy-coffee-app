import os
import json
import hmac
import hashlib
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Mộc Café | Cà phê tử tế", page_icon="☕", layout="wide", initial_sidebar_state="collapsed")

DATA_FILE = Path("orders.json")
ADMIN_USER = os.getenv("COFFEE_ADMIN_USER", "AdminCoffeeShop@")
ADMIN_PASSWORD = os.getenv("COFFEE_ADMIN_PASSWORD", "12345678_")

PRODUCTS = [
    {"id": "espresso", "name": "Espresso", "subtitle": "Đậm đà • Đánh thức giác quan", "price": 39000, "image": "[GẮN LINK ẢNH]", "tag": "BESTSELLER"},
    {"id": "americano", "name": "Americano", "subtitle": "Thanh nhẹ • Hậu vị cân bằng", "price": 42000, "image": "[GẮN LINK ẢNH]", "tag": "NHẸ NHÀNG"},
    {"id": "latte", "name": "Café Latte", "subtitle": "Espresso hòa quyện sữa mịn", "price": 49000, "image": "[GẮN LINK ẢNH]", "tag": "ĐƯỢC YÊU THÍCH"},
    {"id": "cappuccino", "name": "Cappuccino", "subtitle": "Bọt sữa bồng bềnh • Thơm dịu", "price": 49000, "image": "[GẮN LINK ẢNH]", "tag": "CỔ ĐIỂN"},
    {"id": "mocha", "name": "Mocha", "subtitle": "Cà phê • Chocolate • Sữa", "price": 55000, "image": "[GẮN LINK ẢNH]", "tag": "NGỌT NGÀO"},
    {"id": "coldbrew", "name": "Cold Brew", "subtitle": "Ủ lạnh êm dịu • Mát lành", "price": 52000, "image": "[GẮN LINK ẢNH]", "tag": "Ủ LẠNH"},
    {"id": "vietnamese", "name": "Cà phê sữa đá", "subtitle": "Đậm vị Việt • Ngọt béo hài hòa", "price": 35000, "image": "[GẮN LINK ẢNH]", "tag": "VỊ VIỆT"},
    {"id": "coconut", "name": "Cà phê cốt dừa", "subtitle": "Béo thơm • Mát lạnh", "price": 59000, "image": "[GẮN LINK ẢNH]", "tag": "ĐẶC BIỆT"},
    {"id": "milktea", "name": "Trà sữa truyền thống", "subtitle": "Trà thơm • Sữa béo vừa vặn", "price": 42000, "image": "[GẮN LINK ẢNH]", "tag": "TRÀ SỮA"},
    {"id": "matchamilk", "name": "Trà sữa matcha", "subtitle": "Matcha dịu thơm, hậu vị thanh", "price": 49000, "image": "[GẮN LINK ẢNH]", "tag": "TRÀ SỮA"},
    {"id": "kumquat", "name": "Trà quýt", "subtitle": "Chua ngọt tươi mát", "price": 39000, "image": "[GẮN LINK ẢNH]", "tag": "TRÀ TRÁI CÂY"},
    {"id": "tropical", "name": "Trà nhiệt đới", "subtitle": "Hương trái cây nhiệt đới sảng khoái", "price": 45000, "image": "[GẮN LINK ẢNH]", "tag": "TRÀ TRÁI CÂY"},
    {"id": "peachtea", "name": "Trà đào cam sả", "subtitle": "Thơm dịu • Chua ngọt cân bằng", "price": 45000, "image": "[GẮN LINK ẢNH]", "tag": "ĐƯỢC YÊU THÍCH"},
    {"id": "lemontea", "name": "Trà chanh mật ong", "subtitle": "Thanh mát • Dịu ngọt", "price": 35000, "image": "[GẮN LINK ẢNH]", "tag": "THANH MÁT"},
]

def money(value):
    return f"{value:,.0f}₫".replace(",", ".")

def load_orders():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_orders(orders):
    DATA_FILE.write_text(json.dumps(orders, ensure_ascii=False, indent=2), encoding="utf-8")

def init_state():
    st.session_state.setdefault("page", "home")
    st.session_state.setdefault("cart", {})
    st.session_state.setdefault("order_notice", "")
    st.session_state.setdefault("admin_ok", False)
    st.session_state.setdefault("split_group_name", "Nhóm bạn đi cà phê")

init_state()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root { --coffee:#4b2e23; --cream:#fbf6ee; --copper:#bd8055; }
.stApp { background: #fbf8f2; color: #30251f; font-family:'Be Vietnam Pro',sans-serif; }
.block-container { max-width: 1240px; padding-top: 1.3rem; padding-bottom: 3rem; }
h1,h2,h3 { color:#3d281e; }
.hero { background:linear-gradient(100deg,rgba(36,22,16,.88),rgba(36,22,16,.25)),url('https://images.unsplash.com/photo-1445116572660-236099ec97a0?auto=format&fit=crop&w=1800&q=90') center/cover; border-radius:24px; padding:4rem 3.5rem; color:#fffaf4; min-height:340px; display:flex; flex-direction:column; justify-content:center; }
.hero h1 { color:#fffaf4; font:700 clamp(2.4rem,5vw,4.4rem) 'Playfair Display',serif; margin:0; line-height:1.08; }
.hero p { color:#f2e4d5; font-size:1.05rem; max-width:520px; }
.eyebrow { letter-spacing:.16em; text-transform:uppercase; font-size:.72rem; font-weight:700; color:#d8ad82; margin-bottom:.8rem; }
.product { background:white; border:1px solid #eee4d8; border-radius:18px; padding:14px 14px 17px; margin-bottom:10px; }
.product img { width:100%; height:190px; object-fit:cover; border-radius:12px; }
.product-name {font:700 1.25rem 'Playfair Display',serif;color:#3d281e;margin:.6rem 0 .15rem;}
.product-sub {color:#786c62;font-size:.84rem;min-height:40px;}
.tag {font-size:.65rem;letter-spacing:.08em;font-weight:700;color:#95613e;}
.price {font-weight:700;font-size:1.08rem;color:#4b2e23;margin:.6rem 0;}
div.stButton > button { border-radius:999px; border:1px solid #4b2e23; background:#4b2e23; color:#fffaf4; font-weight:600; padding:.55rem 1rem; }
div.stButton > button:hover { background:#704a36;color:white;border-color:#704a36; }
div[data-testid="stMetric"] {background:white;padding:14px;border:1px solid #eee4d8;border-radius:14px;}
hr {border-color:#e9dfd4;}
.small-muted {color:#786c62;font-size:.85rem;}

.site-nav {background:#e9dcc9;border:1px solid #cdb89c;border-radius:18px;padding:14px 16px;margin:4px 0 24px;box-shadow:0 5px 18px rgba(75,46,35,.07);}
.site-nav button {min-height:44px;}
.body-separator {height:1px;background:#d8c7b2;margin:1.2rem 0;}
.stApp, .stApp p, .stApp label, .stApp [data-testid='stMarkdownContainer'] {color:#30251f;}
.stTextInput input,.stTextArea textarea,.stNumberInput input {color:#30251f!important;background:#fff!important;}
.stCaption, small {color:#66584d!important;}
.nav-brand {font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#4b2e23;}
.nav-sub {font-size:.78rem;color:#786c62;}
.site-footer {margin-top:3.2rem;padding:1.4rem 1.6rem;background:#e9dcc9;border:1px solid #cdb89c;border-radius:16px;color:#4c3b30;box-shadow:0 -3px 16px rgba(75,46,35,.04);}
.tool-hero {background:linear-gradient(110deg,#eee3d2,#f8f3e9);border:1px solid #e3d3bd;border-radius:20px;padding:1.5rem 1.8rem;margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

def nav():
    st.markdown('<div class="site-nav">', unsafe_allow_html=True)
    brand, menu = st.columns([2.4, 5.6], vertical_alignment="center")
    with brand:
        st.markdown('<div class="nav-brand">MỘC CAFÉ</div><div class="nav-sub">Pha bằng sự tử tế · Một ngụm an yên</div>', unsafe_allow_html=True)
    with menu:
        cols = st.columns(5)
        nav_items = [
            ("⌂ Trang chủ", "home"),
            ("☕ Thực đơn", "shop"),
            ("🛍 Giỏ hàng", "cart"),
            ("🧮 Chia tiền", "split"),
            ("⚙ Admin", "admin"),
        ]
        for col, (label, page) in zip(cols, nav_items):
            with col:
                if st.button(label, key=f"nav_{page}", use_container_width=True):
                    st.session_state.page = page
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def show_home():
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Roasted with care • Brewed for you</div>
      <h1>Mỗi ngày,<br>một ly thật ngon.</h1>
      <p>Những hạt cà phê được chọn kỹ, pha bằng sự tận tâm. Dừng lại một chút và thưởng thức khoảnh khắc của riêng bạn.</p>
    </div>""", unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.markdown("### 🌱 Hạt tuyển chọn\nNguồn hạt được chọn lọc, chú trọng hương vị.")
    c2.markdown("### ☕ Pha mới mỗi ly\nTập trung vào trải nghiệm thơm ngon, chỉn chu.")
    c3.markdown("### 🛵 Giao đến tận nơi\nĐiền thông tin nhận hàng khi đặt món.")
    st.write("")
    if st.button("Khám phá thực đơn  →", type="primary"):
        st.session_state.page = "shop"
        st.rerun()
    st.markdown("---")
    st.markdown("#### Món được yêu thích")
    picks = [PRODUCTS[0], PRODUCTS[2], PRODUCTS[6]]
    cols = st.columns(3)
    for col, p in zip(cols, picks):
        with col:
            st.image(p["image"], use_container_width=True)
            st.markdown(f"**{p['name']}** · {money(p['price'])}")
            st.caption(p["subtitle"])

def show_shop():
    st.markdown("# Thực đơn")
    st.markdown("Chọn món, tùy chỉnh size, topping và ghi chú riêng cho từng ly.")
    search = st.text_input("Tìm món", placeholder="Ví dụ: latte, trà sữa, trà quýt…")
    products = [p for p in PRODUCTS if search.lower() in p["name"].lower()] if search else PRODUCTS
    for start in range(0, len(products), 3):
        cols = st.columns(3, gap="medium")
        for col, p in zip(cols, products[start:start+3]):
            with col:
                st.markdown('<div class="product">', unsafe_allow_html=True)
                image_url = p["image"]
                if image_url and image_url != "[GẮN LINK ẢNH]":
                    st.image(image_url, use_container_width=True)
                else:
                    st.markdown('<div style="height:170px;border-radius:12px;background:#eee3d2;display:flex;align-items:center;justify-content:center;color:#665344;font-weight:700;letter-spacing:.04em;">GẮN LINK ẢNH</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="tag">{p["tag"]}</div><div class="product-name">{p["name"]}</div><div class="product-sub">{p["subtitle"]}</div><div class="price">Từ {money(p["price"])}</div>', unsafe_allow_html=True)
                size = st.radio("Size ly", ["L", "XL (+10.000₫)"], horizontal=True, key=f"size_{p['id']}")
                toppings_options = ["Trân châu trắng (+7.000₫)", "Trân châu đen (+7.000₫)", "Kem trứng (+12.000₫)", "Thạch (+7.000₫)"]
                toppings = st.multiselect("Topping", toppings_options, key=f"tops_{p['id']}", placeholder="Không topping")
                note = st.text_input("Ghi chú cho ly này", key=f"note_{p['id']}", placeholder="Ví dụ: 30% đường, ít đá…")
                qty = st.number_input("Số lượng", min_value=1, max_value=30, value=1, key=f"qty_{p['id']}")
                if st.button("Thêm vào giỏ", key=f"add_{p['id']}", use_container_width=True):
                    size_code = "XL" if size.startswith("XL") else "L"
                    topping_price = sum(12000 if "Kem trứng" in t else 7000 for t in toppings)
                    unit_price = p["price"] + (10000 if size_code == "XL" else 0) + topping_price
                    variant_key = f"{p['id']}|{size_code}|{'~'.join(toppings)}|{note.strip()}"
                    existing = st.session_state.cart.get(variant_key)
                    if existing:
                        existing["quantity"] += int(qty)
                    else:
                        st.session_state.cart[variant_key] = {"product_id":p["id"],"name":p["name"],"quantity":int(qty),"size":size_code,"toppings":list(toppings),"note":note.strip(),"unit_price":unit_price}
                    st.toast(f"Đã thêm {p['name']} size {size_code} vào giỏ")
                st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    if st.button("Xem giỏ hàng →"):
        st.session_state.page = "cart"
        st.rerun()

def cart_lines():
    return list(st.session_state.cart.items())

def show_cart():
    st.markdown("# Giỏ hàng & thanh toán")
    lines = cart_lines()
    if not lines:
        st.info("Giỏ hàng đang trống. Hãy chọn vài món từ thực đơn nhé.")
        if st.button("Đến thực đơn"):
            st.session_state.page = "shop"
            st.rerun()
        return
    for item_key, item in lines:
        row = st.columns([3, 1, 1, 1])
        details = f"Size {item['size']}"
        if item["toppings"]: details += " · " + ", ".join(t.split(" (+")[0] for t in item["toppings"])
        if item["note"]: details += f" · Ghi chú: {item['note']}"
        row[0].markdown(f"**{item['name']}** · {details}  \n{money(item['unit_price'])}/ly")
        row[1].write(f"× {item['quantity']}")
        row[2].markdown(f"**{money(item['unit_price'] * item['quantity'])}**")
        with row[3]:
            if st.button("Bỏ", key=f"remove_{hashlib.md5(item_key.encode()).hexdigest()[:10]}"):
                st.session_state.cart.pop(item_key, None)
                st.rerun()
    subtotal = sum(item["unit_price"] * item["quantity"] for _, item in lines)
    st.divider()
    _, b = st.columns([2, 1])
    with b:
        st.markdown(f"**Tạm tính**  \n# {money(subtotal)}")
        st.caption("Phí giao hàng, thuế và típ (nếu có) sẽ được xác nhận theo chính sách cửa hàng.")
    st.markdown("### Thông tin nhận hàng")
    with st.form("checkout_form"):
        name = st.text_input("Tên khách hàng *")
        address = st.text_area("Địa chỉ giao hàng *", placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành")
        contact = st.text_input("Số điện thoại hoặc Email liên lạc *")
        payment = st.radio("Phương thức thanh toán", ["Thanh toán khi nhận hàng (COD)", "Chuyển khoản / thanh toán trực tuyến (demo)"], index=0)
        tip = st.selectbox("Típ cho nhân viên (không bắt buộc)", ["Không", "10.000₫", "20.000₫", "Khác"])
        tip_value = {"Không": 0, "10.000₫": 10000, "20.000₫": 20000, "Khác": 0}[tip]
        if tip == "Khác": tip_value = st.number_input("Số tiền típ (₫)", min_value=0, max_value=1000000, step=5000, value=0)
        agreed = st.checkbox("Tôi xác nhận thông tin đơn hàng là chính xác.")
        submitted = st.form_submit_button("Đặt hàng", type="primary", use_container_width=True)
    if submitted:
        if not name.strip() or not address.strip() or not contact.strip():
            st.error("Vui lòng điền đủ tên, địa chỉ và thông tin liên lạc.")
        elif not agreed:
            st.error("Vui lòng xác nhận thông tin đơn hàng.")
        else:
            total = subtotal + int(tip_value)
            order = {"order_id":datetime.now().strftime("MC%y%m%d%H%M%S"),"created_at":datetime.now().isoformat(timespec="seconds"),"customer":name.strip(),"address":address.strip(),"contact":contact.strip(),"payment_method":payment,"payment_status":"Chờ thanh toán khi nhận" if payment.startswith("Thanh toán khi") else "Chưa thanh toán — demo","items":[{"name":item["name"],"quantity":item["quantity"],"size":item["size"],"toppings":item["toppings"],"note":item["note"],"unit_price":item["unit_price"],"line_total":item["unit_price"]*item["quantity"]} for _,item in lines],"subtotal":subtotal,"tip":int(tip_value),"total":total,"status":"Mới nhận"}
            orders=load_orders(); orders.append(order); save_orders(orders)
            st.session_state.cart={}; st.session_state.order_notice=order["order_id"]; st.session_state.page="confirmation"; st.rerun()

def show_confirmation():
    st.success("Đã ghi nhận đơn hàng!")
    st.markdown("# Cảm ơn bạn đã chọn Mộc Café ☕")
    st.markdown(f"Mã đơn hàng: **{st.session_state.order_notice}**")
    st.info("Đơn hàng đã được lưu trên máy chủ ứng dụng để admin xử lý. Nếu chọn phương thức online demo, đây chưa phải giao dịch thanh toán thật.")
    if st.button("Về trang chủ"):
        st.session_state.page = "home"
        st.rerun()

def show_admin():
    st.markdown("# Khu vực quản trị")
    if not st.session_state.admin_ok:
        st.markdown("Đăng nhập để xem và xử lý đơn hàng.")
        with st.form("admin_login"):
            user = st.text_input("Tài khoản")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập", type="primary")
        if submit:
            valid = hmac.compare_digest(user, ADMIN_USER) and hmac.compare_digest(password, ADMIN_PASSWORD)
            if valid:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("Thông tin đăng nhập không chính xác.")
        st.caption("Thiết lập COFFEE_ADMIN_USER và COFFEE_ADMIN_PASSWORD trong secrets/environment trước khi triển khai công khai.")
        return
    orders = load_orders()
    header = st.columns([3, 1])
    header[0].markdown(f"### Đơn hàng ({len(orders)})")
    with header[1]:
        if st.button("Đăng xuất"):
            st.session_state.admin_ok = False
            st.rerun()
    if not orders:
        st.info("Chưa có đơn hàng nào.")
        return
    new_first = list(reversed(orders))
    statuses = ["Mới nhận", "Đang chuẩn bị", "Đang giao", "Hoàn tất", "Đã hủy"]
    for order in new_first:
        with st.expander(f"{order['order_id']} · {order['customer']} · {money(order['total'])} · {order['status']}", expanded=False):
            st.write(f"**Thời gian:** {order['created_at']}")
            st.write(f"**Khách hàng:** {order['customer']}")
            st.write(f"**Địa chỉ:** {order['address']}")
            st.write(f"**Liên hệ:** {order['contact']}")
            st.write(f"**Thanh toán:** {order['payment_method']} — {order['payment_status']}")
            st.write("**Món:**")
            for item in order["items"]:
                st.write(f"- {item['name']} · size {item.get('size', 'L')} × {item['quantity']} — {money(item['line_total'])}")
                if item.get("toppings"): st.caption("Topping: " + ", ".join(t.split(" (+")[0] for t in item["toppings"]))
                if item.get("note"): st.caption("Ghi chú: " + item["note"])
            st.write(f"**Tạm tính:** {money(order['subtotal'])} · **Típ:** {money(order['tip'])} · **Tổng:** {money(order['total'])}")
            index = statuses.index(order["status"]) if order["status"] in statuses else 0
            new_status = st.selectbox("Cập nhật trạng thái", statuses, index=index, key=f"status_{order['order_id']}")
            if st.button("Lưu trạng thái", key=f"save_{order['order_id']}"):
                for stored in orders:
                    if stored["order_id"] == order["order_id"]:
                        stored["status"] = new_status
                save_orders(orders)
                st.toast("Đã cập nhật đơn hàng.")
                st.rerun()
    st.download_button("Tải dữ liệu đơn hàng (JSON)", data=json.dumps(orders, ensure_ascii=False, indent=2), file_name="moc_cafe_orders.json", mime="application/json")


def show_split():
    st.markdown("""
    <div class="tool-hero">
      <div class="eyebrow">MỘC CAFÉ · TIỆN ÍCH DÀNH CHO BẠN</div>
      <h1 style="font-family:'Playfair Display',serif;margin:0;color:#4b2e23;">Chia tiền nhóm</h1>
      <p style="color:#6f5c4b;margin:.5rem 0 0;">Cùng chia hóa đơn cà phê thật gọn gàng — rõ tiền, vui chuyện.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Công cụ tiện ích ngay trong Mộc Café. VAT và tip được tính theo hóa đơn gốc; mỗi người góp bằng nhau.")
    input_col, result_col = st.columns([0.92, 1.3], gap="large")

    with input_col:
        st.markdown("### 01 · Nhập thông tin")
        with st.container(border=True):
            group_name = st.text_input("Tên nhóm", value=st.session_state.split_group_name, key="split_name")
            st.session_state.split_group_name = group_name
            bill = st.number_input("Tổng hóa đơn (đồng)", min_value=0, value=685000, step=1000, key="split_bill")
            vat_rate = st.number_input("Thuế VAT (%)", min_value=0, max_value=20, value=8, step=1, key="split_vat")
            tip_rate = st.slider("Tiền tip cho nhân viên (%)", min_value=0, max_value=20, value=5, key="split_tip")
            people = st.number_input("Số người", min_value=1, max_value=50, value=7, step=1, key="split_people")

    # Tính toán
    vat_amount = bill * vat_rate // 100
    tip_amount = bill * tip_rate // 100
    total_due = bill + vat_amount + tip_amount
    each_exact = total_due / people
    each_rounded = (int(each_exact) + 999) // 1000 * 1000
    group_collected = each_rounded * people
    group_fund = group_collected - total_due

    bills_50 = each_rounded // 50000
    remainder = each_rounded % 50000
    bills_10 = remainder // 10000
    remainder = remainder % 10000
    bills_1 = remainder // 1000

    with result_col:
        st.markdown(f"### 02 · Kết quả — {group_name or 'Nhóm của bạn'}")
        k1, k2, k3 = st.columns(3)
        k1.metric("Tổng phải trả", money(total_due))
        k2.metric("Mỗi người chính xác", money(each_exact))
        k3.metric("Mỗi người góp", money(each_rounded))
        with st.container(border=True):
            st.markdown("#### Bảng tổng kết")
            st.write(f"Hóa đơn gốc: **{money(bill)}**")
            st.write(f"VAT ({vat_rate}%): **+ {money(vat_amount)}**")
            st.write(f"Tip ({tip_rate}%): **+ {money(tip_amount)}**")
            st.divider()
            st.markdown(f"### Tổng thanh toán: {money(total_due)}")
            st.write(f"{people} người × {money(each_rounded)} = **{money(group_collected)}**")
            st.success(f"Phần dư vào quỹ nhóm: {money(group_fund)}")
        st.markdown("#### 💵 Gợi ý tiền mặt mỗi người")
        cash1, cash2, cash3 = st.columns(3)
        cash1.metric("50.000 đ", f"{bills_50} tờ")
        cash2.metric("10.000 đ", f"{bills_10} tờ")
        cash3.metric("1.000 đ", f"{bills_1} tờ")
        with st.expander("🧠 Góc máy tính: Python đã làm gì?"):
            st.code(
                f"tien_vat = {bill} * {vat_rate} // 100 = {vat_amount}\\n"
                f"tien_tip = {bill} * {tip_rate} // 100 = {tip_amount}\\n"
                f"tong_phai_tra = {bill} + {vat_amount} + {tip_amount} = {total_due}\\n"
                f"moi_nguoi = {total_due} / {people} = {each_exact}\\n"
                f"type(moi_nguoi) -> {type(each_exact).__name__}\\n"
                f"so_nguoi = {int(people)} = {binary_people} (nhị phân) = {hex_people} (thập lục phân)",
                language="text",
            )
    st.divider()
    st.caption("Ghi chú: Làm tròn lên hàng nghìn. Tiền góp dư được đưa vào quỹ nhóm.")



nav()
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "shop":
    show_shop()
elif st.session_state.page == "cart":
    show_cart()
elif st.session_state.page == "split":
    show_split()
elif st.session_state.page == "admin":
    show_admin()
elif st.session_state.page == "confirmation":
    show_confirmation()

st.markdown("""
<div class="site-footer">
  <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.1rem;color:#4b2e23;">MỘC CAFÉ</div>
  <div style="margin-top:.35rem;">Pha bằng sự tử tế · Cà phê ngon, khoảnh khắc lành.</div>
  <div style="height:1px;background:#ddcbb5;margin:.85rem 0;"></div>
  <div style="font-size:.82rem;">Thực đơn · Đặt hàng · Tiện ích chia tiền nhóm</div>
  <div style="font-size:.78rem;color:#857362;margin-top:.25rem;">Vui lòng thay [GẮN LINK ẢNH] bằng đường dẫn ảnh món nước. Thanh toán trực tuyến hiện là chế độ demo.</div>
</div>
""", unsafe_allow_html=True)
