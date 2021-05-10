import json
import uuid
from logging import info
from typing import Any

import websocket


class TesterClient:
    """
    Tester application client impl
    """

    def __init__(self, host: str, port: int) -> None:
        uri = f'ws://{host}:{port}'
        self._ws = websocket.create_connection(uri)

    def close(self) -> None:
        self._ws.close()

    def send(self, data: Any) -> dict:
        if isinstance(data, dict):
            data.setdefault('id', str(uuid.uuid4()))

        payload = json.dumps(data)
        info(f'Sent – {data}')

        self._ws.send(payload)
        resp = json.loads(self._ws.recv())
        info(f'Received – {resp}')

        return resp

    def add(self, **data: Any) -> dict:
        return self.send({
            'method': 'add',
            **data
        })

    def delete(self, **data: Any) -> dict:
        return self.send({
            'method': 'delete',
            **data
        })

    def update(self, **data: Any) -> dict:
        return self.send({
            'method': 'update',
            **data
        })

    def select(self, **data: Any) -> dict:
        return self.send({
            'method': 'select',
            **data
        })
