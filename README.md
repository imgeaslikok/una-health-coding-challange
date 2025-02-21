# Una Health Coding Challange

### Running locally

```bash
docker-compose up --build
```

### Running tests

```bash
docker exec -it core-web-1 bash
python manage.py test tests/api/v1
```

API Docs can be found in -> `localhost:8000/api/docs/swagger-ui`


