import contextlib
import time
import pytest
from hypothesis import given, strategies
from conftest import random_string
from src.check import check, softly

parametrize = pytest.mark.parametrize
param = pytest.param


def test_add_user(app, add_user):
    user = add_user()
    select_resp = app.select(phone=user['phone'])

    with softly():
        check(select_resp).is_success()
        check(select_resp['users']).is_length(1)
        check(select_resp['users'][0]).is_equal_to(user)


def test_delete_user(app, add_user):
    user = add_user()
    delete_resp = app.delete(phone=user['phone'])
    select_resp = app.select(phone=user['phone'])

    with softly():
        check(delete_resp).is_success()
        check(select_resp).is_failure()
        check(select_resp.get('reason')).is_not_none()


@parametrize('data', [
    param({'name': 'Matt'}, id='select by name'),
    param({'surname': 'Damon'}, id='select by surname')
])
def test_select_multiple_users(app, add_user, data):
    first = add_user(**data)
    second = add_user(**data)
    third = add_user(**data)

    select_resp = app.select(**data)
    with softly():
        check(select_resp).is_success()
        check(select_resp['users']).contains_only(first, second, third)


def test_update_user(app, add_user):
    user = add_user()

    new_user = {
        'name': f'New {user["name"]}',
        'surname': f'New {user["surname"]}',
        'age': user['age'] + 10,
        'phone': user['phone']
    }

    update_resp = app.update(**new_user)
    check(update_resp).is_success()
    select_resp = app.select(phone=user['phone'])
    with softly():
        check(select_resp).is_success()
        check(select_resp['users']).is_length(1)
        check(select_resp['users'][0]).is_equal_to(new_user)


def test_add_existing_user(app, add_user):
    user = add_user()
    add_resp = app.add(**user)
    check(add_resp).is_failure()
    check(add_resp.get('reason')).is_not_none()


@parametrize('data', [
    param({'method': 'delete'}, id='delete'),
    param({'method': 'update', 'name': random_string(), 'surname': random_string(), 'age': 30}, id='update'),
    param({'method': 'select'}, id='select')
])
def test_request_nonexistent_user(app, data):
    user_phone = str(time.time_ns())
    resp = app.send({'phone': user_phone, **data})
    check(resp).is_failure()
    check(resp.get('reason')).is_not_none()


@given(data=strategies.fixed_dictionaries({
    'id': strategies.text(min_size=1),
    'name': strategies.text(min_size=1),
    'surname': strategies.text(min_size=1),
    'phone': strategies.text(min_size=1),
    'age': strategies.integers(min_value=0)
})
)
def test_add_user_with_randomly_generated_data(app, data):
    @contextlib.contextmanager
    def teardown():
        yield
        app.delete(phone=data['phone'])

    with teardown():
        resp = app.add(**data)
        check(resp).is_success()


@parametrize('data', [
    param({'method': random_string()}, id='unknown method'),
    param([], id='invalid payload format'),
    param({'id': 1}, id='invalid \'id\' format'),
    param({'method': True}, id='invalid \'method\' format'),
    param({'method': 'select', 'name': []}, id='invalid \'name\' format'),
    param({'method': 'add', 'name': random_string(), 'surname': None}, id='invalid \'surname\' format'),
    param({'method': 'delete', 'name': random_string(), 'surname': random_string(), 'phone': 123, 'age': 1},
          id='invalid \'phone\' format'),
    param({'method': 'update', 'name': random_string(), 'surname': random_string(), 'phone': '1', 'age': '1'},
          id='invalid \'age\' format'),
    param({'method': 'add', 'name': '', 'surname': '', 'phone': '', 'age': 0}, id='empty values'),
    param({'method': 'add', 'name': random_string(), 'surname': random_string(), 'phone': '1', 'age': -1},
          id='negative age'),
    param({'test': 10 ** 500}, id='number overflow'),
    param({'method': random_string(10 ** 3)}, id='payload length overflow'),  # breaks application
])
def test_invalid_data(app, data):
    resp = app.send(data)
    check(resp).is_failure()
    check(resp.get('reason')).is_not_none()
