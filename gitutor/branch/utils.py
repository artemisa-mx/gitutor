def list_branches(repo, get_all=True):
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

    branches = sorted(list(branches))
    
    return branches, remote_branches, local_branches
