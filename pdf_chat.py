from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import sys

client = OpenAI()

def main():
    texto = leer_pdf("documento.pdf")
    chunks = crear_chunks(texto)
    vectorstore = crear_vectorstore(chunks)

    while True:
        pregunta = input("Haz una pregunta sobre el pdf: ")
        if pregunta == "salir":
            print("analisis terminado")
            break
        contexto = buscar_contexto(vectorstore,pregunta)
        respuesta = generar_respuesta(contexto, pregunta)
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
    chunk_size=500,
    chunk_overlap=50
)

    chunks = splitter.split_text(texto)
    return chunks

def crear_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore

def buscar_contexto(vectorstore, pregunta):
       
    resultados = vectorstore.similarity_search(pregunta, k=3)

    contexto = ""
    for resultado in resultados:
        contexto += resultado.page_content + "\n"
    
    return contexto

def generar_respuesta(contexto, pregunta):
    prompt = f"""
    Responde la pregunta utilizando el contexto proporcionado:
    Pregunta:{pregunta}    
    Contexto: {contexto}
    Ademas si la pregunta no tiene nada que ver con el archivo quiero que lo digas
    """
    response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
    )
    respuesta = response.output[0].content[0].text
    return respuesta






if __name__ == "__main__":
    main()