# gRPC Python Docker example

In this guide, we are going to build a simple gRPC client and server that take an image as input and return a negative and resized version of the image.

## 1. Dockerfile and dependencies

Nothing specific, just pip install the `grpcio` module for gRPC communication and the `numpy` + `Pillow` libraries to manipulate our image.

We are also going to use the `pickle` library (included in Python) to transform our numpy image, read by Pillow, into bytes.

```Dockerfile
FROM ubuntu:bionic

RUN apt-get update
RUN apt-get install python3 python3-pip -y

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
```

Our `requirements.txt` file :

```python-requirements
numpy==1.19.0
Pillow==8.1.1
grpcio==1.38.0
protobuf==3.17.1
```

## 2. Docker-compose file

To bind our local files to our container files and execute the program easily, let's create a [`docker-compose.yml`](./docker-compose.yml) file :

```yml
version: '3.3'

services:

    client:
        build: .
        command: python3 /usr/app/client.py
        volumes:
            - ./input:/usr/app/input    # Our input image directory
            - ./output:/usr/app/output  # Our output image directory
            - ./client.py:/usr/app/client.py:ro
            - ./grpc_compiled:/usr/app/grpc_compiled
        depends_on: 
            - server

    server:
        build: .
        command: python3 /usr/app/server.py
        volumes:
            - ./server.py:/usr/app/server.py:ro
            - ./grpc_compiled:/usr/app/grpc_compiled
```

> Note : we use `${PWD}` in volumes because Docker requires absolute paths to bind single files

## 3. Defining your proto file

gRPC works with `.proto` files to know which data to handle. Let's create a [`image_transform.proto`](./image_transform.proto) file :

```proto
syntax = "proto3";

package flavienbwk;

service EncodeService {
    rpc GetEncode(sourceImage) returns (transformedImage) {}
}

// input
message sourceImage {
    bytes image = 1; // Our numpy image in bytes (serialized by pickle)
    int32 width = 2; // Width to which we want to resize our image
    int32 height = 3; // Height to which we want to resize our image
}

// output
message transformedImage {
    bytes image = 1; // Our negative resized image in bytes (serialized by pickle)
}
```

## 4. Compile your .proto file

`.proto` files must be compiled with the `grpcio-tools` library to generate two classes that will be used to perform the communication between our client and server

First, install the `grpcio-tools` library :

```console
pip3 install grpcio-tools
```

And compile our [`image_transform.proto`](./image_transform.proto) file with :

```console
python3 -m grpc_tools.protoc -I. --python_out=./grpc_compiled --grpc_python_out=./grpc_compiled image_transform.proto
```

Files `image_transform_pb2.py` and `image_transform_pb2_grpc.py` files will appear in `grpc_compiled/`

## 5. Client

Our [client.py](./client.py) file reads the image which becomes a numpy array and sends the query to the server along with the resize information. Then we save the image returned by the server in `eiffel-tower-transformed.jpg`.

```python
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
```

## 6. Server

Our [server.py](./server.py) file receives the image, resize width and height. Then it returns a resized, negative-transformed image to the client.

```python
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
```

## 7. Run !

So let's run `docker-compose up` !

You will see our original `eiffel-tower.jpg` image will transform into its negative and resized version `eiffel-tower-transformed.jpg`

| [eiffel-tower.jpg](./inpupt/eiffel-tower.jpg) (640px / 360px) | [eiffel-tower-transformed.jpg](./output/eiffel-tower-transformed.jpg) (320px / 180px) |
| ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| ![Original image](./input/eiffel-tower.jpg)                  | ![Transformed image](./output/eiffel-tower-transformed.jpg)                           |
