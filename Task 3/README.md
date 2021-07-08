## Условие

Создать Docker-контейнер, запускающий GUI-приложение (Firefox)

## Как запустить

```
$ sudo docker build -t docker-firefox .
```

```
$ sudo docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" docker-firefox
```

## Пояснение параметров запуска

1. Sharing the Host’s XServer with the Container by creating a volume: `--volume="$HOME/.Xauthority:/root/.Xauthority:rw"`
2. Sharing the Host’s DISPLAY environment variable to the Container: `--env="DISPLAY"`
3. Running container with host network driver with `--net=host`
