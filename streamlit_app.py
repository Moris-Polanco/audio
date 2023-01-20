import streamlit as st
import openai_secret_manager
import openai
import base64
from pydub import AudioSegment
import os

# Autenticación de OpenAI (oculta la clave en una variable de entorno)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Configurar el modelo GPT-3 para usar el idioma español
model_engine = "text-davinci-002"
prompt = (f"transcribir notas de audio en español")

# Crear la interfaz de usuario
st.set_page_config(page_title="Transcripción de audio en español", page_icon=":microphone:", layout="wide")
st.title("Transcripción de audio en español")

audio_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3","wav","aac"])

if audio_file is not None:
    audio_bytes = audio_file.read()
    with open("audio.mp3", "wb") as f:
        f.write(audio_bytes)
    sound = AudioSegment.from_file("audio.mp3", format="mp3")
    sound.export("audio.wav", format="wav")
    with open("audio.wav", "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        audio=audio_base64,
        temperature=0.5,
    )
    result = response["choices"][0]["text"].strip()
    st.success("Transcripción completada")
    st.write("Transcripción:")
    st.write("```" + result + "```")
else:
    st.write("Por favor, seleccione un archivo de audio.")
