import streamlit as st
import openai

# Obtener la clave API de OpenAI desde los secretos del repositorio.
openai_api_key = st.secrets["openai_api_key"]

# Si no se proporciona una clave API, mostrar un mensaje informativo.
if not openai_api_key:
    st.info("Por favor, agrega tu clave API de OpenAI en los secretos para continuar.")
else:
    # Crear un cliente de OpenAI.
    openai.api_key = openai_api_key

    # Selección del modelo basado en la necesidad del usuario.
    model_option = st.selectbox(
        "Selecciona el modelo GPT-3:",
        ("text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001")
    )

    # Crear una variable de estado de sesión para almacenar los mensajes del chat.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes del chat existentes.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Crear un campo de entrada para que el usuario ingrese un mensaje.
    if user_input := st.chat_input("Escribe un mensaje"):
        # Guardar el mensaje del usuario.
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Llamar al modelo seleccionado en OpenAI GPT-3.
        response = openai.Completion.create(
            model=model_option,
            prompt=user_input,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # Guardar la respuesta del modelo en el estado de sesión.
        bot_response = response.choices[0].text.strip()
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Mostrar la respuesta del modelo.
        with st.chat_message("assistant"):
            st.markdown(bot_response)
