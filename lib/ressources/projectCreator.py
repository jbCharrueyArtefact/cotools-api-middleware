import pathlib
from lib.utils.git import (
    git_clone,
    git_pull,
    git_add,
    git_commit,
    git_push,
    get_and_update,
)
from lib.ressources.models import ProjectDetails
from lib.utils.project import project_path, name
import json
import os
import shutil
import logging


class ProjectCreator:
    def __init__(self, url_git_repo, path_local_git_repo, request: ProjectDetails):
        self.path_repo = path_local_git_repo
        self.repo = self._createRepoIfNotExist(url_git_repo, path_local_git_repo)
        self.request = request

    def _createRepoIfNotExist(self, url_git_repo, path_local_git_repo):

        if not pathlib.Path(f"./{path_local_git_repo}").exists():
            return git_clone(url_git_repo, path_local_git_repo)
        else:
            return get_and_update(self.path_repo)

    def _create_json(self):
        filename = f"./{self.path_repo}/conf/{project_path(self.request)}.json"
        if not pathlib.Path(f"./{self.path_repo}/conf/prod").exists():
            os.mkdir(f"./{self.path_repo}/conf/prod")

        final_dict = {name(self.request): self.request.dict()}
        with open(filename, "x") as json_file:
            json_file.write(json.dumps(final_dict))

    def _add_commit_and_push(self, commit_message):
        git_add(self.repo)
        git_commit(self.repo, commit_message)
        git_push(self.repo, "origin")

    @classmethod
    def create_project(cls, url_git_repo, path_local_git_repo, request: ProjectDetails):

        try:
            projectCreator = cls(url_git_repo, path_local_git_repo, request)
            projectCreator._create_json()
            projectCreator._add_commit_and_push(f"crea/{name(projectCreator.request)}")
            return "project created"
        except Exception as e:
            logging.warning(f"an error occured : {str(e)}")
        finally:
            shutil.rmtree(path_local_git_repo)
