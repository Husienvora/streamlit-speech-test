import streamlit as st
import assemblyai as aai
from translate import translate
from speech_synthesize import gen_dub
from configure import auth_key
import threading
from queue import Queue
import os
from dotenv import load_dotenv

load_dotenv()

# Set AssemblyAI API key
aai.settings.api_key = os.environ["ASSEMBLY_KEY"]

# Initialize Streamlit session state
if "text" not in st.session_state:
    st.session_state["text"] = "Listening..."
    st.session_state["translated_text"] = ""
    st.session_state["run"] = False

# Create a queue for communication between threads
queue = Queue()


def start_listening():
    st.session_state["run"] = True
    run_transcription()


def stop_listening():
    st.session_state["run"] = False
    if "transcriber" in st.session_state:
        st.session_state.transcriber.close()


st.title("Get real-time transcription")

start, stop = st.columns(2)
start.button("Start listening", on_click=start_listening)
stop.button("Stop listening", on_click=stop_listening)


# Define callbacks
def on_open(session_opened: aai.RealtimeSessionOpened):

    print("Session ID:", session_opened.session_id)


def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        translated_text = translate(transcript.text, language="Japanese")
        gen_dub(translated_text)
        queue.put((transcript.text, translated_text))  # Add both texts to the queue

        st.rerun()  # Trigger a re-render of the Streamlit app


def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)


def on_close():
    print("Closing Session")


def run_transcription():
    # Create the Real-Time transcriber
    transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=44_100,
        on_open=on_open,
        on_close=on_close,
    )

    # Store the transcriber in the session state
    st.session_state.transcriber = transcriber

    # Start the connection
    transcriber.connect()

    # Open a microphone stream
    microphone_stream = aai.extras.MicrophoneStream()

    # Start streaming
    transcriber.stream(microphone_stream)
    # while True:
    #     print("True")


# Display transcription and translation (Updated with values from queue)
# st.markdown(
#     f"**Transcription:** {st.session_state['text']}"
# )  # Optional: Use session state or directly from queue
# st.markdown(
#     f"**Translation:** {st.session_state['translated_text']}"
# )  # Optional: Use session state or directly from queue
