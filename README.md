## example fastapi project with registration and JWT authentication

## run
- `docker compose up --build` in root

### before run change .env.example to .env and add change example variables to real

## formatting and linting
- run brunette: `brunette --config=setup.cfg app`
- run isort: `isort --sp=setup.cfg app`
- run flake8: `flake8 --config=setup.cfg`
- run ruff: `ruff --show-source --fix app`

## testing
- =`pytest` in root

## nox
- for format and run tests: `nox` in root
