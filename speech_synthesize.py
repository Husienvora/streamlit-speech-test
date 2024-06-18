from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream

client = ElevenLabs(api_key="sk_7d33f527170371a2a1364c03d7e04c9306942fbcf6dd27c4")


def gen_dub(text):
    print("Generating audio...")
    audio = client.generate(
        text=text,
        voice="21m00Tcm4TlvDq8ikWAM",
        model="eleven_multilingual_v2",  # Insert voice model here!
    )
    play(audio)


# print(client.voices.get_all())
# gen_dub("こんにちは、私の名前はフセインです。")
# str = "sk_7d33f527170371a2a1364c03d7e04c9306942fbcf6dd27c4"
