import streamlit as st
import google.generativeai as gen_ai
import time
import PyPDF2

# Configura Streamlit
st.set_page_config(
    page_title="Generador de Ideas y Modelos de Negocio - IngenIAr",
    page_icon=":lightbulb:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configuración de generación
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Título de la web
st.title("Generador de Ideas y Modelos de Negocio 💡")

# Selección de la funcionalidad
option = st.selectbox("Elige una opción:", ("Generar Ideas de Negocio", "Generar Modelo de Negocio", "Planificador Financiero", "Validador de Ideas"))

# Barra de progreso al cambiar de opción
with st.spinner("Cargando..."):
    time.sleep(1)

if option == "Generar Ideas de Negocio":
    st.header("Cuéntanos sobre ti")

    # Cajas de texto para ingresar información del usuario
    intereses = st.text_area("¿Cuáles son tus intereses o pasiones?")
    experiencia = st.text_area("¿Cuál es tu experiencia laboral o académica?")
    conocimientos = st.text_area("¿En qué áreas tienes conocimientos o habilidades?")
    mercado = st.text_area("¿Qué tipo de mercado te interesa?")
    problemas = st.text_area("¿Qué problemas o necesidades quieres resolver?")

    # Botón para iniciar la generación de ideas
    if st.button("Generar Ideas"):
        if not (intereses and experiencia and conocimientos and mercado and problemas):
            st.error("Por favor, completa todos los campos antes de generar ideas.")
        else:
            prompt = f"""
            Genera 5 ideas de negocio innovadoras para una persona con las siguientes características:
            - Intereses: {intereses}
            - Experiencia: {experiencia}
            - Conocimientos: {conocimientos}
            - Mercado: {mercado}
            - Problemas a resolver: {problemas}
            
            Incluye una breve descripción de cada idea y su potencial mercado.
            """

            try:
                model = gen_ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction="Eres un generador de ideas de negocio innovadoras."
                )

                chat_session = model.start_chat(history=[])

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simulación de tiempo de espera
                    progress.progress(i + 1)

                gemini_response = chat_session.send_message(prompt)

                st.markdown(f"## Ideas de negocio:\n{gemini_response.text}")
            except Exception as e:
                st.error(f"Ocurrió un error al generar las ideas: {str(e)}")

elif option == "Generar Modelo de Negocio":
    st.header("Proporcione su idea de negocio")

    idea_negocio = st.text_area("Describe tu idea de negocio")

    if st.button("Generar Modelo de Negocio"):
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

        try:
            model = gen_ai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="Eres un asistente para crear modelos de negocio Canvas."
            )

            chat_session = model.start_chat(history=[])

            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.05)  # Simulación de tiempo de espera
                progress.progress(i + 1)

            gemini_response = chat_session.send_message(prompt)

            st.markdown(f"## Modelo de Negocio Canvas Generado:\n{gemini_response.text}")
        except Exception as e:
            st.error(f"Error al generar el modelo de negocio: {str(e)}")

elif option == "Planificador Financiero":
    st.header("Planificador Financiero")

    # Entradas para ingresos y costos
    ingresos_fijos = st.number_input("Ingresos fijos proyectados:", min_value=0.0, step=100.0)
    ingresos_variables = st.number_input("Ingresos variables proyectados:", min_value=0.0, step=100.0)
    costos_fijos = st.number_input("Costos fijos proyectados:", min_value=0.0, step=100.0)
    costos_variables = st.number_input("Costos variables proyectados:", min_value=0.0, step=100.0)

    # Selección de moneda
    moneda = st.selectbox("Selecciona la moneda:", ["Dólares (USD)", "Soles (PEN)", "Euros (EUR)"])

    # Campo para describir el negocio
    descripcion_negocio = st.text_area("Describe tu negocio y su estructura:")

    # Subida de archivo PDF
    uploaded_file = st.file_uploader("Sube un archivo PDF con información adicional", type="pdf")

    if st.button("Generar Plan Financiero"):
        # Validación de entradas
        if ingresos_fijos < 0 or ingresos_variables < 0 or costos_fijos < 0 or costos_variables < 0:
            st.error("Por favor, ingresa valores válidos para ingresos y costos.")
        else:
            # Leer contenido del PDF si se sube uno
            pdf_content = ""
            if uploaded_file is not None:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text() + "\n"

            total_ingresos = ingresos_fijos + ingresos_variables
            total_costos = costos_fijos + costos_variables
            rentabilidad = total_ingresos - total_costos
            
            prompt = f"""
            Genera un plan financiero realista para un negocio con los siguientes datos:
            - Ingresos fijos proyectados: {ingresos_fijos} {moneda}
            - Ingresos variables proyectados: {ingresos_variables} {moneda}
            - Costos fijos proyectados: {costos_fijos} {moneda}
            - Costos variables proyectados: {costos_variables} {moneda}
            - Rentabilidad proyectada: {rentabilidad} {moneda}
            - Descripción del negocio: {descripcion_negocio}
            - Información adicional del PDF: {pdf_content}
            
            Proporciona un análisis de la rentabilidad y sugerencias para optimizar los costos.
            """

            try:
                model = gen_ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction="Eres un planificador financiero. "
                                      "Proporciona un análisis realista basado en los datos proporcionados."
                )

                chat_session = model.start_chat(history=[])

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simulación de tiempo de espera
                    progress.progress(i + 1)

                gemini_response = chat_session.send_message(prompt)

                st.markdown(f"## Plan Financiero Generado:\n{gemini_response.text}")
            except Exception as e:
                st.error(f"Error al generar el plan financiero: {str(e)}")

else:  # Opción: Validador de Ideas
    st.header("Validador de Ideas de Negocio")

    # Campo de entrada para la idea de negocio
    idea_negocio = st.text_area("Describe tu idea de negocio")

    # Botón para validar la idea
    if st.button("Validar Idea"):
        if not idea_negocio:
            st.error("Por favor, ingresa una descripción de tu idea de negocio.")
        else:
            prompt = f"""
            Evalúa la viabilidad de la siguiente idea de negocio:
            Idea de negocio: {idea_negocio}
            
            Proporciona comentarios sobre:
            - Oportunidades de mercado
            - Potenciales desafíos
            - Sugerencias para mejorar la idea
            """

            try:
                model = gen_ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction="Eres un validador de ideas de negocio. "
                                      "Proporciona comentarios sobre la viabilidad de la idea presentada."
                )

                chat_session = model.start_chat(history=[])

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simulación de tiempo de espera
                    progress.progress(i + 1)

                gemini_response = chat_session.send_message(prompt)

                st.markdown(f"## Comentarios sobre la Idea:\n{gemini_response.text}")
            except Exception as e:
                st.error(f"Ocurrió un error al validar la idea: {str(e)}")
