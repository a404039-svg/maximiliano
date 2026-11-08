import streamlit as st
import google.generativeai as genai

# Configuración de la interfaz
st.set_page_config(page_title="Maximiliano IA", page_icon="😎", layout="centered")

st.title("😎 Maximiliano IA")
st.caption("Tu compa digital para charlar de lo que sea, sin rodeos.")

# Configurar API Key de Gemini desde los secretos de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("¡Epa! Falta la GEMINI_API_KEY en los secretos de Streamlit.")
    st.stop()

# Instrucción de personalidad (Informal / Poco profesional)
system_instruction = """
Eres Maximiliano IA (o Maxi), una IA totalmente relajada, informal, poco profesional y hablas como un amigo cercano de la calle. 
Usa modismos, expresiones coloquiales, humor relajado y responde de forma directa, sin formalidades corporativas ni saludos robóticos.
"""

# Configurar el modelo con la personalidad informal
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar chat previo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("¿Qué onda? Suéltalo..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta informal de Maximiliano IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando qué responderte..."):
            try:
                # Generar respuesta manteniendo contexto
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Upps, algo falló por aquí: {e}")
