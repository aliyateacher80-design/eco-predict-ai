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
    h1 { color: #1b5e20; text-align: center; }
    .eco-tree { font-size: 50px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 🏠 3. HEADER
st.title("🌍 EcoPredict AI: Ресурстарды болжау жүйесі")
st.markdown("<p style='text-align: center;'>Атырау облысының нақты тарифтеріне негізделген интеллектуалды модель</p>", unsafe_allow_html=True)

# ⚙️ 4. SIDEBAR - БАПТАУЛАР
with st.sidebar:
    st.header("⚙️ Деректерді енгізу")
    st.subheader("Осы айдағы көрсеткіштер:")
    energy = st.number_input("Электр қуаты (кВт/сағ)", value=395)
    water = st.number_input("Су мөлшері (м³)", value=10)
    
    st.markdown("---")
    # Бақшасы бар-жоғын сұрайтын логика
    has_garden = st.checkbox("Бақшаңыз/Жер теліміңіз бар ма?")
    
    st.markdown("---")
    st.subheader("📊 Салыстыру үшін:")
    last_month_cost = st.number_input("Өткен айдағы жалпы төлем, ₸", value=12000)
    ppl = st.slider("Отбасы мүшелері", 1, 10, 7)

# 🧠 5. МАТЕМАТИКАЛЫҚ МОДЕЛЬ (НАҚТЫ ТАРИФТЕР)
# Түбіртек негізіндегі тарифтер (Тұрақты мәндер)
LIGHT_TARIFF = 24.5
WATER_TOTAL_TARIFF = 286.49 # Су (217.96) + Канализация (68.53)

# Тұтынуды есептеу
current_light_cost = energy * LIGHT_TARIFF
current_water_cost = water * WATER_TOTAL_TARIFF
total_current_cost = current_light_cost + current_water_cost

# Электр нормасы - адам басына 70 кВт, Су нормасы - адам басына 3 м3
energy_limit = ppl * 70
water_limit = ppl * 3

# Рейтинг (Eco Score) логикасы - Шек 60-қа түсірілген
energy_efficiency = max(0, 100 - (energy / energy_limit * 100))
water_efficiency = max(0, 100 - (water / water_limit * 100))
eco_score = int((energy_efficiency + water_efficiency) / 2 + 15)
eco_score = min(100, eco_score)

# Келесі айға болжам
forecast_cost = total_current_cost * 0.95 

# Айырмашылықты есептеу
diff = total_current_cost - last_month_cost
diff_text = f"{abs(int(diff))} ₸ үнемделді" if diff < 0 else f"{int(diff)} ₸ артық шығын"
diff_color = "green" if diff < 0 else "red"

# 📊 6. DASHBOARD (РЕСУРСТАРДЫ БӨЛЕК КӨРСЕТУ)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><h3>⚡ Электр (Нақты)</h3><h2 style='color:#2e7d32;'>{energy} кВт</h2><p>{current_light_cost:.2f} ₸</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>💧 Су + Канализация</h3><h2 style='color:#0277bd;'>{water} м³</h2><p>{current_water_cost:.2f} ₸</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>🏆 Eco Score</h3><h2 style='color:#f9a825;'>{eco_score}/100</h2><p style='color:{diff_color};'>{diff_text}</p></div>", unsafe_allow_html=True)

# 🌳 7. ECO-TREE STATUS (Рейтинг 60-тан төмен болса - Абайлаңыз)
st.markdown("---")
st.subheader("🌳 Эко-ағаштың күйі")
if eco_score >= 80:
    st.balloons()
    st.markdown("<div class='eco-tree'>🌳🌳🌳</div>", unsafe_allow_html=True)
    st.success(f"Керемет! Сіз нақты үнемшілсіз! (Рейтинг: {eco_score}/100)")
elif 60 <= eco_score < 80:
    st.markdown("<div class='eco-tree'>🌿🌿</div>", unsafe_allow_html=True)
    st.info(f"Орташа көрсеткіш. (Рейтинг: {eco_score}/100)")
else:
    st.markdown("<div class='eco-tree'>🍂</div>", unsafe_allow_html=True)
    st.warning(f"Абайлаңыз! Ресурстарды көп жұмсау байқалады. (Рейтинг: {eco_score}/100)")

# 📈 8. ГРАФИК (АНАЛИТИКА)
st.subheader("📊 Тұтыну аналитикасы: Осы ай vs Келесі ай")
chart_data = pd.DataFrame({
    'Айлар': ['Сәуір (Нақты)', 'Мамыр (Болжам)'],
    'Шығын (₸)': [total_current_cost, forecast_cost]
})
fig = px.bar(chart_data, x='Айлар', y='Шығын (₸)', color='Айлар', 
             color_discrete_sequence=['#4caf50', '#ff9800'], text_auto='.0f')
st.plotly_chart(fig, use_container_width=True)

# 🤖 9. AI ADVISOR - ИНТЕЛЛЕКТУАЛДЫ ҰСЫНЫСТАР
st.markdown("---")
st.subheader("🤖 Eco AI Advisor ұсыныстары")

col_adv1, col_adv2 = st.columns(2)

with col_adv1:
    st.info("💡 Ток бойынша кеңестер")
    if energy > energy_limit:
        st.write("* ⚠️ Сізде ток шығыны нормадан жоғары. **LED шамдарын** қолдануды ұсынамыз.")
    st.write("* 🔌 Құрылғыларды **күту режимінен (standby)** ажырату айына 5-10% үнем береді.")
    st.write("* 🧼 Кір жуғыш машинаны толық толғанда ғана қосыңыз.")

with col_adv2:
    st.info("💧 Су бойынша кеңестер")
    # Су тұтыну 15 кубтан асса және бақшасы болса шығатын арнайы ұсыныс
    if water >= 15:
        st.error("❗ Су тұтыну деңгейі өте жоғары (15 м³-ден асты)!")
        if has_garden:
            st.success("🌻 **Маман ұсынысы:** Егер сізде бақша болса, суару жүйесін **тамшылатуға** ауыстырыңыз. Бұл шығынды еселеп азайтады.")
    elif water > water_limit:
        st.write("* 🚿 Ваннаның орнына 5 минуттық душ қабылдауды әдетке айналдырыңыз.")
    st.write("* 🚰 Тіс жуу кезінде суды жауып қоюды ұмытпаңыз.")

st.markdown("<p style='text-align: center; color: grey;'>© 2026 EcoPredict AI | Атырау қ. | Информатика жобасы</p>", unsafe_allow_html=True)
