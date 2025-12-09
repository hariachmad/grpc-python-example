import grpc

import Audio_pb2
import Audio_pb2_grpc
import wave
import opuslib


def send_audio():
    channel = grpc.insecure_channel("localhost:50051")
    stub = Audio_pb2_grpc.AudioServiceStub(channel)
    path =  "./recorded.wav"
    channels = None
    sample_rate = None
    opus_frames = []
    frame_size = 960

    with wave.open(path, "rb") as wf:
        channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        encoder = opuslib.Encoder(
        Fs=sample_rate,
        channels=channels,
        application=opuslib.APPLICATION_AUDIO)
        opus_frames = []
        while True:
            pcm = wf.readframes(frame_size)
            if not pcm:
                break

            # Encode PCM → Opus frame
            encoded = encoder.encode(pcm, frame_size)
            opus_frames.append(encoded)

    request = Audio_pb2.AudioRequest(
        opus_data=opus_frames,
        sample_rate=48000,
        channels=1
    )

    response = stub.SendAudio(request)
    print("Server respond:", response.status)


if __name__ == "__main__":
    send_audio()
