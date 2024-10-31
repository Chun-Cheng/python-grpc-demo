# python-grpc-demo

A simple chat/messaging app demo using gRPC.

## Prerequisites

- Python>=3.12 installed
- Poetry installed
- Unix environment (it needs to use `curses` in Python)

## How to run

1. Install dependencies
    ```sh
    poetry install
    ```
2. Activate Poetry environment
    ```sh
    poetry shell
    ```
3. Add `src` to Python path
    ```sh
    export PYTHONPATH=$PYTHONPATH:/home/dev/message/python-grpc-demo/src
    ```
4. Start the server
    ```sh
    python src/server/server.py
    ```
5. Open another shell and repeat step 1~3, then start the client
    ```sh
    python src/client/client.py
    ```

## Update the protos

To generate a new version of protobuf code, setup the environment first:

```sh
poetry install --with dev
poetry shell
```

Then, run the following command:

```sh
python script/generate.py
```
