## example fastapi project with registration and JWT authentication

## run
- `docker compose up --build` in root

### before run change .env.example to .env and change example variables to real

## formatting and linting
- run brunette: `brunette --config=setup.cfg app`
- run isort: `isort --sp=setup.cfg app`
- run flake8: `flake8 --config=setup.cfg`
- tun mypy: `mypy --config-file=setup.cfg app`

## testing
- =`pytest` in root

## nox
- for format and run tests: `nox` in root
