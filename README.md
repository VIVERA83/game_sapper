# API к игре крестики нолики

Запуск через docker:

1. Монтируем образ

```commandline
docker build -f dockerfile_game_xo -t game_xo .
```

2. Запускаем образ

```commandline
docker run --rm --name test_game_xo -p 8004:8004 -e POSTGRES__DB="test_db" -e POSTGRES__USER="test_user" -e POSTGRES__PASSWORD="test_pass" game_xo
```