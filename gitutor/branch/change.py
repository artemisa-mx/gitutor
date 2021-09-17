import click
from git import GitCommandError
from PyInquirer import prompt


def get_branches(repo, get_all=True):
    local_branches = set(branch.name for branch in repo.branches)

    if get_all:
        branches = []
        remote_refs = repo.remote().refs
        for refs in remote_refs:
            branch = refs.name
            branch = branch.replace("origin/", "")

            if branch == "HEAD":
                continue

            branches.append(branch)

        remote_branches = set(branches) - local_branches
        branches = set(branches).union(local_branches)
    else:
        branches = local_branches
        remote_branches = []
    
    return branches, remote_branches


def get_new_branch(repo, get_all):
    repo_branches, remote_branches = get_branches(repo, get_all)

    message = "Select the branch you want to use."

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
@click.option('-a', '--all', 'get_all', is_flag=True, help="create local branch", default=False)
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
        except GitCommandError as ex:
            # error = "Please commit your changes or stash them before you switch branches.\nAborting"
            error = str(ex)
            click.echo(click.style(error, fg="yellow"))
