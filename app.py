import streamlit as st
import pandas as pd
import plotly.express as px

# 1. БЕТТІҢ НЕГІЗГІ ПАРАМЕТРЛЕРІ
st.set_page_config(page_title="EcoPredict AI v3.0", layout="wide", page_icon="🌿")

# 🎨 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8faf8; }
    .metric-card {
        background: white; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
        border-top: 5px solid #2e7d32;
    }
    .impact-card {
        background: #e8f5e9; border-radius: 10px; padding: 15px;
        text-align: center; border: 1px dashed #2e7d32;
    }
    h1 { color: #1b5e20; text-align: center; }
    .eco-tree { font-size: 50px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 🏠 3. HEADER
st.title("🌍 EcoPredict AI: Ресурстарды болжау жүйесі")
st.markdown("<p style='text-align: center;'>Математикалық модельдеу және AI арқылы үнемдеу</p>", unsafe_allow_html=True)

# ⚙️ 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Баптаулар")
    st.subheader("Осы айдағы көрсеткіштер:")
    energy = st.number_input("Электр қуаты (кВт/сағ)", value=143)
    water = st.number_input("Су мөлшері (м³)", value=4)
    
    st.markdown("---")
    st.subheader("📊 Салыстыру үшін:")
    last_month_cost = st.number_input("Өткен айдағы төлем (су + ток), ₸", value=8000)
    
    ppl = st.slider("Отбасы мүшелері", 1, 10, 3)

# 🧠 5. МАТЕМАТИКАЛЫҚ МОДЕЛЬ
current_cost = (energy * 25) + (water * 150)

# Электр нормасы - 200 кВт, Су нормасы - 12 м3 (ТҮЗЕТІЛДІ)
energy_efficiency = max(0, 100 - (energy / 200 * 100))
water_efficiency = max(0, 100 - (water / 12 * 100))

# Eco Score есептеу
eco_score = int((energy_efficiency + water_efficiency) / 2 + 30)
eco_score = min(100, eco_score)

# Экологиялық әсерді есептеу (Көрнекі болуы үшін қосылды)
# 1 кВт үнемдеу = 0.5 кг CO2 азайту, 1 м3 үнемдеу = 0.3 кг CO2 азайту
co2_saved = max(0, (200 - energy) * 0.5 + (12 - water) * 0.3)
virtual_trees = int(co2_saved / 2) # Әр 2 кг CO2 = 1 виртуалды ағаш

diff = current_cost - last_month_cost
diff_text = f"{abs(diff)} ₸ үнемделді" if diff < 0 else f"{diff} ₸ артық шығын"
diff_color = "green" if diff < 0 else "red"

# 📊 6. DASHBOARD (НЕГІЗГІ КӨРСЕТКІШТЕР)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><h3>⚡ Электр</h3><h2 style='color:#2e7d32;'>{energy} кВт</h2><p>{energy*25} ₸</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>💧 Су</h3><h2 style='color:#0277bd;'>{water} м³</h2><p>{water*150} ₸</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>🏆 Eco Score</h3><h2 style='color:#f9a825;'>{eco_score}/100</h2><p style='color:{diff_color};'>{diff_text}</p></div>", unsafe_allow_html=True)

# 🌱 7. ЖАҢА: ЭКОЛОГИЯЛЫҚ ӘСЕР (КӨРНЕКІ БӨЛІМ)
st.markdown("---")
st.subheader("🍃 Сіздің экологиялық үлесіңіз (AI есептеуі)")
ecol1, ecol2 = st.columns(2)
with ecol1:
    st.markdown(f"<div class='impact-card'>☁️ <b>Азайтылған CO2:</b><br><h2>{co2_saved:.1f} кг</h2></div>", unsafe_allow_html=True)
with ecol2:
    st.markdown(f"<div class='impact-card'>🌳 <b>Сақталған ағаштар:</b><br><h2>{virtual_trees} ағаш</h2></div>", unsafe_allow_html=True)

# 🌳 8. ЖАСЫЛ АҒАШ СТАТУСЫ
st.markdown("---")
st.subheader("🌳 Эко-ағаштың күйі")
if eco_score >= 70:
    st.balloons()
    st.markdown("<div class='eco-tree'>🌳🌳🌳</div>", unsafe_allow_html=True)
    st.success("Керемет! Сіздің ағашыңыз жайқалып тұр!")
elif 40 <= eco_score < 70:
    st.markdown("<div class='eco-tree'>🌿🌿</div>", unsafe_allow_html=True)
    st.info("Жақсы, ағашыңыз өсіп келеді.")
else:
    st.markdown("<div class='eco-tree'>🍂</div>", unsafe_allow_html=True)
    st.warning("Абайлаңыз! Ағаш қурай бастады.")

# 📈 9. ГРАФИК
st.subheader("📊 Шығындарды салыстыру")
chart_data = pd.DataFrame({
    'Айлар': ['Осы ай', 'Өткен ай'],
    'Шығын (₸)': [current_cost, last_month_cost]
})
fig = px.bar(chart_data, x='Айлар', y='Шығын (₸)', color='Айлар', 
             color_discrete_sequence=['#4caf50', '#9e9e9e'], text_auto='.0f')
st.plotly_chart(fig, use_container_width=True)

st.markdown("<p style='text-align: center; color: grey;'>© 2026 EcoPredict AI - Мектеп жобасы</p>", unsafe_allow_html=True)
