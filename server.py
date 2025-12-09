import grpc
from concurrent import futures

import Audio_pb2
import Audio_pb2_grpc
import subprocess


class AudioService(Audio_pb2_grpc.AudioServiceServicer):
    def SendAudio(self, request, context):
        opus_data = request.opus_data
        sample_rate = request.sample_rate
        channels = request.channels

        print("Received Opus:", len(opus_data), "bytes")
        print("Sample Rate:", sample_rate)
        print("Channels:", channels)
        
        with open("temp.opus", "wb") as f:
            f.write(opus_data)
        
        subprocess.run([
            "ffmpeg", "-y", "-i", "temp.opus",
            "-ar", str(sample_rate), "-ac", str(channels),
            "output_server.wav"
        ], check=True)

        print("File WAV berhasil dibuat: output.wav")

        return Audio_pb2.AudioResponse(status="received")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Audio_pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port("[::]:50051")
    print("Server running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()