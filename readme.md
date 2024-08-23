처음 make 후 아래 명령어 실행<br>
이후 make부터는 할 필요 없음

```shell
docker exec web_room python3 manage.py makemigrations
docker exec web_room python3 manage.py migrate
```


swagger로 방을 하나 만든 후(id:1)<br>
http://localhost:8000/chat/ 접속후 1(id)입력하면 방 입장.<br>
1번 방의 세부 정보 출력 됨.<br>
웹페이지 하나 더 열어서 같은 방식으로 입장 시 같은 데이터 출력.
