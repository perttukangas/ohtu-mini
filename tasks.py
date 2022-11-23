from invoke import task


@task
def start(ctx):
    ctx.run("flask run", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest && coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)
