## Простой HTTP сервер

Проверить POST запрос
```bash
curl -v -X POST --data-binary @bigfile.txt http://localhost:8080/upload
```