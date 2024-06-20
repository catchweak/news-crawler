# news-crawler

news-crawler

## environment

> python 3.10.11
> fast-api
> poetry # ISTALL.md 참조
> selenium

## start

### 1. activate virtual env
```sh
poetry shell
```

### 2. install dependencies
```sh
poetry install
```

### 3. settings.json 파일 생성
본인의 환경에 맞게 `settings.json` 파일 생성
```sh
cp settings-sample.json settings.json
```

### 4. run server
```sh
# poetry shell 이 실행 되어 있는 경우
uvicorn app.main:app --reload

# poetry shell 이 실행 되어 있으면서 port 변경하는 경우
uvicorn app.main:app --port 8888 --reload

# poetry shell 이 실행 되어 있지 않은 경우
poetry run uvicorn app.main:app
```

### run test
```sh
pytest
```

### db migration

```sh
alembic revision -m "commit 메시지 작성"
```

### check api docs
http://localhost:8000/docs <br/>
http://localhost:8000/redoc