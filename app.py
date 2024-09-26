import os
import streamlit as st
import google.generativeai as gen_ai

# Configura Streamlit
st.set_page_config(
    page_title="Generador de Modelos de Negocio - IngenIAr",
    page_icon=":chart_with_upwards_trend:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configura la generación
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
}

# Crea el modelo con instrucciones de sistema
model = gen_ai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un asistente para crear modelos de negocio Canvas. "
                      "Utiliza la idea proporcionada para generar un modelo de negocio y sugerencias de estrategias."
)

# Título de la web
st.title("Generador de Modelos de Negocio Canvas 💡")

# Sección de información del negocio
st.header("Proporcione su idea de negocio")

# Campo de entrada para la idea del negocio
idea_negocio = st.text_area("Describe tu idea de negocio")

# Botón para iniciar la generación del modelo de negocio
if st.button("Generar Modelo de Negocio"):
    # Crea el prompt para la API de Gemini
    prompt = f"""
    Crea un modelo de negocio Canvas basado en la siguiente idea:
    
    Idea de negocio: {idea_negocio}

    Incluye los siguientes componentes:
    - Propuesta de valor
    - Segmentos de clientes
    - Fuentes de ingresos
    - Actividades clave
    - Recursos clave
    - Canales
    
    Además, proporciona sugerencias de estrategias para mejorar cada área.
    """

    # Envía el prompt a Gemini para obtener el modelo de negocio
    try:
        response = model.generate(text=prompt)
        # Muestra el modelo de negocio al usuario
        st.markdown(f"## Modelo de Negocio Canvas Generado:\n{response.text}")
    except Exception as e:
        st.error(f"Error al generar el modelo de negocio: {str(e)}")
