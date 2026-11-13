# projekt

## setup

- install dependencies with
  `pip install -r requirements.txt`

- create .env with secret keys

  ```
  HASHING_KEY=""
  ENCRYPTION_KEY=""
  ```

  `HASHING_KEY` should be generated with `openssl rand -hex 32`

  `ENCRYPTION_KEY` should be generated with python code

  ```
  from cryptography.fernet import Fernet
  Fernet.generate_key()
  ```

## running

start fastapi server on localhost with port 8000
`fastapi run server.py --port 8000 --host 127.0.0.1`

## testing

install pytest
`pip install pytest`

you need to run pytest with PYTHONPATH set to current directory

### mac/linux bash

`PYTHONPATH=. pytest`

### windows cmd

`set PYTHONPATH=.&& pytest`

### windows powershell

`$env:PYTHONPATH = "."; pytest`
