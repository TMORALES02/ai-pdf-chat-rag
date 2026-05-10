import streamlit as st
from pdf_chat import (
    leer_pdf,
    crear_chunks,
    crear_vectorstore,
    buscar_contexto,
    generar_respuesta
)

st.title("AI PDF Chat")


# Inicializar memoria
if "messages" not in st.session_state:
    st.session_state.messages = []


# Construir historial conversacional
def construir_historial(messages):
    historial = ""

    for message in messages:
        historial += f"{message['role']}: {message['content']}\n"

    return historial


# Subir PDF
pdf = st.file_uploader("Sube un archivo PDF", type="pdf")


if pdf:

    # Procesar PDF
    texto = leer_pdf(pdf)

    chunks = crear_chunks(texto)

    vectorstore = crear_vectorstore(chunks)

    st.success("PDF cargado correctamente")

    # Mostrar historial del chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input del usuario
    pregunta = st.chat_input("Haz una pregunta sobre el PDF")

    if pregunta:

        # Mostrar mensaje usuario
        with st.chat_message("user"):
            st.write(pregunta)

        # Guardar mensaje usuario
        st.session_state.messages.append(
            {"role": "user", "content": pregunta}
        )

        # Buscar contexto relevante
        contexto = buscar_contexto(vectorstore, pregunta)

        # Construir historial
        chat_history = construir_historial(
            st.session_state.messages
        )

        # Generar respuesta IA
        respuesta, _ = generar_respuesta(
            contexto,
            pregunta,
            chat_history
        )

        # Mostrar respuesta
        with st.chat_message("assistant"):
            st.write(respuesta)

        # Guardar respuesta
        st.session_state.messages.append(
            {"role": "assistant", "content": respuesta}
        )