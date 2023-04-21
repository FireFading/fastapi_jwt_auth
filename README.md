# FastAPI JWT-auth project

## Features:
- JWT-authentication
- actions with User model
- registration/login
- testing

## installation
- change .env.example to .env and change example variables to real

## run
```bash
  docker compose up --build
 ``` 

## formatting and linting
- run brunette: `brunette --config=setup.cfg app`
- run isort: `isort --sp=setup.cfg app`
- run flake8: `flake8 --config=setup.cfg`
- tun mypy: `mypy --config-file=setup.cfg app`

## testing
- `pytest` in root

## nox
- for format and run tests: `nox` in root
