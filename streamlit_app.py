import streamlit as st
import openai

# Accede a la clave API desde los secretos
openai_api_key = st.secrets["openai"]["api_key"]

# Configura la clave API para OpenAI
openai.api_key = openai_api_key

# Mostrar título y descripción en español.
st.title("💬 Chatbot")
st.write(
    "Este es un chatbot sencillo que utiliza el modelo GPT-3.5 de OpenAI para generar respuestas. "
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

        # Generar una respuesta usando la API de OpenAI.
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

            # Obtener el contenido de la respuesta.
            response_content = response.choices[0].message['content']

            # Mostrar la respuesta al chat y almacenarla en el estado de la sesión.
            with st.chat_message("assistant"):
                st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})
        except openai.error.OpenAIError as e:
            st.error(f"Error al obtener respuesta de la API: {e}")
