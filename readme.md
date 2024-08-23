처음 make 후 아래 명령어 실행<br>
이후 make부터는 할 필요 없음

```shell
docker exec web_room python3 manage.py makemigrations
docker exec web_room python3 manage.py migrate
```