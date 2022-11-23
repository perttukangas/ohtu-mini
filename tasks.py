from invoke import task


@task
def dev(ctx):
    ctx.run("flask run", pty=True)


@task
def start(ctx):
    ctx.run("gunicorn --bind 0.0.0.0:8080 app:app", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest && coverage html", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)
