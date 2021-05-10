import os
import random
import time
import pytest
from typing import Callable, Dict, Union

from src.check import check
from src.client import TesterClient
from src.utils import random_string


@pytest.fixture(scope='session')
def app() -> TesterClient:
    client = TesterClient(
        os.environ.get('APP_HOST'),
        int(os.environ.get('APP_PORT'))
    )
    yield client
    client.close()


@pytest.fixture
def add_user(app: TesterClient) -> Callable:
    users = []

    def wrapped(
            name: str = None,
            surname: str = None,
            phone: str = None,
            age: int = None
    ) -> Dict[str, Union[str, int]]:
        new_user = {
            'name': random_string() if name is None else name,
            'surname': random_string() if surname is None else surname,
            'phone': str(time.time_ns()) if phone is None else phone,
            'age': random.randint(18, 100) if age is None else age
        }
        resp = app.add(**new_user)
        check(resp).is_success()
        users.append(new_user)
        return new_user

    yield wrapped

    for user in users:
        app.delete(phone=user['phone'])
