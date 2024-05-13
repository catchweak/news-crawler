# news-crawler
news-crawler

## environment
> python 3.10.11
> fast-api
> poetry # ISTALL.md 참조

## start
### 1. activate virtual env
```sh
poetry shell
```

### 2. install dependencies
```sh
poetry install
```

### 3. run server
```sh
# poetry shell 이 실행 되어 있는 경우
uvicorn app.main:app --reload

# poetry shell 이 실행 되어 있지 않은 경우
poetry run uvicorn app.main:app
```

### 4. run test
```sh
pytest
```

### check api docs
http://localhost:8000/docs
http://localhost:8000/redoc