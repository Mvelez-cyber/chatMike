import streamlit as st
import openai

# Cargar la API key desde los secretos de Streamlit
openai.api_key = st.secrets["openai"]["api_key"]

# Interfaz de usuario con Streamlit
st.title("Chatbot con GPT-3")

# Selecciona el modelo GPT
model = st.selectbox("Selecciona el modelo GPT:", ["text-davinci-003", "text-curie-001"])

# Campo para ingresar el prompt
prompt = st.text_area("Introduce el prompt:")

# Al hacer clic en el botón, se envía el prompt a la API
if st.button("Enviar"):
    if prompt:
        try:
            # Uso del método adecuado para la versión 0.28 de la API
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=100,
                temperature=0.5,
            )
            # Mostrar la respuesta en Streamlit
            st.write("Respuesta:")
            st.write(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Por favor, introduce un prompt.")
