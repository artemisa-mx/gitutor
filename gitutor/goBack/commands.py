import os
import click
from util import prompt_for_commit_selection, commits_full_list
from git import GitCommandError
from collections import deque 
  

@click.command(short_help='Returns repo version to a specific commit')
@click.pass_context
@click.option('-h', '--hash', 'commit_hash', help="hash of the commit to go back")
def goBack(ctx, commit_hash):
    """
    Returns version to a specific commit via hash or selected commit

    To display a list with all the commits run:

        $ gt goback 

    If you know the hash of the commit you want to go back to, then run

        $ gt goback --hash  <commitHash>
    """
    repo = ctx.obj['REPO']

    full_list_of_commits = commits_full_list(repo)
    if commit_hash:
        commit_hash = commit_hash[0:7]
        commit_info = find_commit_info(full_list_of_commits, commit_hash)
    else:
        selected_log_entry = prompt_for_commit_selection(full_list_of_commits, 'Select the commit you want to return')
        if 'commit' not in selected_log_entry: #handle PyInquirer bug that returns None on user click on list
            return
        selected_log_entry = selected_log_entry['commit']
        commit_info = extract_info_from_log_entry(selected_log_entry)

    if not commit_info:
        click.echo('There is no commit with the hash provided')
        return

    click.echo(f'Going back to "{commit_info["comment"]}"...')
    click.echo('Saving changes before revert...')
    commit_before_revert(repo)
    number_of_reverts = revert_to_target(repo, commit_info['hash'], full_list_of_commits)
    if number_of_reverts > 0:
        combine_reverts_into_single_commit(repo, number_of_reverts, commit_info['comment'])
        click.echo('Done!')
    else:
        click.echo('Nothing to revert!')


def combine_reverts_into_single_commit(repo, number_of_reverts, commit_comment):
    index_of_first_revert = number_of_reverts 
    repo.git.reset('--soft', f'HEAD~{index_of_first_revert}')
    repo.git.commit('-m', f'Going back to "{commit_comment}"')

def hash_sequence_to_target(target_hash, list_of_commits):
    list_of_commit_dicts = [ extract_info_from_log_entry(log_entry) for log_entry in list_of_commits ]
    list_of_hashes = [ commit_info['hash'] for commit_info in list_of_commit_dicts ]
    return list_of_hashes[:list_of_hashes.index(target_hash)]

def revert_to_target(repo, target_hash, list_of_commits):
    hash_sequence = hash_sequence_to_target(target_hash, list_of_commits)
    head_sha = hash_sequence[0] if len(hash_sequence) > 0 else None
    #We need to recalculate list_of_commits in case there was a new commit created by commit_before_revert
    list_of_commits = commits_full_list(repo)
    hash_sequence = hash_sequence_to_target(target_hash, list_of_commits)
    if len(hash_sequence) > 0:
        try:
            revert_hash_sequence(repo, hash_sequence)
        except Exception as e:
            print(e)
            repo.git.reset('--hard', head_sha)
            return 0
    
    return len(hash_sequence)

def revert_hash_sequence(repo, hash_sequence):

    for commit_hash in hash_sequence:
        try:
            if is_merge_commit(repo, commit_hash):
                repo.git.revert('-m', '1', commit_hash, '--no-edit')
            else:
                repo.git.revert(commit_hash, '--no-edit')
        except Exception as e:
            raise e

def is_merge_commit(repo, commit_hash):
    return len(repo.commit(commit_hash).parents) > 1

def find_commit_info(list_of_commits, commit_hash):
    list_of_commits = [ extract_info_from_log_entry(log_entry) for log_entry in list_of_commits]
    for commit_info in list_of_commits:
        if commit_info['hash'] == commit_hash:
            return commit_info
        
    return None

def extract_info_from_log_entry(log_entry):
    log_entry_parts = log_entry.split('-')
    return {
        'hash': log_entry_parts[0].strip(),
        'comment': log_entry_parts[1].split(':')[0]
    }

def commit_before_revert(repo):
    repo.git.add(A=True)
    try:
        repo.git.commit("-m", 'Saving before revert')
        return 1
    except GitCommandError:
        return 0