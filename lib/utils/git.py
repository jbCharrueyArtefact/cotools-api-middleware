from git import Repo


def git_clone(repo_url, local_repo_target_path):
    repo = Repo.clone_from(repo_url, local_repo_target_path)
    return repo


def git_pull(repo, remote_name):
    repo.git.pull(remote_name)


def git_add(repo):
    repo.git.add(all=True)


def git_commit(repo, commit_message):
    repo.git.commit("-m", commit_message)


def git_push(repo, remote_name):
    repo.git.push(remote_name)


def get_and_update(local_repo_target_path):
    repo = Repo(local_repo_target_path)
    git_pull(repo, "origin")
    return repo
