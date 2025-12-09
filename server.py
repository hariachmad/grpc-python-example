import grpc
from concurrent import futures

import Audio_pb2
import Audio_pb2_grpc


class AudioService(Audio_pb2_grpc.AudioServiceServicer):
    def SendAudio(self, request, context):
        # Ambil data dari RPC
        opus_data = request.opus_data
        sample_rate = request.sample_rate
        channels = request.channels

        print("Received Opus:", len(opus_data), "bytes")
        print("Sample Rate:", sample_rate)
        print("Channels:", channels)

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