# python-grpc-demo

A simple chat/messaging app demo using gRPC.

![demo screenshot](docs/images/image.png)

## Prerequisites

- Python>=3.12 installed
- Poetry installed
- Unix environment (need `curses` in Python)

## How to run

1. Install dependencies
    ```sh
    poetry install --no-root
    ```
2. Activate Poetry environment
    ```sh
    eval $(poetry env activate)
    ```
3. Add `src` to Python path (Change the path to yours)
    ```sh
    export PYTHONPATH=$PYTHONPATH:path/to/python-grpc-demo/src
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
poetry install --no-root --extras dev
eval $(poetry env activate)
```

Then, run the following command:

```sh
python scripts/generate.py
```

## File structure

```
python-grpc-demo
├── protos/             # Protocol Buffers definition contents
├── scripts/            # useful commands
│   └── generate.py     # generate Python codes from protos/
├── src/                # source code
│   ├── proto_gen/      # generated codes from protos/
│   ├── client/
│   └── server/
├── pyproject.toml      # project and dependencies info and settings
└── ......
```

The app use SQLite to store data. If you want to clear the data, delete `server.db` and `client.db`.
