import grpc

import Audio_pb2
import Audio_pb2_grpc
import ffmpeg
import subprocess


def send_audio():
    channel = grpc.insecure_channel("localhost:50051")
    stub = Audio_pb2_grpc.AudioServiceStub(channel)
    input_file = "input_recorded.wav"
    output_file = "output_recorded.opus"
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
    print("Writing response file")
    with open("temp_output_reply.opus", "wb") as f:
        f.write(response.opus_data)
    
    subprocess.run([
            "ffmpeg", "-y", "-i", "temp_output_reply.opus",
            "-ar", str(response.sample_rate), "-ac", str(response.channels),
            "output_reply.wav"
        ], check=True)



if __name__ == "__main__":
    send_audio()
