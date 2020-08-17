import click
from github import Github
from github import GithubException
from git import GitCommandError
import git
import os


@click.command(short_help = "Create Git repo and GitHub remote")
@click.pass_context
@click.option('-u', '--user', 'user_name', help = "GitHub username")
@click.option('-p', '--password', 'password', hide_input=True, help = "GitHub password")
@click.option('-l', '--local', is_flag=True, help = "Init repo locally")
@click.option('-n', '--name', help = "Repository's name")
@click.option('--ssh', is_flag=True, help = "Use ssh authentication")
def init(ctx, user_name, password,local, name, ssh):
    """
    Create git repo and github remote

    If you don't want to create the repo in your GitHub account run:

        $ gt init -l

    You can use ssh authentication with 

        $ gt init --ssh

    (To enable ssh authentication follow this tutorial https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

    You can also provide your repo's information in one step instead of waiting for the prompt with: 

        $ gt init --name <repo name> --user <GitHub user> --password <GitHub password>

    """
    if is_initialized_repo():
        click.echo('This is already a git repo!')
        return

    if local:
        init_local_repo()
        return
    if not user_name:
        user_name = click.prompt('Username')
    
    if not password:
        password = click.prompt('Password', hide_input=True)

    if not name:
        name = click.prompt('Repo name')
    
    try:
        g = Github(user_name, password)
        user = g.get_user()
        click.echo('Creating github repo...')
        remote_repo = user.create_repo(name)
    except GithubException as e:
        error_code = e.args[0]
        if error_code == 401 :
            click.echo('Problem with credentials!')
        else:
            if error_code == 422 :
                click.echo('Repo name already used!')
    else:
        local_repo = init_local_repo()
        if ssh:
            local_repo.create_remote('origin', remote_repo.ssh_url)
        else:
            local_repo.create_remote('origin', remote_repo.clone_url)
        click.echo('Push to origin...')
        local_repo.git.push('-u', 'origin', 'master')
        click.echo('Ready!')

def init_local_repo():
    repo_dir = os.getcwd()
    file_name = os.path.join(repo_dir, 'README.md')

    repo = git.Repo.init(repo_dir)
    #Create empty README.md
    open(file_name, 'wb').close()
    repo.index.add([file_name])
    repo.index.commit('first commit')
    return repo

def is_initialized_repo():
    try:
        git.Repo('.', search_parent_directories=True)
    except:
        return False
    else:
        return True




