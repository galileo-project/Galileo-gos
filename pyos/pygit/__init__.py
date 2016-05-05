import os
from gitdb import GitDB
from git import Repo, Git
from github import GithubObject
from pyos.pygit.pygithub import GitHubClient
from pyos.pyos.operation import SysOperation

class GitClient(SysOperation):
    _GITIGNORE_NAME = ".gitignore"

    def __init__(self, email=None, uname=None, pwd=None):
        self.__repo        = None
        self.__origin      = None
        self.__github      = None
        self.__email       = email
        self.__uname       = uname
        self.__password    = pwd
        self.__repo_name   = None
        self.__github_url  = None
        self.__path        = None
        self.__language    = None

    @property
    def github_url(self):
        if not self.__github_url:
            self.__github_url = "git@github.com:%s/%s.git" % (self.__uname, self.__repo_name)
        return self.__github_url

    @property
    def github(self):
        if not self.__github:
            self.__github = GitHubClient(self.__uname, self.__password)
        return self.__github

    @property
    def repo(self):
        if not self.__repo:
            self.__repo = Repo(self.rel2abs(), odbt=GitDB)
        return self.__repo

    @property
    def origin(self):
        if not self.__origin:
            self.__origin = self.repo.remotes[0]
        return self.__origin

    @property
    def branch(self):
        return self.repo.active_branch.name

    def init(self, name, path=None):
        self.__repo_name = name
        self.__path      = path or self.__path or self.rel2abs()

        repo_path = os.path.join(self.__path, self.__repo_name)
        repo = Repo.init(repo_path, odbt=GitDB)
        self.__repo = repo
        return repo.bare

    def add(self, paths):
        _paths = []
        if not isinstance(paths, list):
            paths = [paths]
        _paths.append(self.rel2abs(paths))

        return self.repo.index.add(_paths)

    def commit(self, msg):
        return self.repo.index.commit(msg)

    def clone(self, url = None, to_path = None, branch = None):
        g = Git(to_path)
        g.clone(url or self.github_url)
        if branch:
            g.checkout(branch)
        return True

    def pull(self):
        self.run("git pull origin %s" % self.branch)

    def push(self):
        return self.run("git push origin %s" % self.branch)

    def _add_remote(self, name, url):
        return self.repo.create_remote(name=name, url=url)

    def git_config(self):
        return self.run("git config --global push.default matching")

    def publish(self, name = "origin"):
        try:
            self._add_remote(name, self.github_url)
        except:
            pass
        self._create_remote(self.__repo_name, description=GithubObject.NotSet)
        return self.push()

    def tag(self, path):
        return self.repo.tag(path)

    def _create_remote(self, name, *args, **kwargs):
        self.github.create_repo(name, *args, **kwargs)

    def create_gitignore(self, language):
        self.__language = language
        if self.__language:
            content = self.github.get_gitignore_template(self.__language)
            self.touch(self._GITIGNORE_NAME, content)
