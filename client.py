from PIL import Image
import numpy as np
import pickle
import grpc

import grpc_compiled.image_transform_pb2
import grpc_compiled.image_transform_pb2_grpc

def run():
    channel = grpc.insecure_channel('server:13000')
    stub = image_transform_pb2_grpc.EncodeServiceStub(channel)
    image = np.array(Image.open('eiffel-tower.jpg'))
    query = image_transform_pb2.sourceImage(
        image=pickle.dumps(image),
        width=320,
        height=180
    )
    response = stub.GetEncode(query)
    response.image

if __name__ == "__main__":
    run()
