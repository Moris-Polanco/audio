import speech_recognition as sr
import streamlit as st

st.set_page_config(page_title="Transcripción de audio en español", page_icon=":microphone:", layout="wide")
st.title("Transcripción de audio en español")

audio_file = st.file_uploader("Selecciona un archivo de audio", type=["mp3","wav","aac"])

if audio_file is not None:
    audio_bytes = audio_file.read()
    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)
    r = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='es-ES')
        st.success("Transcripción completada")
        st.write("Transcripción:")
        st.write("```" + text + "```")
    except sr.UnknownValueError:
        st.error("Lo siento, no he podido entender el audio")
    except sr.RequestError as e:
        st.error("Error en el servicio; {0}".format(e))
else:
    st.write("Por favor, seleccione un archivo de audio.")
