import click
import versso

@click.group()
def cli():
    """Verso — QuickSight CI/CD pipeline CLI."""
    pass

@cli.command(name="init")
def init():
    """Initialize a new Verso project configuration."""
    versso.initialize()



