import streamlit as st
import google.generativeai as genai

API_KEY = "AIzaSyAXYmiCr0sZZCLrGbMbbh10wckFm0YUjFU"

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Belalcázar – El Balcón del Paisaje",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS personalizado ─
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

/* Reset y fondo general */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1f0e !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(160deg, #0d1f0e 0%, #132b14 40%, #1a3a1b 100%) !important;
}

/* Ocultar elementos por defecto */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Tipografía base */
* { font-family: 'Lato', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, rgba(13,31,14,0.85) 0%, rgba(20,50,21,0.7) 100%),
                url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Cristo_Rey_Belalc%C3%A1zar.jpg/800px-Cristo_Rey_Belalc%C3%A1zar.jpg') center/cover no-repeat;
    border-radius: 20px;
    padding: 80px 60px;
    text-align: center;
    margin-bottom: 40px;
    border: 1px solid rgba(180,220,100,0.2);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 50%, rgba(180,220,100,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-block;
    background: rgba(180,220,100,0.15);
    border: 1px solid rgba(180,220,100,0.4);
    color: #b4dc64;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 30px;
    margin-bottom: 20px;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    color: #f0f5e8;
    line-height: 1.15;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 20px rgba(0,0,0,0.5);
}

.hero h1 span { color: #b4dc64; }

.hero p {
    font-size: 1.2rem;
    color: rgba(240,245,232,0.75);
    max-width: 560px;
    margin: 0 auto 30px;
    line-height: 1.7;
    font-weight: 300;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
    margin-top: 30px;
}

.stat {
    text-align: center;
}

.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    color: #b4dc64;
    font-weight: 700;
    display: block;
    line-height: 1;
}

.stat-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(240,245,232,0.55);
    margin-top: 6px;
    display: block;
}

/* Sección title */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #f0f5e8;
    text-align: center;
    margin: 50px 0 8px;
}

.section-title span { color: #b4dc64; }

.section-sub {
    text-align: center;
    color: rgba(240,245,232,0.55);
    font-size: 0.95rem;
    margin-bottom: 32px;
    letter-spacing: 0.5px;
}

/* Tarjetas de atractivos */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(180,220,100,0.15);
    border-radius: 16px;
    padding: 28px 24px;
    height: 100%;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #b4dc64, #7ab82f);
    opacity: 0;
    transition: opacity 0.3s;
}

.card:hover {
    background: rgba(180,220,100,0.07);
    border-color: rgba(180,220,100,0.35);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}

.card:hover::before { opacity: 1; }

.card-icon {
    font-size: 2.5rem;
    margin-bottom: 14px;
    display: block;
}

.card-tag {
    display: inline-block;
    background: rgba(180,220,100,0.12);
    border: 1px solid rgba(180,220,100,0.3);
    color: #b4dc64;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
}

.card h3 {
    font-family: 'Playfair Display', serif;
    color: #f0f5e8;
    font-size: 1.2rem;
    margin: 0 0 10px;
}

.card p {
    color: rgba(240,245,232,0.65);
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0;
}

/* Info boxes */
.info-box {
    background: rgba(180,220,100,0.06);
    border: 1px solid rgba(180,220,100,0.2);
    border-left: 4px solid #b4dc64;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.info-box h4 {
    color: #b4dc64;
    margin: 0 0 8px;
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
}

.info-box p {
    color: rgba(240,245,232,0.7);
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* Chat container */
.chat-wrapper {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(180,220,100,0.2);
    border-radius: 20px;
    padding: 32px;
    margin-top: 50px;
}

.chat-header {
    text-align: center;
    margin-bottom: 28px;
}

.chat-header h2 {
    font-family: 'Playfair Display', serif;
    color: #f0f5e8;
    font-size: 1.8rem;
    margin: 0 0 8px;
}

.chat-header p {
    color: rgba(240,245,232,0.55);
    font-size: 0.9rem;
    margin: 0;
}

.ai-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(180,220,100,0.12);
    border: 1px solid rgba(180,220,100,0.3);
    color: #b4dc64;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 16px;
}

/* Mensajes del chat */
.msg-user {
    background: rgba(180,220,100,0.12);
    border: 1px solid rgba(180,220,100,0.25);
    border-radius: 14px 14px 4px 14px;
    padding: 14px 18px;
    margin: 10px 0 10px 60px;
    color: #f0f5e8;
    font-size: 0.93rem;
    line-height: 1.6;
}

.msg-ai {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px 14px 14px 4px;
    padding: 14px 18px;
    margin: 10px 60px 10px 0;
    color: rgba(240,245,232,0.85);
    font-size: 0.93rem;
    line-height: 1.6;
}

.msg-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.msg-label.user { color: #b4dc64; }
msg-label.ai { color: rgba(240,245,232,0.4); }

/* Divider decorativo */
.divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 48px 0;
}

.divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180,220,100,0.3), transparent);
}

.divider-icon {
    color: #b4dc64;
    font-size: 1.2rem;
}

/* Footer */
.footer {
    text-align: center;
    padding: 40px 20px;
    color: rgba(240,245,232,0.3);
    font-size: 0.8rem;
    letter-spacing: 1px;
    border-top: 1px solid rgba(180,220,100,0.1);
    margin-top: 60px;
}

/* Streamlit overrides */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(180,220,100,0.3) !important;
    border-radius: 12px !important;
    color: #f0f5e8 !important;
    font-family: 'Lato', sans-serif !important;
    padding: 12px 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #b4dc64 !important;
    box-shadow: 0 0 0 2px rgba(180,220,100,0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(240,245,232,0.3) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #b4dc64, #7ab82f) !important;
    color: #0d1f0e !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Lato', sans-serif !important;
    letter-spacing: 1px !important;
    padding: 12px 28px !important;
    transition: all 0.3s !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(180,220,100,0.3) !important;
}

[data-testid="stMarkdownContainer"] p {
    color: rgba(240,245,232,0.75);
}

</style>
""", unsafe_allow_html=True)

# ── Inicializar Gemini (AUTO) ─────────────────────────────────────────────────
@st.cache_resource
def init_gemini_auto():
    try:
        genai.configure(api_key=API_KEY)

        # Listar modelos y elegir el primero compatible con generateContent
        models = genai.list_models()

        compatible = []
        for m in models:
            methods = getattr(m, "supported_generation_methods", []) or []
            if "generateContent" in methods:
                compatible.append(m.name)

        if not compatible:
            # Mostrar modelos para depurar
            all_models = [m.name for m in models]
            st.error("No encontré modelos compatibles con generateContent para esta API key.")
            st.write("Modelos detectados:", all_models)
            return None

        selected_model = compatible[0]
        # Mostrar el modelo elegido
        st.write("Modelo seleccionado automáticamente:", selected_model)

        model = genai.GenerativeModel(
            model_name=selected_model,
            system_instruction="""Eres GuíaBot, el asistente turístico oficial de Belalcázar, Caldas, Colombia.
Tu única función es responder preguntas EXCLUSIVAMENTE sobre el turismo de Belalcázar.

Sobre lo que SÍ puedes hablar:
- Atractivos turísticos de Belalcázar (Cristo Rey, La Habana, Eco Parque La Estampilla, La Playa, etc.)
- Gastronomía local caldense
- Actividades y planes (senderismo, pesca deportiva, camping, miradores)
- Hoteles, hospedajes y glamping en Belalcázar
- Cómo llegar a Belalcázar (desde Manizales, Pereira, etc.)
- Historia y cultura del municipio
- Clima y mejor época para visitar
- Festividades y eventos locales
- Paisaje Cultural Cafetero y su relación con Belalcázar

Sobre lo que NO debes hablar:
- Cualquier tema no relacionado con el turismo de Belalcázar
- Política, noticias, tecnología u otros destinos turísticos

Si te preguntan algo fuera del turismo de Belalcázar, responde amablemente:
"Solo puedo ayudarte con información turística de Belalcázar, el Balcón del Paisaje. ¿En qué te puedo orientar sobre este hermoso municipio?"

Responde siempre en español, de manera cálida, entusiasta y profesional. Usa emojis ocasionalmente para hacerlo más ameno."""
        )
        return model

    except Exception as e:
        st.error(f"Error inicializando Gemini: {repr(e)}")
        return None

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🏔️ Caldas · Colombia · Paisaje Cultural Cafetero</div>
    <h1>Belalcázar<br><span>El Balcón del Paisaje</span></h1>
    <p>Donde los valles del Cauca y el Risaralda se encuentran, y el cielo parece más cercano.</p>
    <div class="hero-stats">
        <div class="stat">
            <span class="stat-num">45.5m</span>
            <span class="stat-label">Cristo Rey</span>
        </div>
        <div class="stat">
            <span class="stat-num">27°C</span>
            <span class="stat-label">Temperatura</span>
        </div>
        <div class="stat">
            <span class="stat-num">6</span>
            <span class="stat-label">Departamentos a la vista</span>
        </div>
        <div class="stat">
            <span class="stat-num">40min</span>
            <span class="stat-label">Desde Pereira</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Atractivos Principales ────────────────────────────────────────────────────
st.markdown("""
<div class="section-title">Atractivos <span>Principales</span></div>
<p class="section-sub">Descubre lo que hace único a este rincón del Eje Cafetero</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <span class="card-icon">✝️</span>
        <span class="card-tag">Monumento Histórico</span>
        <h3>Monumento Cristo Rey</h3>
        <p>El Cristo más alto del mundo en su tipo, con 45.5 metros de altura. Único que permite ascender por su interior —154 escalones— hasta contemplar 12 municipios de 6 departamentos.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <span class="card-icon">🌄</span>
        <span class="card-tag">Mirador Natural</span>
        <h3>Mirador La Habana</h3>
        <p>A 5 km del centro urbano, este mirador privilegiado ofrece vistas espectaculares de los valles del Risaralda y Cauca. De noche, los caseríos iluminados crean un espectáculo único.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <span class="card-icon">🌿</span>
        <span class="card-tag">Ecoturismo</span>
        <h3>Eco Parque La Estampilla</h3>
        <p>Reserva forestal de 8 hectáreas con 1.450 metros de sendero ecológico. Ideal para conectar con la fauna y flora local, y observar el nacimiento natural de agua que abastece el municipio.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="card">
        <span class="card-icon">🏖️</span>
        <span class="card-tag">Aventura</span>
        <h3>La Playa del Río Cauca</h3>
        <p>En la vereda La Paloma, una pequeña playa junto al río Cauca. Perfecta para camping, paseos de olla y pesca deportiva. Puedes cruzar el río en garrucha o recorrer la vía férrea en carro de balineras.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
        <span class="card-icon">⛪</span>
        <span class="card-tag">Patrimonio</span>
        <h3>Templo Inmaculada Concepción</h3>
        <p>Joya arquitectónica gótica en el Parque Bolívar. Alberga una valiosa colección de imágenes religiosas importadas de España, incluyendo obras de la Virgen del Carmen y La Inmaculada de Murillo.</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="card">
        <span class="card-icon">☕</span>
        <span class="card-tag">Cultura Cafetera</span>
        <h3>Paisaje Cultural Cafetero</h3>
        <p>Belalcázar es parte del Patrimonio Mundial UNESCO. Sus fincas cafeteras, arquitectura de colonización antioqueña y la calidez de su gente hacen de este lugar una experiencia cultural auténtica.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider">
    <div class="divider-line"></div>
    <span class="divider-icon">⛰️</span>
    <div class="divider-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Información Práctica ──────────────────────────────────────────────────────
st.markdown("""
<div class="section-title">Información <span>Práctica</span></div>
<p class="section-sub">Todo lo que necesitas saber para planear tu visita</p>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div class="info-box">
        <h4>🚗 Cómo Llegar</h4>
        <p>Desde <strong>Pereira:</strong> ~40 minutos por carretera.<br>
        Desde <strong>Manizales:</strong> ~1.5 horas.<br>
        Hay transporte público disponible desde ambas ciudades. También puedes llegar en transporte privado disfrutando las paisajes del Eje Cafetero.</p>
    </div>
    <div class="info-box">
        <h4>🌡️ Clima</h4>
        <p>Temperatura promedio de <strong>27°C</strong>. Clima cálido y agradable durante todo el año. La mejor época para visitar es entre <strong>diciembre y febrero</strong>, y <strong>junio y agosto</strong>, temporadas de menor lluvia.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="info-box">
        <h4>🏨 Hospedaje</h4>
        <p>Belalcázar ofrece hoteles con esencia cafetera, glamping con vistas panorámicas y fincas campestres. La oferta de alojamiento se adapta a todos los presupuestos, desde experiencias rústicas hasta confort moderno.</p>
    </div>
    <div class="info-box">
        <h4>🍽️ Gastronomía</h4>
        <p>Disfruta de la auténtica cocina caldense: <strong>bandeja paisa</strong>, sancocho, mondongo, arepas de chócolo y postres artesanales. Los restaurantes locales preparan los platos con ingredientes frescos de la región.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Actividades ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider">
    <div class="divider-line"></div>
    <span class="divider-icon">🌿</span>
    <div class="divider-line"></div>
</div>
<div class="section-title">Actividades <span>& Experiencias</span></div>
<p class="section-sub">Planes para todos los gustos en el Balcón del Paisaje</p>
""", unsafe_allow_html=True)

act_cols = st.columns(4)
activities = [
    ("🎣", "Pesca Deportiva", "Lagos de Mojarra y Trucha Arco Iris para una tarde de pesca inolvidable."),
    ("🚶", "Senderismo", "Senderos ecológicos con flora y fauna endémica del Eje Cafetero."),
    ("⛺", "Camping", "Zonas habilitadas junto al río Cauca con instalaciones básicas."),
    ("🔭", "Avistamiento", "Observación de aves endémicas y paisajes de los nevados del Ruiz y Tolima."),
]

for col, (icon, title, desc) in zip(act_cols, activities):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <span class="card-icon">{icon}</span>
            <h3 style="font-size:1rem;">{title}</h3>
            <p style="font-size:0.85rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ── Chat con IA ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-wrapper">
    <div class="chat-header">
        <div class="ai-badge">✨ Asistente Turístico · Powered by Gemini</div>
        <h2>¿Tienes preguntas sobre Belalcázar?</h2>
        <p>Nuestro GuíaBot conoce todos los secretos del Balcón del Paisaje. Pregúntale lo que quieras sobre turismo local.</p>
    </div>
""", unsafe_allow_html=True)

# Inicializar historial de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None

# Cargar modelo AUTO
model = init_gemini_auto()

# Mostrar historial
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-label user">Tú</div>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-label ai">🤖 GuíaBot</div>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# Input del chat
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_input = st.text_input(
            "",
            placeholder="Ej: ¿Cómo llego a Cristo Rey? ¿Qué debo comer en Belalcázar?",
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("Preguntar")

if submitted and user_input.strip():
    if model is None:
        st.error("⚠️ No se pudo conectar con Gemini. Verifica la API key y los modelos disponibles.")
    else:
        if st.session_state.gemini_chat is None:
            st.session_state.gemini_chat = model.start_chat(history=[])

        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("GuíaBot está respondiendo..."):
            try:
                response = st.session_state.gemini_chat.send_message(user_input)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"Error Gemini (chat): {repr(e)}"

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# Sugerencias rápidas
st.markdown("""
<p style="text-align:center; color:rgba(240,245,232,0.35); font-size:0.8rem; margin-top:20px; letter-spacing:1px;">
PREGUNTAS FRECUENTES
</p>
""", unsafe_allow_html=True)

sug_cols = st.columns(3)
suggestions = [
    "¿Qué es lo mejor que ver en Belalcázar?",
    "¿Cuál es la mejor época para visitar?",
    "¿Qué actividades hay para hacer en familia?",
]

for col, sug in zip(sug_cols, suggestions):
    with col:
        if st.button(sug, key=f"sug_{sug[:20]}"):
            if model is not None:
                if st.session_state.gemini_chat is None:
                    st.session_state.gemini_chat = model.start_chat(history=[])
                st.session_state.chat_history.append({"role": "user", "content": sug})
                with st.spinner(""):
                    try:
                        response = st.session_state.gemini_chat.send_message(sug)
                        bot_reply = response.text
                    except Exception as e:
                        bot_reply = f"Error Gemini (sugerencia): {repr(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p>⛰️ BELALCÁZAR · EL BALCÓN DEL PAISAJE · CALDAS · COLOMBIA</p>
    <p style="margin-top:8px;">Parte del Paisaje Cultural Cafetero · Patrimonio de la Humanidad UNESCO</p>
</div>
""", unsafe_allow_html=True)