## poetry

https://python-poetry.org/docs/#installing-with-the-official-installer
linux

### 1. install

- linux, macOS, window(WSL)

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

- window(PowerShell)

```sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 2. 환경변수 설정

- linux

```sh

```

- window
  시스템 PATH에 아래 추가

```sh
C:\Users\ydj51\AppData\Roaming\Python\Scripts
```

### 3. version check

```sh
poetry --version
```

### 4. initialize project

```sh
poetry new demo
poetry init # 이미 생성된 디렉토리에 시작할때
```

### 5. activate virtual environment

```sh
poetry shell
```

### 6. install dependencies

```sh
poetry install
```

### 7. add dependency

```sh
poetry add fastapi
```
