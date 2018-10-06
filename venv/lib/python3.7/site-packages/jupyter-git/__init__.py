from IPython.html.utils import url_path_join as ujoin
from tornado.web import RequestHandler
from tornado.log import app_log
import os, json, git, urllib, requests, logging
from git import Repo, GitCommandError
from subprocess import check_output
from urllib.parse import urlparse

class GitCommitHandler(RequestHandler):
    def initialize(self, log=None):
        self.log = log
        print("HELLO")
        self.write("HELLO1")
        app_log.error("\t\t### initialize function ###")

    def error_and_return(self, dirname, reason):
        self.write("HELLO2")

        app_log.error("\t\t### error_and_return function ###")
        # send error
        self.send_error(500, reason=reason)

        # return to directory
        os.chdir(dirname)

    def put(self):

        #self.write("HELLO")

        # targetfile = open("test.txt", 'w')
        # testline = raw_input("test test")
        #
        # targetfile.write(testline)

        #app_log.error("\t\t### TEST TEST TEST ###")

        # git parameters from environment variables
        # expand variables since Docker's will pass VAR=$VAL as $VAL without expansion
        git_dir = "{}/{}".format(os.path.expandvars(os.environ.get('GIT_PARENT_DIR')), os.path.expandvars(os.environ.get('GIT_REPO_NAME')))
        git_url = os.path.expandvars(os.environ.get('GIT_REMOTE_URL'))
        git_user = os.path.expandvars(os.environ.get('GIT_USER'))
        git_repo_upstream = os.path.expandvars(os.environ.get('GIT_REMOTE_UPSTREAM'))
        git_branch = git_remote = os.path.expandvars(os.environ.get('GIT_BRANCH_NAME'))
        git_access_token = os.path.expandvars(os.environ.get('GITHUB_ACCESS_TOKEN'))

        app_log.error("\t\t### git_dir %s ###" % git_dir)
        app_log.error("\t\t### git_url %s ###" % git_url)
        app_log.error("\t\t### git_user %s ###" % git_user)
        app_log.error("\t\t### git_repo_upstream %s ###" % git_repo_upstream)
        app_log.error("\t\t### git_branch %s ###" % git_branch)
        app_log.error("\t\t### git_access_token %s ###" % git_access_token)


        # get the parent directory for git operations
        git_dir_parent = os.path.dirname(git_dir)
        app_log.error("\t\t### git_dir_parent %s ###" % git_dir_parent)

        # obtain filename and msg for commit
        data = json.loads(self.request.body.decode('utf-8'))
        app_log.error("\t\t### urllib.parse.unquote(data['filename']) %s ###" % urllib.parse.unquote(data['filename']))
        filename = urllib.parse.unquote(data['filename'])  #.decode('utf-8')
        msg = data['msg']
        app_log.error("\t\t### WE RECEIVED THIS filepath %s ###" % filename)
        #app_log.error("\t\t### THE BALD MAN SAID SO ###")
        #import pdb; pdb.set_trace()

        # get current directory (to return later)
        cwd = os.getcwd()
        app_log.error("\t\t### current directory (cwd) %s ###" % cwd)

        # select branch within repo
        try:
            os.chdir(git_dir)
            app_log.error("\t\t### current directory after change %s ###" % os.getcwd())
            dir_repo = check_output(['git','rev-parse','--show-toplevel']).strip()
            app_log.error("\t\t### dir_repo %s ###" % dir_repo)
            dir_repo = os.getcwd()   #added by me
            #dir_repo = "/promitd06/tests" #hardcoded test
            repo = Repo(dir_repo)
            app_log.error("\t\t### repo %s ###" % repo)
        except GitCommandError as e:
            app_log.error("\t\t### Could not checkout repo: %s ###" % format(dir_repo))
            self.error_and_return(cwd, "Could not checkout repo: {}".format(dir_repo))
            return

        # create new branch
        app_log.error("\t\t### Create New Branch Stage ###")
        try:
            print(repo.git.checkout('HEAD', b=git_branch))
        except GitCommandError:
            print("Switching to {}".format(repo.heads[git_branch].checkout()))

        # commit current notebook
        # client will sent pathname containing git directory; append to git directory's parent
        # git_dir_parent + filename is giving promitd06/promitd06/tests/Untitled.ipynb, trying just filename now
        app_log.error("\t\t### Commit Notebook Stage ###")
        try:
            #print(repo.git.add("Untitled.ipynb"))
            print(os.path.basename(filename))
            print(repo.git.add(os.path.basename(filename)))
            #print("added")
            #app_log.error("\t\t### repo.git.add(git_dir_parent + filename) = %s ###" % repo.git.add(git_dir_parent + filename))
            #print(repo.git.commit( a=True, m="{}\n\nUpdated {}".format(msg, "tests/Untitled.ipynb") ))
            print(repo.index.commit("{}".format(msg)))
            #print("committed")
        except GitCommandError as e:
            app_log.error("\t\t### Could not commit changes to notebook: %s ###" % format("promitd06/tests/Untitled.ipynb"))
            self.error_and_return(cwd, "Could not commit changes to notebook: {}".format("promitd06/tests/Untitled.ipynb"))
            return

        # create or switch to remote
        app_log.error("\t\t### create or switch to remote Stage ###")
        try:
            remote = repo.create_remote(git_remote, git_url)
        except GitCommandError:
            print("Remote {} already exists...".format(git_remote))
            remote = repo.remote(git_remote)

        # push changes
        app_log.error("\t\t### Push Changes Stage ###")
        try:
            pushed = remote.push(git_branch)
            assert len(pushed)>0
            assert pushed[0].flags in [git.remote.PushInfo.UP_TO_DATE, git.remote.PushInfo.FAST_FORWARD, git.remote.PushInfo.NEW_HEAD, git.remote.PushInfo.NEW_TAG]
        except GitCommandError as e:
            self.error_and_return(cwd, "Could not push to remote {}".format(git_remote))
            return
        except AssertionError as e:
            self.error_and_return(cwd, "Could not push to remote {}: {}".format(git_remote, pushed[0].summary))
            return

        # open pull request
        app_log.error("\t\t### Open Pull Request Stage ###")
        try:
          github_url = "https://api.github.com/repos/{}/pulls".format(git_repo_upstream)
          github_pr = {
              "title":"{} Notebooks".format(git_user),
              "body":"IPython notebooks submitted by {}".format(git_user),
              "head":"{}:{}".format(git_user, git_remote),
              "base":"master"
          }
          github_headers = {"Authorization": "token {}".format(git_access_token)}
          r = requests.post(github_url, data=json.dumps(github_pr), headers=github_headers)
          if r.status_code != 201:
            print("r.status_code != 201")
            print("Error submitting Pull Request to {}".format(git_repo_upstream))
        except:
            print("Error submitting Pull Request to {}".format(git_repo_upstream))

        # return to directory
        os.chdir(cwd)

        # close connection
        self.write({'status': 200, 'statusText': 'Success!  Changes to {} captured on branch {} at {}'.format(filename, git_branch, git_url)})


def _jupyter_server_extension_paths():
    app_log.error("\t\t### _jupyter_server_extension_paths function ###")
    return [{
        "module": "jupyter-git"
    }]

def load_jupyter_server_extension(nbapp):
    nbapp.log.info('Loaded Jupyter extension: Git Commit and Push SERVER SIDE TEST')
    app_log.error("\t\t### load_jupyter_server_extension function ###")
    webapp = nbapp.web_app
    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (ujoin(base_url, r"/git/commit"), GitCommitHandler,
            {'log': nbapp.log}),
    ])
