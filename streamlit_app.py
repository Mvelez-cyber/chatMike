import streamlit as st
from openai import OpenAI

# Accede a la clave API desde los secretos
openai_api_key = st.secrets["openai"]["api_key"]

# Configura el cliente de OpenAI
client = OpenAI(api_key=openai_api_key)

# Mostrar título y descripción en español.
st.title("💬 Chatbot")
st.write(
    "Este es un chatbot sencillo que utiliza el modelo GPT-3.5 de OpenAI para generar respuestas en tiempo real usando streaming. "
    "Para usar esta aplicación, necesitas proporcionar una clave API de OpenAI, que puedes guardar en los secretos del repositorio."
)

# Verifica si la clave API está disponible.
if not openai_api_key:
    st.info("Por favor, agrega tu clave API de OpenAI en los secretos para continuar.", icon="🗝️")
else:
    # Crear una variable de estado de sesión para almacenar los mensajes del chat.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes del chat existentes.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Crear un campo de entrada para que el usuario ingrese un mensaje.
    if prompt := st.chat_input("¿Qué tal?"):
        # Almacenar y mostrar el mensaje actual.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar una respuesta usando la API de OpenAI con streaming.
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            response_content = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response_content += chunk.choices[0].delta.content
                    # Mostrar el contenido recibido hasta ahora.
                    st.chat_message("assistant").markdown(response_content)

            # Almacenar la respuesta completa en el estado de la sesión.
            st.session_state.messages.append({"role": "assistant", "content": response_content})

        except Exception as e:
            st.error(f"Error al obtener respuesta de la API: {e}")
