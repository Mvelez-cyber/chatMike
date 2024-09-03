import streamlit as st
import openai

# Cargar la API key desde los secretos de Streamlit
openai.api_key = st.secrets["openai"]["api_key"]

# Interfaz de usuario con Streamlit
st.title("Chatbot con GPT-3/4")

model = st.selectbox("Selecciona el modelo GPT:", ["gpt-3.5-turbo", "gpt-4"])

prompt = st.text_area("Introduce el prompt:")

if st.button("Enviar"):
    if prompt:
        try:
            # Uso del método adecuado para la versión 1.0.0 o posterior
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5,
            )
            st.write("Respuesta:")
            st.write(response.choices[0].message['content'].strip())
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Por favor, introduce un prompt.")
