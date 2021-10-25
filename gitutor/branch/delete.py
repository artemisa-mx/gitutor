import click
from git import GitCommandError
from PyInquirer import prompt

from .utils import list_branches


def get_branches(repo):
    _, remote_branches, local_branches= list_branches(repo, get_all=True)

    current_branch = repo.active_branch.name
    local_branches.remove(current_branch)

    if current_branch != "master":
        local_branches.remove("master")

    questions = [
        {
            'type': 'checkbox',
            'message': "Select the branches you want to delete.",
            'name': 'branches',
            'choices': [{"name": b} for b in local_branches]
        }
    ]
    answers = prompt(questions)

    branches = []
    if 'branches' in answers:
        branches = answers["branches"]

    return branches, remote_branches


def get_merged_branches(repo):
    merged = repo.git.branch('--merged').split("\n")
    merged = [b.replace("*", "").strip() for b in merged]
    return merged


def can_delete(branch_name, merged_branches, remote_branches, force, is_local):
    delete = False
    error = ""
    
    if force:
        delete = True
    elif not is_local and branch_name not in remote_branches:
        error = f"Unable to delete '{branch_name}': remote ref does not exist.\nTo delete locally run 'gt branch delete --local'."
    elif branch_name not in merged_branches:
        error = f"The branch '{branch_name}' is not fully merged.\nIf you are sure you want to delete it, run 'gt branch delete --force'."
    else: 
        delete = True

    return delete, error


@click.command()
@click.pass_context
@click.option('-f', '--force', 'force', is_flag=True, help="force deletion (unmerged branches)", default=False)
@click.option('-l', '--local', 'is_local', is_flag=True, help="only delete branches locally", default=False)
@click.option('-b', '--branch', 'branch_name', help="branch to delete")
def delete(ctx, is_local: bool, force: bool, branch_name: str):
    """
    Delete branches remote or only locally
    """
    # recover repository's object from context
    repo = ctx.obj['REPO']

    if not branch_name:
        # prompt to get new branch
        delete_branches, remote_branches = get_branches(repo)
    else:
        _, remote_branches, _ = list_branches(repo, get_all=True)

    # get branches that have already been merged
    merged_branches = get_merged_branches(repo)

    remote = repo.remote(name="origin")
    deleted = []
    for branch in delete_branches:
        # check if branch can be deleted
        delete, error = can_delete(branch, merged_branches, remote_branches, force, is_local)

        if not delete:
            click.echo(click.style(error, fg="yellow"))
        else:
            # delete remote branch
            if not is_local:
                try:
                    remote.push(refspec=(f":{branch}"))
                except:
                    pass

            # delete branch locally
            delete_str = "-D" if force else "-d"
            repo.git.branch(delete_str, branch)  
            
            deleted.append(branch)

    if deleted:
        message = f"Successfully deleted {len(deleted)} branches: {', '.join(deleted)}"
        click.echo(click.style(message, fg="green"))