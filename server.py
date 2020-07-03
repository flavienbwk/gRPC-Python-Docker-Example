from concurrent import futures
import numpy as np
import pickle
import grpc
import time
import sys

sys.path.append("/usr/app/grpc_compiled")
import image_transform_pb2
import image_transform_pb2_grpc

def image_to_negative(image: np.ndarray) -> np.ndarray:
    """Transforms a classic image into its negative"""
    negative = image.copy()
    for i in range(0, image.size[0]-1):
        for j in range(0, image.size[1]-1):
            pixelColorVals = image.getpixel((i,j))
            redPixel    = 255 - pixelColorVals[0] # Negate red pixel
            greenPixel  = 255 - pixelColorVals[1] # Negate green pixel
            bluePixel   = 255 - pixelColorVals[2] # Negate blue pixel
            negative.putpixel((i,j),(redPixel, greenPixel, bluePixel))
    return negative

class EService(image_transform_pb2_grpc.EncodeServiceServicer):

    def GetEncode(self, request, context):
        print("Received job !")
        image = pickle.loads(request.image)
        image = image.resize((request.width, request.height))
        image_transformed = image_to_negative(image)
        return image_transform_pb2.transformedImage(image=pickle.dumps(image_transformed))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    image_transform_pb2_grpc.add_EncodeServiceServicer_to_server(EService(),server)
    server.add_insecure_port('[::]:13000')
    server.start()
    print("Server started. Awaiting jobs...")
    try:
        while True: # since server.start() will not block, a sleep-loop is added to keep alive
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
