import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. БЕТТІҢ НЕГІЗГІ ПАРАМЕТРЛЕРІ
st.set_page_config(page_title="EcoPredict AI v5.2", layout="wide", page_icon="🌿")

# 🎨 2. ДИЗАЙН (CSS)
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

# 📅 ДИНАМИКАЛЫҚ АЙДЫ АНЫҚТАУ
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
st.title("🌍 EcoPredict AI: Коммуналдық шығындар мен ресурстарды болжау")
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Атырау облысының тұрғын үй ерекшеліктеріне негізделген интеллектуалды модель</p>", unsafe_allow_html=True)

# ⚙️ 4. SIDEBAR - ПАРАМЕТРЛЕР ЖӘНЕ ТАРИФТЕР
with st.sidebar:
    st.header("⚙️ Деректерді енгізу")
    
    housing_type = st.radio("🏠 Тұрғын үй түрі:", ("Пәтер (Корпус үй)", "Жер үй"))
    ppl = st.slider("👥 Отбасы мүшелері", 1, 10, 5)
    
    st.markdown("---")
    st.subheader("📊 Ресурс тұтыну мөлшері (Есептеуіш бойынша)")
    
    default_gas = 500 if housing_type == "Жер үй" else 30
    
    energy = st.number_input("⚡ Электр қуаты (кВт/сағ)", value=395, min_value=0)
    water = st.number_input("💧 Су мөлшері (м³)", value=12, min_value=0)
    gas = st.number_input("🔥 Табиғи газ (м³)", value=default_gas, min_value=0)
    
    has_garden = False
    if housing_type == "Жер үй":
        has_garden = st.checkbox("🌻 Бақшаңыз/Жер теліміңіз бар ма?")
    
    st.markdown("---")
    st.subheader("🌐 Бекітілген төлем (Абоненттік)")
    
    wifi_cost = st.number_input("📡 Wi-Fi / Телеком тариф (₸/ай)", value=6500, step=500)

    st.markdown("---")
    st.subheader("💳 Тарифтерді реттеу (₸)")
    
    default_water_tariff = 286.49 if housing_type == "Пәтер (Корпус үй)" else 217.96
    
    LIGHT_TARIFF = st.number_input("⚡ Электр тарифі (₸/кВт)", value=24.50, step=0.1)
    WATER_TARIFF = st.number_input("💧 Су тарифі (₸/м³)", value=default_water_tariff, step=1.0)
    GAS_TARIFF = st.number_input("🔥 Газ тарифі (₸/м³)", value=10.37, step=0.1)

    st.markdown("---")
    last_month_cost = st.number_input("💰 Өткен айдағы жалпы төлем, ₸", value=25000, min_value=0)

# 🧠 5. МАТЕМАТИКАЛЫҚ МОДЕЛЬ (ЖҰМСАРТЫЛҒАН ЛОГИКА)
housing_note = "Су + Канализация" if housing_type == "Пәтер (Корпус үй)" else "Тек су"

# Шығындарды есептеу
current_light_cost = energy * LIGHT_TARIFF
current_water_cost = water * WATER_TARIFF
current_gas_cost = gas * GAS_TARIFF

# Есептеуіш арқылы шығатын ресурстар сомасы
resources_cost = current_light_cost + current_water_cost + current_gas_cost

# Жалпы айлық төлем (Ресурстар + Wi-Fi)
total_current_cost = resources_cost + wifi_cost

# ЖҰМСАРТЫЛҒАН НОРМАЛАР:
energy_limit = ppl * 100  # 70-тен 100 кВт-қа көбейтілді
water_limit = ppl * 5     # 3-тен 5 м³-қа көбейтілді
gas_limit = 600 + (ppl * 30) if housing_type == "Жер үй" else ppl * 15

energy_eff = max(0, 100 - (energy / energy_limit * 100))
water_eff = max(0, 100 - (water / water_limit * 100))
gas_eff = max(0, 100 - (gas / gas_limit * 100))

# +25 БАЗАЛЫҚ БОНУС БАЛЛ
if housing_type == "Жер үй":
    eco_score = int((energy_eff * 0.35) + (water_eff * 0.20) + (gas_eff * 0.45) + 25)
else:
    eco_score = int((energy_eff * 0.40) + (water_eff * 0.35) + (gas_eff * 0.25) + 25)

eco_score = max(0, min(100, eco_score))

# Болжам: Тек есептеуіш ресурстарын 10%-ға үнемдеу
forecast_cost = (resources_cost * 0.90) + wifi_cost

# Салыстыру
diff = total_current_cost - last_month_cost
diff_text = f"{abs(int(diff))} ₸ үнемделді" if diff < 0 else f"{int(diff)} ₸ артық шығын"
diff_color = "#2e7d32" if diff < 0 else "#c62828"

# 📊 6. DASHBOARD
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"<div class='metric-card'><h3>⚡ Электр</h3><h2 style='color:#2e7d32;'>{energy} кВт</h2><p>{current_light_cost:,.0f} ₸</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>💧 Су</h3><h2 style='color:#0277bd;'>{water} м³</h2><p>{current_water_cost:,.0f} ₸</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>🔥 Газ</h3><h2 style='color:#e65100;'>{gas} м³</h2><p>{current_gas_cost:,.0f} ₸</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><h3>📡 Wi-Fi</h3><h2 style='color:#6a1b9a;'>Абонент</h2><p>{wifi_cost:,.0f} ₸</p></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='metric-card'><h3>🏆 Eco Score</h3><h2 style='color:#f9a825;'>{eco_score}/100</h2><p style='color:{diff_color}; font-weight:bold;'>{diff_text}</p></div>", unsafe_allow_html=True)

# 🌳 7. ECO-TREE STATUS (ЖАҢАРТЫЛҒАН ШЕКТЕР)
st.markdown("---")
st.subheader("🌳 Эко-ағаштың күйі")

if eco_score >= 75:
    st.balloons()
    st.markdown("<div class='eco-tree'>🌳🌳🌳</div>", unsafe_allow_html=True)
    st.success(f"Керемет! Сіздің экологиялық жауапкершілігіңіз өте жоғары! (Рейтинг: {eco_score}/100)")
elif 50 <= eco_score < 75:
    st.markdown("<div class='eco-tree'>🌿🌿</div>", unsafe_allow_html=True)
    st.info(f"Жақсы көрсеткіш! Ресурстар ұтымды жұмсалуда, тағы да үнемдеуге болады. (Рейтинг: {eco_score}/100)")
else:
    st.markdown("<div class='eco-tree'>🍂</div>", unsafe_allow_html=True)
    st.warning(f"Абайлаңыз! Ресурстарды шамадан тыс жұмсау байқалады. (Рейтинг: {eco_score}/100)")

# 📈 8. ГРАФИК
st.subheader(f"📊 Шығындар аналитикасы: {current_month_name} vs {next_month_name} (Болжам)")

chart_data = pd.DataFrame({
    'Кезең': [f'{current_month_name} (Жалпы)', f'{next_month_name} (10% Үнем Болжамы)'],
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

# 🤖 9. AI ADVISOR
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
    st.info("🔥 Табиғи газ & 📡 Интернет")
    if gas > gas_limit:
        st.write("🔥 Жер үйде газ шығыны жоғары. **Терморегулятор** қосыңыз.")
    st.write("📡 Wi-Fi тарифін жылына 1 рет тиімді пакеттерге ауыстыру арқылы абоненттік төлемді азайтуға болады.")

st.markdown("<br><p style='text-align: center; color: grey;'>© 2026 EcoPredict AI | Атырау қ. | Информатика секциясы</p>", unsafe_allow_html=True)
