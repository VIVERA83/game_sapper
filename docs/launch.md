# <span style="color:purple">Запуск</span>

___

#### [Назад](../README.md) - Вернуться на главную

___

Необходимо выполнить следующие действия:

1. Установить [Docker](https://www.docker.com/), если его у Вас нет 
2. Монтируем образ
    ```commandline
    docker build -f dockerfile_game_xo -t game_xo .
    ```
3. Запускаем образ
   ```commandline
   docker run --rm --name test_game_xo -p 8004:8004 -e POSTGRES__DB="test_db" -e POSTGRES__USER="test_user" -e POSTGRES__PASSWORD="test_pass" game_xo
   ```

