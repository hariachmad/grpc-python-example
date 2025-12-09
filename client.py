import grpc

import Audio_pb2
import Audio_pb2_grpc
import wave
import ffmpeg


def send_audio():
    channel = grpc.insecure_channel("localhost:50051")
    stub = Audio_pb2_grpc.AudioServiceStub(channel)
    path =  "./recorded.wav"
    input_file = "recorded.wav"
    output_file = "output.opus"
    opus_frames = None

    (
    ffmpeg
    .input(input_file)
    .output(output_file, acodec='libopus')
    .run()
    )

    with open(output_file, "rb") as f:
        opus_frames = f.read()

    request = Audio_pb2.AudioRequest(
        opus_data=opus_frames,
        sample_rate=48000,
        channels=1
    )

    response = stub.SendAudio(request)
    print("Server respond:", response.status)


if __name__ == "__main__":
    send_audio()
