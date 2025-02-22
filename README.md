# Una Health Coding Challange

API endpoints that returns glucose levels by filtering user_id, start and stop dates


## Table of Contents

- [Installation](#installation)
- [Run](#run)
- [Test](#test)
- [Documnetation](#documentation)


## Installation

1. Clone the repository.

```bash
git clone https://github.com/imgeaslikok/una-health-coding-challange.git
```

2. Navigate to the project folder.

```bash
cd una-health-coding-challange
```


## Run

1. Create an .env file in the project directory.

```bash
touch .env
```


2. Build the project.

```bash
docker-compose build
```

3. Run the project.

```bash
docker-compose up
```


## Test

1. Check container name.

```bash
docker ps
```

2. Get into the container.

```bash
docker exec -it <container_name> bash
```

2. Run tests
```bash
python manage.py test tests/api/v1
```

API Docs can be found in -> `localhost:8000/api/docs/swagger-ui`



## Documentation

- API Docs ->   localhost:8000/api/docs
- Swagger UI -> localhost:8000/api/docs/swagger-ui
