import os
import json
import hmac
import hashlib
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Mộc Café | Cà phê tử tế", page_icon="☕", layout="wide")

DATA_FILE = Path("orders.json")
ADMIN_USER = os.getenv("COFFEE_ADMIN_USER", "AdminCoffeeShop@")
ADMIN_PASSWORD = os.getenv("COFFEE_ADMIN_PASSWORD", "12345678_")

PRODUCTS = [
    {"id": "espresso", "name": "Espresso", "subtitle": "Đậm đà • Đánh thức giác quan", "price": 39000, "image": "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?auto=format&fit=crop&w=1000&q=85", "tag": "BESTSELLER"},
    {"id": "americano", "name": "Americano", "subtitle": "Thanh nhẹ • Hậu vị cân bằng", "price": 42000, "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=1000&q=85", "tag": "NHẸ NHÀNG"},
    {"id": "latte", "name": "Café Latte", "subtitle": "Espresso hòa quyện sữa mịn", "price": 49000, "image": "https://images.unsplash.com/photo-1561882468-9110e03e0f78?auto=format&fit=crop&w=1000&q=85", "tag": "ĐƯỢC YÊU THÍCH"},
    {"id": "cappuccino", "name": "Cappuccino", "subtitle": "Bọt sữa bồng bềnh • Thơm dịu", "price": 49000, "image": "https://images.unsplash.com/photo-1572445420243-3e9b8e7c9b36?auto=format&fit=crop&w=1000&q=85", "tag": "CỔ ĐIỂN"},
    {"id": "mocha", "name": "Mocha", "subtitle": "Cà phê • Chocolate • Sữa", "price": 55000, "image": "https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?auto=format&fit=crop&w=1000&q=85", "tag": "NGỌT NGÀO"},
    {"id": "coldbrew", "name": "Cold Brew", "subtitle": "Ủ lạnh êm dịu • Mát lành", "price": 52000, "image": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=1000&q=85", "tag": "Ủ LẠNH"},
    {"id": "vietnamese", "name": "Cà phê sữa đá", "subtitle": "Đậm vị Việt • Ngọt béo hài hòa", "price": 35000, "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1000&q=85", "tag": "VỊ VIỆT"},
    {"id": "coconut", "name": "Cà phê cốt dừa", "subtitle": "Béo thơm • Mát lạnh", "price": 59000, "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1000&q=85", "tag": "ĐẶC BIỆT"},
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

init_state()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root { --coffee:#4b2e23; --cream:#fbf6ee; --copper:#bd8055; }
.stApp { background: #fbf8f2; color: #30251f; font-family:'DM Sans',sans-serif; }
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
</style>
""", unsafe_allow_html=True)

def nav():
    left, right = st.columns([4, 3])
    with left:
        st.markdown("## ☕ MỘC **CAFÉ**")
        st.caption("Một chút chậm rãi, một ngụm an yên.")
    with right:
        cols = st.columns(4)
        for col, label, page in zip(cols, ["Trang chủ", "Thực đơn", "Giỏ hàng", "Admin"], ["home", "shop", "cart", "admin"]):
            with col:
                if st.button(label, key=f"nav_{page}", use_container_width=True):
                    st.session_state.page = page
                    st.rerun()
    st.divider()

def show_home():
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Roasted with care • Brewed for you</div>
      <h1>Mỗi ngày,<br>một ly thật ngon.</h1>
      <p>Những hạt cà phê được chọn kỹ, pha bằng sự tận tâm. Dừng lại một chút và thưởng thức khoảnh khắc của riêng bạn.</p>
    </div>""", unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
