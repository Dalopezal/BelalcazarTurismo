# 🏔️ Belalcázar - El Balcón del Paisaje

Aplicación web de turismo para Belalcázar, Caldas, con asistente de IA (GuíaBot) impulsado por Google Gemini.

## 🚀 Cómo subir a Streamlit Cloud

### 1. Sube el proyecto a GitHub
```bash
git init
git add .
git commit -m "Turismo Belalcázar con GuíaBot"
git push origin main
```

### 2. Despliega en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio de GitHub
3. Archivo principal: `app.py`

### 3. Configura el API Key de Gemini
En Streamlit Cloud:
- Ve a tu app → **Settings** → **Secrets**
- Pega exactamente esto:

```toml
GEMINI_API_KEY = "AIzaSyAXYmiCr0sZZCLrGbMbbh10wckFm0YUjFU"
```

### 4. ¡Listo! 🎉

## 📁 Estructura del proyecto
```
belalcazar_turismo/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
└── .streamlit/
    └── secrets.toml    # API keys (NO subir a GitHub público)
```

## ⚠️ Importante
- **No subas** `.streamlit/secrets.toml` a GitHub si tu repositorio es público
- Añade `.streamlit/secrets.toml` a tu `.gitignore`
- Configura el secret directamente en el panel de Streamlit Cloud

## 🤖 GuíaBot
El chat utiliza `gemini-1.5-flash` con instrucciones para responder ÚNICAMENTE sobre turismo de Belalcázar. Si el usuario pregunta sobre otro tema, el bot lo redirige amablemente al turismo local.
