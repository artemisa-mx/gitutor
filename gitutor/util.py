from PyInquirer import prompt
import click

def prompt_for_commit_selection(list_of_commits, message):
    commit_page_index = 0
    choices = get_commit_page(commit_page_index, list_of_commits)
    question = [
        {
            'type': 'list',
            'message': message,
            'name': 'commit',
            'choices': choices
        }
    ]
    answer = prompt(question)
    if answer:
        while answer['commit'] == '...Show previous commits' or answer['commit'] == 'Show more commits...':
            if answer['commit'] == '...Show previous commits':
                commit_page_index-=1
                commits_to_show=get_commit_page(commit_page_index, list_of_commits)
            else:
                commit_page_index+=1
                commits_to_show=get_commit_page(commit_page_index, list_of_commits)
            question[0].update({'choices': commits_to_show})
            answer = prompt(question)
    return answer

def commits_full_list(repo, first_parent = True):
    
    if first_parent:
        log_params = ['--first-parent']
    else:
        log_params = []
    
    log_params.append("--pretty=format:'%h - %s: %an, %ar'")
    full_list_of_commits = repo.git.log(log_params).replace("'","").splitlines()
    return full_list_of_commits

def get_commit_page(page_index, full_list_of_commits):
    if page_index == 0:
        commits_to_show = full_list_of_commits[0:20]
    else:
        commits_to_show = full_list_of_commits[page_index*20:page_index*20+20]
        commits_to_show.insert(0,'...Show previous commits')
    if len(full_list_of_commits) > page_index*20+20:    
        commits_to_show.append('Show more commits...')
    return commits_to_show