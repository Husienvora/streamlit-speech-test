import streamlit as st
import assemblyai as aai
from translate import translate
from speech_synthesize import gen_dub
from configure import auth_key
import threading

# Set AssemblyAI API key
aai.settings.api_key = auth_key

# Initialize Streamlit session state
if "text" not in st.session_state:
    st.session_state["text"] = "Listening..."
    st.session_state["translated_text"] = ""
    st.session_state["run"] = False


def start_listening():
    st.session_state["run"] = True
    threading.Thread(target=run_transcription).start()


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
        st.session_state["text"] = transcript.text
        st.markdown(st.session_state["text"])
        st.session_state["translated_text"] = translate(
            st.session_state["text"], language="Japanese"
        )
        st.markdown(st.session_state["translated_text"])
        gen_dub(st.session_state["translated_text"])
        st.rerun()
    else:
        print(transcript.text, end="\r")


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


# Display transcription and translation
if st.session_state["text"] != "Listening...":
    st.markdown(f"**Transcription:** {st.session_state['text']}")
    st.markdown(f"**Translation:** {st.session_state['translated_text']}")
