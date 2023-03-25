import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.run('pytest')


@nox.session
def format(session: nox.Session) -> None:
    session.install("brunette", "isort")
    session.run("brunette", "--config=setup.cfg", ".")
    session.run("isort", "--sp=setup.cfg", ".")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("flake8", "mypy")
    session.run("flake8", "--config=setup.cfg", ".")
    session.run("mypy", "--config-file=setup.cfg", ".")