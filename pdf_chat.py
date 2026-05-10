from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import sys
from config import (
    MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K_RESULTS
)

client = OpenAI()

def main():
    texto = leer_pdf("documento.pdf")
    chunks = crear_chunks(texto)
    vectorstore = crear_vectorstore(chunks)
    chat_history = ""
    

    while True:
        pregunta = input("Haz una pregunta sobre el pdf: ")
        if pregunta.lower() == "salir":
            print("analisis terminado")
            break
        contexto = buscar_contexto(vectorstore,pregunta)
        respuesta, chat_history = generar_respuesta(contexto, pregunta, chat_history)
        print (respuesta)



def leer_pdf(pdf):
    try:
        archivo = PdfReader(pdf)
        texto = ""
        for page in archivo.pages:
            texto += page.extract_text()
        return texto
    except FileNotFoundError:
        sys.exit("no se encontro el archivo")



def crear_chunks(texto):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size = CHUNK_SIZE,
    chunk_overlap = CHUNK_OVERLAP 
)

    chunks = splitter.split_text(texto)
    return chunks

def crear_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore

def buscar_contexto(vectorstore, pregunta):
       
    resultados = vectorstore.similarity_search(pregunta, k = TOP_K_RESULTS)

    contexto = ""
    for resultado in resultados:
        contexto += resultado.page_content + "\n"
    
    return contexto

def generar_respuesta(contexto, pregunta, chat_history):

    prompt = f"""

    Eres un asistente especializado en responder preguntas sobre documentos PDF.

    Debes responder utilizando SOLO la información del contexto proporcionado.

    Reglas:
    - Si la respuesta no está en el contexto, di:
    "No encontré información sobre eso en el documento."
    - No inventes información.
    - Responde de forma clara y resumida.
    - Usa un tono profesional.

    Pregunta:
    {pregunta}

    Contexto:
    {contexto}
    Historial de coversacion: {chat_history}
    """
    response = client.responses.create(
    model = MODEL_NAME,
    input=prompt
    )
    respuesta = response.output[0].content[0].text

    chat_history += f"\nUsuario: {pregunta}\n"
    chat_history += f"Asistente: {respuesta}\n"
    
    return respuesta, chat_history






if __name__ == "__main__":
    main()