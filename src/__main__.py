import uvicorn
import click
import time
import logging
import subprocess
from src.app import app


@click.group()
def cli():
    pass


@cli.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8000)
@click.option("--no-migrate", is_flag=True)
def runserver(host, port, no_migrate=False):

    if not no_migrate:
        time.sleep(10)  # wait before postgres container starts
        subprocess.check_output(["aerich", "upgrade"])
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    cli()
