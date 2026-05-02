import click
from .agent import run
from .writer import render_brief


@click.command()
@click.option("--domain", required=True)
@click.option("--prospect", required=True)
def prep(domain: str, prospect: str):
    state = run(domain, prospect)
    click.echo(render_brief(state))


if __name__ == "__main__":
    prep()
