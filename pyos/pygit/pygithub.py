from github import Github, GithubObject

class GitHubClient(object):
    __API_GOOD = "good"

    def __init__(self, name, password):
        self.__username = name
        self.__password = password
        self.__github   = None
        self.__user     = None

    def __verify_login(self, obj):
        if obj.get_api_status().status == self.__API_GOOD:
            return True
        return False

    @property
    def user(self):
        if not self.__user:
            self.__user = self.github.get_user()
        return self.__user

    @property
    def github(self):
        if not self.__github:
            self.__github = Github(self.__username, self.__password)
            if not self.__verify_login(self.__github):
                return False
        return self.__github

    def create_repo(self, name, *args, **kwargs):
        return self.user.create_repo(name=name, *args, **kwargs)

    def get_gitignore_template(self, name):
        return self.github.get_gitignore_template(name)