import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. БЕТТІҢ НЕГІЗГІ ПАРАМЕТРЛЕРІ
st.set_page_config(page_title="EcoPredict AI", layout="wide", page_icon="🌿")

# 🎨 2. ЕҢ ӘДЕМІ SOFT DARK / GLASSMORPHISM СТИЛІ (АППАҚ ЕМЕС, СӘНДІ ФОН)
st.markdown("""
    <style>
    /* Негізгі артқы фон (Жұмсақ күңгірт-жасыл градиент) */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Сайдбар стилі */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Сәнді мөлдір Карточкалар (Glassmorphism Effect) */
    .metric-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 22px 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 5px 0;
    }
    .metric-sub {
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Шеткі түсті индикаторлар */
    .card-light { border-top: 4px solid #10b981; }
    .card-water { border-top: 4px solid #38bdf8; }
    .card-gas { border-top: 4px solid #fb923c; }
    .card-wifi { border-top: 4px solid #c084fc; }
    .card-score { border-top: 4px solid #facc15; }
    
    /* Эко-ағаш секциясы */
    .eco-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
        text-align: center;
    }
    .eco-tree-icon {
        font-size: 65px;
        margin: 10px 0;
    }
    
    /* Сәнді Прогресс-бар */
    .progress-bar-bg {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 50px;
        height: 14px;
        width: 100%;
        overflow: hidden;
        margin: 15px 0;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 50px;
        transition: width 0.8s ease-in-out;
    }
    
    /* Текстерді ақ түске реттеу */
    h1, h2, h3, h4, p, span {
        color: #f8fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 📅 ДИНАМИКАЛЫҚ АЙДЫ АНЫҚТАУ
MONTH_NAMES = {
    1: "Қаңтар", 2: "Ақпан", 3: "Наурыз", 4: "Сәуір",
    5: "Мамыр", 6: "Маусым", 7: "Шілде", 8: "Тамыз",
    9: "Қыркүйек", 10: "Қараша", 11: "Қараша", 12: "Желтоқсан"
}

now = datetime.now()
current_month_num = now.month
next_month_num = (current_month_num % 12) + 1

current_month_name = MONTH_NAMES[current_month_num]
next_month_name = MONTH_NAMES[next_month_num]

# 🏠 3. HEADER
st.markdown("<h1 style='text-align: center; font-size: 2.5rem; font-weight: 800;'>🌿 EcoPredict AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #cbd5e1 !important; font-size: 1.1rem; margin-bottom: 30px;'>Атырау облысы бойынша коммуналдық шығындар мен ресурстарды интеллектуалды аналитикалау</p>", unsafe_allow_html=True)

# ⚙️ 4. SIDEBAR
with st.sidebar:
    st.header("⚙️ Енгізу панелі")
    
    housing_type = st.radio("🏠 Тұрғын үй түрі:", ("Пәтер (Корпус үй)", "Жер үй"))
    ppl = st.slider("👥 Отбасы мүшелері", 1, 10, 5)
    
    st.markdown("---")
    st.subheader("📊 Ресурс тұтыну (Есептеуіш)")
    
    default_gas = 350 if housing_type == "Жер үй" else 30
    
    energy = st.number_input("⚡ Электр қуаты (кВт/сағ)", value=220, min_value=0, step=10)
    water = st.number_input("💧 Су мөлшері (м³)", value=12, min_value=0, step=1)
    gas = st.number_input("🔥 Табиғи газ (м³)", value=default_gas, min_value=0, step=10)
    
    has_garden = False
    if housing_type == "Жер үй":
        has_garden = st.checkbox("🌻 Бақша / Жер телімі бар")
    
    st.markdown("---")
    st.subheader("🌐 Бекітілген төлем")
    wifi_cost = st.number_input("📡 Wi-Fi / Телеком (₸/ай)", value=6500, step=500)

    st.markdown("---")
    st.subheader("💳 Тарифтер (₸)")
    default_water_tariff = 286.49 if housing_type == "Пәтер (Корпус үй)" else 217.96
    
    LIGHT_TARIFF = st.number_input("⚡ Электр (₸/кВт)", value=24.50, step=0.1)
    WATER_TARIFF = st.number_input("💧 Су (₸/м³)", value=default_water_tariff, step=1.0)
    GAS_TARIFF = st.number_input("🔥 Газ (₸/м³)", value=10.37, step=0.1)

    st.markdown("---")
    last_month_cost = st.number_input("💰 Өткен айдағы төлем, ₸", value=25000, min_value=0)

# 🧠 5. МАТЕМАТИКАЛЫҚ МОДЕЛЬ
current_light_cost = energy * LIGHT_TARIFF
current_water_cost = water * WATER_TARIFF
current_gas_cost = gas * GAS_TARIFF

resources_cost = current_light_cost + current_water_cost + current_gas_cost
total_current_cost = resources_cost + wifi_cost

energy_limit = ppl * 80
water_limit = ppl * 4
gas_limit = (300 + (ppl * 20)) if housing_type == "Жер үй" else (ppl * 12)

energy_eff = max(0, 100 - (energy / energy_limit * 100))
water_eff = max(0, 100 - (water / water_limit * 100))
gas_eff = max(0, 100 - (gas / gas_limit * 100))

if housing_type == "Жер үй":
    eco_score = int((energy_eff * 0.35) + (water_eff * 0.25) + (gas_eff * 0.40) + 10)
else:
    eco_score = int((energy_eff * 0.45) + (water_eff * 0.35) + (gas_eff * 0.20) + 10)

eco_score = max(0, min(100, eco_score))
forecast_cost = (resources_cost * 0.90) + wifi_cost

diff = total_current_cost - last_month_cost
diff_text = f"{abs(int(diff))} ₸ үнемделді" if diff < 0 else f"{int(diff)} ₸ артық шығын"
diff_color = "#34d399" if diff < 0 else "#f87171"

# 📊 6. СӘНДІ DASHBOARD CARDS
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class='metric-card card-light'>
            <div class='metric-title'>⚡ Электр</div>
            <div class='metric-value' style='color: #34d399;'>{energy} <span style='font-size: 1rem;'>кВт</span></div>
            <div class='metric-sub'>{current_light_cost:,.0f} ₸</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card card-water'>
            <div class='metric-title'>💧 Су</div>
            <div class='metric-value' style='color: #38bdf8;'>{water} <span style='font-size: 1rem;'>м³</span></div>
            <div class='metric-sub'>{current_water_cost:,.0f} ₸</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='metric-card card-gas'>
            <div class='metric-title'>🔥 Табиғи газ</div>
            <div class='metric-value' style='color: #fb923c;'>{gas} <span style='font-size: 1rem;'>м³</span></div>
            <div class='metric-sub'>{current_gas_cost:,.0f} ₸</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='metric-card card-wifi'>
            <div class='metric-title'>📡 Wi-Fi</div>
            <div class='metric-value' style='color: #c084fc;'>Абонент</div>
            <div class='metric-sub'>{wifi_cost:,.0f} ₸</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class='metric-card card-score'>
            <div class='metric-title'>🏆 Eco Score</div>
            <div class='metric-value' style='color: #facc15;'>{eco_score}<span style='font-size: 1.2rem;'>/100</span></div>
            <div class='metric-sub' style='color: {diff_color}; font-weight: bold;'>{diff_text}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 🌳 7. ECO-TREE STATUS
if eco_score >= 70:
    tree_icon = "🌳🌳🌳"
    status_title = "Керемет көрсеткіш!"
    status_desc = "Ресурстар өте үнемді жұмсалуда. Экологиялық жауапкершілігіңіз жоғары."
    bar_color = "#34d399"
elif 45 <= eco_score < 70:
    tree_icon = "🌿🌿"
    status_title = "Жақсы орташа деңгей!"
    status_desc = "Ресурстар ұтымды жұмсалуда, бірақ әлі де үнемдеуге мүмкіндік бар."
    bar_color = "#fbbf24"
else:
    tree_icon = "🍂"
    status_title = "Ресурстарды тұтыну жоғары!"
    status_desc = "Абайлаңыз! Белгіленген нормалардан асу байқалады."
    bar_color = "#f87171"

st.markdown(f"""
    <div class='eco-container'>
        <h3 style='margin: 0; font-weight: 700;'>🌳 Эко-ағаштың күйі</h3>
        <div class='eco-tree-icon'>{tree_icon}</div>
        <h4 style='color: {bar_color} !important; margin: 5px 0;'>{status_title} (Рейтинг: {eco_score}/100)</h4>
        <p style='color: #cbd5e1 !important; font-size: 0.95rem;'>{status_desc}</p>
        <div class='progress-bar-bg'>
            <div class='progress-bar-fill' style='width: {eco_score}%; background-color: {bar_color};'></div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 📈 8. ГРАФИК (DARK THEME)
st.markdown(f"<h3 style='font-size: 1.3rem; font-weight: 700;'>📊 Шығындар аналитикасы: {current_month_name} vs {next_month_name} (Болжам)</h3>", unsafe_allow_html=True)

chart_data = pd.DataFrame({
    'Кезең': [f'{current_month_name} (Ағымдағы)', f'{next_month_name} (10% Үнем Болжамы)'],
    'Шығын (₸)': [total_current_cost, forecast_cost]
})

fig = px.bar(
    chart_data, 
    x='Кезең', 
    y='Шығын (₸)', 
    color='Кезең', 
    color_discrete_sequence=['#34d399', '#facc15'], 
    text_auto='.0f'
)
fig.update_layout(
    showlegend=False, 
    xaxis_title="", 
    yaxis_title="Сомасы (₸)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", size=14, color="#f8fafc")
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')

st.plotly_chart(fig, use_container_width=True)

# 🤖 9. AI ADVISOR
st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 1.3rem; font-weight: 700;'>🤖 Eco AI Advisor ұсыныстары</h3>", unsafe_allow_html=True)

col_adv1, col_adv2, col_adv3 = st.columns(3)

with col_adv1:
    st.info("💡 **Электр энергиясы**")
    if energy > energy_limit:
        st.write("⚠️ Электр шығыны нормадан жоғары. LED шамдарға ауысуды ұсынамыз.")
    st.write("🔌 Құрылғыларды «күту режимінен» ажырату айына 5-10% үнем береді.")

with col_adv2:
    st.info("💧 **Су ресурстары**")
    if water >= 15 and housing_type == "Жер үй" and has_garden:
        st.success("🌻 Бақшаны тамшылатып суаруға ауыстыру тиімді.")
    elif water > water_limit:
        st.write("🚿 Ваннаның орнына 5 минуттық душ қабылдаңыз.")

with col_adv3:
    st.info("🔥 **Газ & Интернет**")
    if gas > gas_limit:
        st.write("🔥 Газ шығыны жоғары. Терморегулятор қосу ұсынылады.")
    st.write("📡 Wi-Fi тарифін жылына 1 рет қайта қарап тұрыңыз.")

st.markdown("<br><p style='text-align: center; color: #64748b !important; font-size: 0.85rem;'>© 2026 EcoPredict AI | Атырау қ. | Информатика секциясы</p>", unsafe_allow_html=True)
