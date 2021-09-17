import click

from .change import change
from .create import create


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
    pass


branch.add_command(create)
branch.add_command(change)
