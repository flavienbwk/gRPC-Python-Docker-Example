from PIL import Image
import numpy as np
import pickle
import grpc
import sys

sys.path.append("/usr/app/grpc_compiled")
import image_transform_pb2
import image_transform_pb2_grpc

def run():
    channel = grpc.insecure_channel('server:13000')
    stub = image_transform_pb2_grpc.EncodeServiceStub(channel)
    image_np = np.array(Image.open('/usr/app/input/eiffel-tower.jpg'))
    image = Image.fromarray(image_np.astype('uint8')) # Transforming np array image into Pillow's Image class
    query = image_transform_pb2.sourceImage(
        image=pickle.dumps(image),
        width=320,
        height=180
    )
    response = stub.GetEncode(query)
    image_transformed = pickle.loads(response.image)
    image_transformed.save('/usr/app/output/eiffel-tower-transformed.jpg')

if __name__ == "__main__":
    run()
