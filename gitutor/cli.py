import git
import click

from goBack.commands import goBack
from init.commands import init
from save.commands import save
from ignore.commands import ignore
from compare.commands import compare
from lesson.commands import lesson
from branch.commands import branch


class CustomGroup(click.Group):
    def invoke(self, ctx):
        ctx.obj['args'] = tuple(ctx.args)
        super(CustomGroup, self).invoke(ctx)


@click.group(cls=CustomGroup)
@click.pass_context
def cli(ctx):
    """
    Git the easy way.

    If you want to access gitutor tutorials run 

        $ gt lesson

    Any issues, questions or bugs you can reach us at support@gitutor.io
    """
    # Check ctx was initialized
    ctx.ensure_object(dict)

    if ('--help' not in ctx.obj['args']) and (ctx.invoked_subcommand != 'init') and ctx.invoked_subcommand != 'lesson':
        try:
            repo = git.Repo(".", search_parent_directories=True)
            ctx.obj['REPO'] = repo
        except Exception:
            click.echo('Ups! You\'re not inside a git repo')
            exit()


cli.add_command(init)
cli.add_command(goBack)
cli.add_command(save)
cli.add_command(ignore)
cli.add_command(compare)
cli.add_command(branch)
cli.add_command(lesson)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
