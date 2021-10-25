import git
import click

from .change import change
from .create import create
from .delete import delete

class CustomGroup(click.Group):
    def invoke(self, ctx):
        ctx.obj['args'] = tuple(ctx.args)
        super(CustomGroup, self).invoke(ctx)


@click.group(cls=CustomGroup)
@click.pass_context
def branch(ctx):
    """
    Manage your repo branches
    """
     # Check ctx was initialized
    ctx.ensure_object(dict)

    if '--help' not in ctx.obj['args'] and 'REPO' not in ctx.obj:
        try:
            repo = git.Repo(".", search_parent_directories=True)
            ctx.obj['REPO'] = repo
        except Exception:
            click.echo('Ups! You\'re not inside a git repo')
            exit()


branch.add_command(create)
branch.add_command(change)
branch.add_command(delete)


def main():
    branch(obj={})
