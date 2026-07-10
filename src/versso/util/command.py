import click
import versso

@click.group()
def cli():
    """Verso — QuickSight CI/CD pipeline CLI."""
    pass

@cli.command(name="init")
def init():
    """Initialize a new Verso local configuration."""
    versso.initialize()

@cli.command(name="clone")
def clone():
    """Initialize a new Verso local configuration."""
    versso.initialize()

@cli.command(name="commit")
def commit():
    """Initialize a new Verso local configuration."""
    versso.initialize()

@cli.command(name="push")
def push():
    """Initialize a new Verso local configuration."""
    versso.initialize()

@cli.command(name="promote")
def promote():
    """Initialize a new Verso local configuration."""
    versso.initialize()