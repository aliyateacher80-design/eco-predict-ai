import streamlit as st
import pandas as pd
import plotly.express as px

# 1. БЕТТІҢ НЕГІЗГІ ПАРАМЕТРЛЕРІ
st.set_page_config(page_title="EcoPredict AI v3.0", layout="wide", page_icon="🌿")

# 🎨 2. ДИЗАЙН (CSS) - Жасыл стиль
st.markdown("""
    <style>
    .stApp { background-color: #f8faf8; }
    .metric-card {
        background: white; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
        border-top: 5px solid #2e7d32;
    }
    h1 { color: #1b5e20; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 🏠 3. HEADER
st.title("🌍 EcoPredict AI: Ресурстарды болжау жүйесі")
st.markdown("<p style='text-align: center;'>Математикалық модельдеу және AI арқылы үнемдеу</p>", unsafe_allow_html=True)

# ⚙️ 4. SIDEBAR - МӘЛІМЕТТЕРДІ ЕНГІЗУ
with st.sidebar:
    st.header("⚙️ Баптаулар")
    st.subheader("Осы айдағы көрсеткіштер:")
    energy = st.number_input("Электр қуаты (кВт/сағ)", value=185)
    water = st.number_input("Су мөлшері (м³)", value=8)
    
    st.markdown("---")
    st.subheader("📊 Салыстыру үшін:")
    last_month_cost = st.number_input("Өткен айдағы төлем (₸)", value=9000)
    
    ppl = st.slider("Отбасы мүшелері", 1, 10, 4)

# 🧠 5. МАТЕМАТИКАЛЫҚ МОДЕЛЬ
current_cost = (energy * 25) + (water * 150)
eco_score = max(0, int(100 - (energy/10 + water*4)))
forecast_cost = current_cost * 1.07  # 7% келесі айға болжам

diff = current_cost - last_month_cost
diff_text = f"{abs(diff)} ₸ үнемделді" if diff < 0 else f"{diff} ₸ артық шығын"
diff_color = "green" if diff < 0 else "red"

# 📊 6. DASHBOARD (НӘТИЖЕЛЕР)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><h3>⚡ Электр</h3><h2 style='color:#2e7d32;'>{energy} кВт</h2><p>{energy*25} ₸</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>💧 Су</h3><h2 style='color:#0277bd;'>{water} м³</h2><p>{water*150} ₸</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>🏆 Eco Score</h3><h2 style='color:#f9a825;'>{eco_score}/100</h2><p style='color:{diff_color};'>{diff_text}</p></div>", unsafe_allow_html=True)

# 📈 7. ВИЗУАЛИЗАЦИЯ (ГРАФИК)
st.subheader("📊 Тұтыну аналитикасы және болжам")
chart_data = pd.DataFrame({
    'Айлар': ['Қазіргі ай', 'Келесі ай (Болжам)'],
    'Шығын (₸)': [current_cost, forecast_cost]
})
fig = px.bar(chart_data, x='Айлар', y='Шығын (₸)', color='Айлар', 
             color_discrete_sequence=['#4caf50', '#ff9800'], text_auto='.0f')
st.plotly_chart(fig, use_container_width=True)

# 🤖 8. AI ADVISOR (КЕҢЕСТЕР)
st.markdown("---")
st.subheader("🤖 Eco AI Advisor ұсыныстары")

if eco_score >= 80:
    st.balloons()
    st.success(f"🎊 Керемет! Сіздің рейтингіңіз: {eco_score}/100. Сіз нағыз Эко-Батырсыз!")
    st.markdown("""
    **Сіздің жетістігіңіз:**
    * ✅ Тұтыну деңгейіңіз өте төмен.
    * 💡 **Кеңес:** Үйдегі құрылғыларды розеткадан суырып жүруді ұмытпаңыз.
    """)
elif 50 <= eco_score < 80:
    st.info(f"⚡ Жақсы нәтиже, бірақ үнемдеуге мүмкіндік бар. Рейтинг: {eco_score}/100")
    st.markdown("""
    **Үнемдеу бойынша ұсыныстар:**
    * 🛍️ **Пластиктен бас тартыңыз:** Дүкенге барғанда пластик пакеттердің орнына **мата шоппер (эко-сөмке)** ұстаңыз.
    * 💧 **Суды үнемдеңіз:** Тіс жуғанда суды жауып қойыңыз.
    """)
else:
    st.warning(f"⚠️ Шығын өте көп! Ресурстарды шұғыл үнемдеу қажет. Рейтинг: {eco_score}/100")
    st.markdown(f"""
    **Шұғыл әрекет ету жоспары:**
    * 💡 **LED шамдарға көшіңіз:** Кәдімгі шамдарды **LED** шамдарға ауыстырыңыз. Олар 10 есе аз энергия жұмсайды.
    * 🚿 **Душ қабылдау:** Ваннаға қарағанда, 5 минуттық душ суды 3 есе аз жұмсайды.
    """)

st.markdown("---")
st.caption("© 2026 EcoPredict AI - Мектеп жобасы")
