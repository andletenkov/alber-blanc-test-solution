### Запуск тестов

```bash
docker-compose up --exit-code-from tests
```

### Найденные баги

В скобках указаны автотесты, которые их воспроизводят

* метод `select` возвращает `'status': 'failure'` при успешном выполнении (test_add_user);
* значение `reason` возвращается только в случае ошибок, связанных с неверным форматом указанных полей (
  test_delete_user);
* при вызове `select` с указанием поля `surname` возвращается только первый подходящий под условие пользователь (
  test_select_multiple_users[select by surname]);
* при вызове `update` значение `age` пользователя остается неизменным (test_update_user);
* приложение не валидирует пустые значения переданных полей (test_invalid_data[empty values]);
* приложение не валидирует отрицательное значение `age` (test_invalid_data[negative age]);
* приложение не валидирует некорректное значение `phone` (буквы, знаки пунктуации и т.п.) – формально багом не является, так как в спецификации это не описано, но по логике – да. (test_invalid_data[no digit 'phone' value]);
* приложение падает с ошибкой `*** buffer overflow detected ***: terminated` при передаче слишком длинного (~1000
  символов) сообщения (test_invalid_data[payload length overflow]).

#### Замечания

* желательно использовать подключение поверх TLS (wss) вместо небезопасного ws;
* строковые поля без валидации – потенциальная угроза для XSS и SQL-инъекций для продакшн приложения