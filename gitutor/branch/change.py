import click
from git import GitCommandError
from PyInquirer import prompt

from .utils import list_branches


def get_new_branch(repo, get_all):
    repo_branches, _, _ = list_branches(repo, get_all)

    message = f"Select the branch you want to use. Current branch is {repo.active_branch.name}"

    questions = [
        {
            'type': 'list',
            'message': message,
            'name': 'selected_branch',
            'default': 1,
            'choices': repo_branches
        }
    ]
    answers = prompt(questions)

    if "selected_branch" in answers:
        selected_branch = answers["selected_branch"]
    else:
        selected_branch = None

    return selected_branch


@click.command()
@click.pass_context
@click.option('-a', '--all', 'get_all', is_flag=True, help="show remote and local branches", default=False)
@click.option('-b', '--branch', 'branch_name', help="branch name")
def change(ctx, get_all: bool, branch_name: str):
    """
    Change current branch
    """
    # recover repository's object from context
    repo = ctx.obj['REPO']

    if not branch_name:
        # prompt to get new branch
        branch_name = get_new_branch(repo, get_all)

    if branch_name:
        try:
            repo.git.checkout(branch_name)
        except GitCommandError:
            error = "Please commit your changes or stash them before you switch branches.\nAborting"
            click.echo(click.style(error, fg="yellow"))
