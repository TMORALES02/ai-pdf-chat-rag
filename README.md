# AI PDF Chat

AI PDF Chat es una aplicación web construida con Python, Streamlit y OpenAI que permite subir documentos PDF y hacer preguntas sobre su contenido utilizando inteligencia artificial.

La aplicación utiliza embeddings, búsqueda semántica y Retrieval-Augmented Generation (RAG) para responder preguntas de forma contextual.

---

# Features

- Subida de archivos PDF
- Extracción automática de texto
- División inteligente en chunks
- Embeddings con OpenAI
- Base vectorial FAISS
- Búsqueda semántica
- Chat interactivo estilo ChatGPT
- Memoria conversacional
- Respuestas contextuales usando IA

---

# Tecnologías utilizadas

- Python
- Streamlit
- OpenAI API
- LangChain
- FAISS
- PyPDF

---

# Screenshots

## Interfaz principal

![Interfaz principal](screenshots/app.png)

---

## Chat funcionando

![Chat funcionando](screenshots/chat.png)

---

# Cómo ejecutar el proyecto

## 1. Clonar repositorio

```bash
git clone https://github.com/TMORALES02/ai-pdf-chat-rag.git
```

---

## 2. Entrar al proyecto

```bash
cd ai-pdf-chat-rag
```

---

## 3. Crear entorno virtual

```bash
python -m venv .venv
```

---

## 4. Activar entorno virtual

### Windows

```bash
.venv\Scripts\activate
```

---

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 6. Configurar API Key

Configurar variable de entorno:

```bash
OPENAI_API_KEY=tu_api_key
```

---

## 7. Ejecutar aplicación

```bash
streamlit run app.py
```

---

# Autor

Tomás Morales

GitHub:
https://github.com/TMORALES02