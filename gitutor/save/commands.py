import git
import click
from git import GitCommandError

@click.command(short_help = "Creates a checkpoint of your project")
@click.pass_context
@click.option('-m', '--message', 'message', help='Commit message')
@click.option('-l', '--local', is_flag=True, help='Save locally only')
@click.option('--defer-conflicts', is_flag=True, help='Defer conflict resolution')
def save(ctx, message, local, defer_conflicts):
    """
    Creates a checkpoint of your project, i.e., saves all of your current changes and new files.

    You can pass the commit message without the prompt with:

        $ gt save --message "This is a commit"

    If you don't want to push your changes to the remote repository run:

        $ gt save --local

    If you have files with conflicts but don't want to resolve them right away run: 

        $ gt save --defer-conflicts

    This will abort the attempt to sync with the remote repo. Your changes will be saved on your local machine only.
    You will have to solve the merge conflict later on.
    """
    # Recover repo from context
    repo = ctx.obj['REPO']

    if defer_conflicts:
        try:
            repo.git.merge('--abort')
        except Exception as e:
            if e.args[1] == 128:
                click.echo('No merge to abort!')
        else:
            click.echo('Merge aborted!')
        return

    conflicted_files = get_conflict_files(repo)

    if not conflicted_files:

        #git add .
        if not message:
            message = click.prompt('Commit message')
    
        repo.git.add(A=True)

        #git commit -m ""
        try:
            repo.git.commit("-m", message)
        except GitCommandError:
            click.echo("No changes in local repository since last commit")

        if not local:
            try: 
                repo.remotes.origin.exists()
            except:
                click.echo('Remote repository does not exist!')
            else: 
                try:
                    repo.git.pull()
                except GitCommandError as e:
                    if "no tracking" in e.stderr:
                        click.echo("There is no corresponding branch in the remote repository")
                        click.echo("Changes were saved only in local repository")
                    else:
                        conflicted_files_merge = conflicts_from_merge(repo)
                        if conflicted_files_merge:
                            click.echo('Merge conflicts in:')
                            for conflict_file in conflicted_files_merge: 
                                click.echo("- " + conflict_file)
                            click.echo('Please fix conflicts then use "gt save" again')    
                            print_abort_merge_instructions()
                else:
                    click.echo('Pushing to remote repository...')
                    repo.git.push()
                    click.echo('Done!')
    else:
        click.echo('Please fix the following conflicts then use "gt save" again')
        for conflicted_file in conflicted_files:
            click.echo(conflicted_file)
        print_abort_merge_instructions()

def print_abort_merge_instructions():
        click.echo('\nLearn how to resolve conflicts here: https://gitutor.io/guide/multiple-users.html#merge-conflicts')
        click.echo('\nDon\'t want conflicts right now ?')
        click.echo('Defer conflict resolution: gt save --defer-conflicts ')
        click.echo('Dont worry, your work will still be saved on your local repo:)')
        click.echo('\nSave only on local repo until you want to resolve conflict: gt save -l ')

def conflicts_from_merge(repo):
    unmerged_blobs = repo.index.unmerged_blobs()
    error_array = []
    # We're really interested in the stage each blob is associated with.
    # So we'll iterate through all of the paths and the entries in each value
    # list, but we won't do anything with most of the values.
    for path in unmerged_blobs:
        list_of_blobs = unmerged_blobs[path]
        for (stage, blob) in list_of_blobs:
            # Now we can check each stage to see whether there were any conflicts
            if stage != 0:
                if path not in error_array:
                    error_array.append(path)
    return error_array

def get_conflict_files(repo):
    matched_lines=[]
    try:
        repo.git.diff("--check")
    except GitCommandError as e:
        matched_lines = [line for line in e.stdout.split("'")[1].split('\n') if (": leftover conflict marker" in line) ]
    return matched_lines

