import git
import click
from git import GitCommandError
from .color_diff import color_diff
from util import commits_full_list, prompt_for_commit_selection

@click.command(short_help = "Compare current status with selected commit")
@click.pass_context
@click.option('-h', '--hash', 'commit', help='Hash of commit to compare')
def compare(ctx,commit):
    """
    Compare current status with selected commit.

    To display a list with all the commits run:

        $ gt compare 

    If you know the hash of the commit you want to compare your repo with, then run
    
        $ gt compare --hash  <commitHash>

    """
    #Recover repo from context
    repo = ctx.obj['REPO']

    if commit:
        try:
            click.echo(repo.git.diff(commit))
        except GitCommandError:
            click.echo('Hash not found')
        return


    full_list_of_commits = commits_full_list(repo)
    click.echo('\n'.join(color_diff("-Red lines are from prior version. \n+Green lines are from current version".splitlines())))
    click.echo("Learn how to read diff output here: https://gitutor.io/guide/gt-compare.html#understanding-the-output \n")
    answer = prompt_for_commit_selection(full_list_of_commits, 'Select commit to compare')
    if answer:
        answer_hash = answer['commit'][:7]
        diff_string = repo.git.diff(answer_hash)
        click.echo('\n'.join(color_diff(diff_string.splitlines())))
