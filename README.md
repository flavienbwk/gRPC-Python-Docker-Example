# gRPC Python Docker example

A simple gRPC communication example in Python built by Docker

In this example, we are going to build a simple gRPC client and server that take an image as input and return a negative and resized version of the image.

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
Pillow==7.2.0
grpcio==1.30.0
```

## 2. Defining your proto file

gRPC works with `.proto` files to know which data to handle. Let's create a [`image_transform.proto`](./image_transform.proto) file :

```proto
syntax = "proto3";

package flavienbwk;

service EncodeService {
    rpc GetEncode(sourceImage) returns (transformedImage) {}
}

// input
message sourceImage {
    bytes image = 1; // Our numpy image in bytes (by pickle)
    int32 width = 2; // Width to which we want to resize our image
    int32 height = 3; // Height to which we want to resize our image
}

// output
message transformedImage {
    bytes image = 1; // Our negative resized image in bytes (by pickle)
}
```

## 3. Compile your .proto file

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

## 4. Client

Our [client.py](./client.py) file reads the image which becomes a numpy array and sends the query to the server along with the resize information. Then we save the image under `eiffel-tower-transformed.jpg`.

```client.py
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
```
