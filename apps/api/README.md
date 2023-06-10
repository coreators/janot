### FastAPI Setup
* fastapi
* poetry
* uvicorn

[ref](https://medium.com/@caetanoog/start-your-first-fastapi-server-with-poetry-in-10-minutes-fef90e9604d9)

## How to run
### Setup environment
First, run virtual environment. 
```
poetry shell
```

Second, install requirement packages. 
```
poetry install
``` 

### Load Documents into memory
First, locate your .pdf, .csv, .txt, .obs files in SOURCE_DOCUMENTS
(Write obisidian root path into .obs file to load obsidian)

Second, run ingest script. 
```
python ingest.py
```

### Start FASTAPI server

```
make start
```


### API Document

[Swagger](http://127.0.0.1:9000/docs)
[Redoc](http://127.0.0.1:9000/redoc)


### Additional Commands
To install package

```
poetry add <package-name>
```


### Env variable

mac
```
brew install direnv

```

ubuntu
```
$ apt install direnv
$ vim ~/.bashrc

add eval "$(direnv hook bash)"

```


### Poetry venv VScode setting

apps/api/.venv/bin/python

[ref](https://amazingguni.medium.com/python-poetry%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EB%A5%BC-vscode%EC%97%90%EC%84%9C-%EA%B0%9C%EB%B0%9C%ED%95%A0-%EB%95%8C-interpreter%EB%A5%BC-%EC%9E%A1%EB%8A%94-%EB%B0%A9%EB%B2%95-e1806f093e6d)
