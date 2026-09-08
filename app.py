import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. БЕТТІҢ НЕГІЗГІ ПАРАМЕТРЛЕРІ
st.set_page_config(page_title="EcoPredict AI v4.5", layout="wide", page_icon="🌿")

# 🎨 2. ДИЗАЙН (CSS) - Интерфейсті жақсарту
st.markdown("""
    <style>
    .stApp { background-color: #f8faf8; }
    .metric-card {
        background: white; border-radius: 15px; padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
        border-top: 5px solid #2e7d32;
    }
    h1 { color: #1b5e20; text-align: center; font-weight: bold; }
    .eco-tree { font-size: 60px; text-align: center; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# 📅 ДИНАМИКАЛЫҚ АЙДЫ АНЫҚТАУ (ҚАЖЕТТІ АЙ АВТОМАТТЫ ТҮРДЕ ШЫҒАДЫ)
MONTH_NAMES = {
    1: "Қаңтар", 2: "Ақпан", 3: "Наурыз", 4: "Сәуір",
    5: "Мамыр", 6: "Маусым", 7: "Шілде", 8: "Тамыз",
    9: "Қыркүйек", 10: "Қазан", 11: "Қараша", 12: "Желтоқсан"
}

now = datetime.now()
current_month_num = now.month
next_month_num = (current_month_num % 12) + 1

current_month_name = MONTH_NAMES[current_month_num]
next_month_name = MONTH_NAMES[next_month_num]

# 🏠 3. HEADER
st.title("🌍 EcoPredict AI: Ресурстарды болжау жүйесі")
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Атырау облысының тұрғын үй ерекшеліктеріне негізделген интеллектуалды модель</p>", unsafe_allow_html=True)

# ⚙️ 4. SIDEBAR - ПАРАМЕТРЛЕР (3 РЕСУРС БӨЛЕК ЕНГІЗІЛЕДІ)
with st.sidebar:
    st.header("⚙️ Деректерді енгізу")
    
    # Тұрғын үй түрін таңдау логикасы
    housing_type = st.radio("🏠 Тұрғын үй түрі:", ("Пәтер (Корпус үй)", "Жер үй"))
    
    st.markdown("---")
    energy = st.number_input("⚡ Электр қуаты (кВт/сағ)", value=395, min_value=0)
    water = st.number_input("💧 Су мөлшері (м³)", value=10, min_value=0)
    gas = st.number_input("🔥 Табиғи газ (м³)", value=120, min_value=0)
    
    # Жер үйлер үшін бақша сұрағын шығару
    has_garden = False
    if housing_type == "Жер үй":
        has_garden = st.checkbox("🌻 Бақшаңыз/Жер теліміңіз бар ма?")
    
    st.markdown("---")
    ppl = st.slider("👥 Отбасы мүшелері", 1, 10, 5)
    last_month_cost = st.number_input("💰 Өткен айдағы жалпы төлем, ₸", value=16000, min_value=0)

# 🧠 5. МАТЕМАТИКАЛЫҚ МОДЕЛЬ (ДИНАМИКАЛЫҚ ТАРИФТЕР)
LIGHT_TARIFF = 24.5
GAS_TARIFF = 11.23  # Атырау облысы бойынша табиғи газ тарифи (₸/м³)

# Тұрғын үй түріне қарай тарифті анықтау
if housing_type == "Пәтер (Корпус үй)":
    WATER_TARIFF = 286.49  # Су (217.96) + Канализация (68.53)
    housing_note = "Тариф: Су + Канализация"
else:
    WATER_TARIFF = 217.96  # Тек пайдаланған суға (Жер үй)
    housing_note = "Тариф: Тек су (Канализациясыз)"

# Шығындарды есептеу (Ток + Су + Газ)
current_light_cost = energy * LIGHT_TARIFF
current_water_cost = water * WATER_TARIFF
current_gas_cost = gas * GAS_TARIFF
total_current_cost = current_light_cost + current_water_cost + current_gas_cost

# Рейтинг (Eco Score) логикасы
energy_limit = ppl * 70  # Адам басына норма (кВт/сағ)
water_limit = ppl * 3    # Адам басына норма (м³)
gas_limit = ppl * 25     # Адам басына норма (м³)

energy_eff = max(0, 100 - (energy / energy_limit * 100))
water_eff = max(0, 100 - (water / water_limit * 100))
gas_eff = max(0, 100 - (gas / gas_limit * 100))

eco_score = int((energy_eff + water_eff + gas_eff) / 3 + 15)
eco_score = max(0, min(100, eco_score))

# Болжам (Келесі айға 10% үнемдеу мүмкіндігімен)
forecast_cost = total_current_cost * 0.90 

# Салыстыру
diff = total_current_cost - last_month_cost
diff_text = f"{abs(int(diff))} ₸ үнемделді" if diff < 0 else f"{int(diff)} ₸ артық шығын"
diff_color = "#2e7d32" if diff < 0 else "#c62828"

# 📊 6. DASHBOARD (4 РЕСУРС БАҒАНЫ)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><h3>⚡ Электр</h3><h2 style='color:#2e7d32;'>{energy} кВт</h2><p>{current_light_cost:,.2f} ₸</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>💧 Су</h3><h2 style='color:#0277bd;'>{water} м³</h2><p>{current_water_cost:,.2f} ₸</p><small style='color:gray;'>{housing_note}</small></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>🔥 Газ</h3><h2 style='color:#e65100;'>{gas} м³</h2><p>{current_gas_cost:,.2f} ₸</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h3>🏆 Eco Score</h3><h2 style='color:#f9a825;'>{eco_score}/100</h2><p style='color:{diff_color}; font-weight:bold;'>{diff_text}</p></div>", unsafe_allow_html=True)

# 🌳 7. ECO-TREE STATUS
st.markdown("---")
st.subheader("🌳 Эко-ағаштың күйі")

if eco_score >= 80:
    st.balloons()
    st.markdown("<div class='eco-tree'>🌳🌳🌳</div>", unsafe_allow_html=True)
    st.success(f"Керемет! Сіздің экологиялық жауапкершілігіңіз өте жоғары! (Рейтинг: {eco_score}/100)")
elif 60 <= eco_score < 80:
    st.markdown("<div class='eco-tree'>🌿🌿</div>", unsafe_allow_html=True)
    st.info(f"Жақсы көрсеткіш, бірақ ресурстарды одан әрі үнемдеуге мүмкіндік бар. (Рейтинг: {eco_score}/100)")
else:
    st.markdown("<div class='eco-tree'>🍂</div>", unsafe_allow_html=True)
    st.warning(f"Абайлаңыз! Ресурстарды шамадан тыс жұмсау байқалады. (Рейтинг: {eco_score}/100)")

# 📈 8. ГРАФИК (ЖҮЙЕЛІК ДИНАМИКАЛЫҚ АЙЛАРМЕН)
st.subheader(f"📊 Шығындар аналитикасы: {current_month_name} vs {next_month_name} (Болжам)")

chart_data = pd.DataFrame({
    'Кезең': [f'{current_month_name} (Нақты)', f'{next_month_name} (10% Болжам)'],
    'Шығын (₸)': [total_current_cost, forecast_cost]
})

fig = px.bar(
    chart_data, 
    x='Кезең', 
    y='Шығын (₸)', 
    color='Кезең', 
    color_discrete_sequence=['#2e7d32', '#f9a825'], 
    text_auto='.0f'
)
fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Сомасы (₸)")
st.plotly_chart(fig, use_container_width=True)

# 🤖 9. AI ADVISOR - ИНТЕЛЛЕКТУАЛДЫ ҰСЫНЫСТАР
st.markdown("---")
st.subheader("🤖 Eco AI Advisor интеллектуалды ұсыныстары")

col_adv1, col_adv2, col_adv3 = st.columns(3)

with col_adv1:
    st.info("💡 Электр энергиясы")
    if energy > energy_limit:
        st.write("⚠️ Сізде ток шығыны нормадан жоғары. **LED шамдарын** қолдануды ұсынамыз.")
    st.write("🔌 Құрылғыларды **күту режимінен** ажырату айына 5-10% үнем береді.")

with col_adv2:
    st.info("💧 Су ресурстары")
    if water >= 15 and housing_type == "Жер үй" and has_garden:
        st.success("🌻 **МАМАН КЕҢЕСІ:** Бақшаны **тамшылатып суаруға** ауыстырыңыз!")
    elif water > water_limit:
        st.write("🚿 Ваннаның орнына 5 минуттық душ қабылдаңыз.")

with col_adv3:
    st.info("🔥 Табиғи газ")
    if gas > gas_limit:
        st.write("⚠️ Газ шығыны жоғары. Жылыту қазанын (котел) **терморегуляторға** қосыңыз.")
    st.write("🏠 Терезелер мен есіктерді жылылау газ шығынын 15–20%-ға азайтады.")

st.markdown("<br><p style='text-align: center; color: grey;'>© 2026 EcoPredict AI | Атырау қ. | Информатика секциясы</p>", unsafe_allow_html=True)
