import re
import click
from git import GitCommandError


def parse_branch(branch_name: str):
    branch_name = re.sub(r"\s{2,}", " ", branch_name)
    branch_name = branch_name.replace(" ", "-")
    return branch_name


@click.command()
@click.pass_context
@click.option('-l', '--local', 'is_local', is_flag=True, help="create local branch")
@click.option('-b', '--branch', 'branch_name', help="branch name")
def create(ctx, is_local: bool, branch_name: str):
    """
    Create new branch in the repo
    """
    # recover repository's object from context
    repo = ctx.obj['REPO']

    if not branch_name:
        branch_name = click.prompt("Branch name")

    branch_name = parse_branch(branch_name)

    # create new branch
    try:
        repo.git.checkout(b=branch_name)
    except GitCommandError:
        error = f"fatal: A branch named '{branch_name}' already exists."
        click.echo(click.style(error, fg="red"))
    else:
        # create branch in remote repo
        if not is_local:
            repo.git.execute(["git", "push", "--set-upstream", "origin", branch_name])
            click.echo(f"Local branch {branch_name} created successfully!")
        else:
            click.echo(f"Branch {branch_name} created successfully!")
