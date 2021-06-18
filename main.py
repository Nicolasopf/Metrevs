#!/usr/bin/python3
''' Starts flask application. Allow github oauth2 login and view /panel'''
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_github import GitHub as Github_login
from flask import Blueprint
from views import app_views
from github import Github
from os import urandom, getenv as env


if not env("GITHUB_CLIENT_ID") or not env("GITHUB_CLIENT_SECRET"):
    print("Please use environment variables in order to run the app.\
 \nSyntax: GITHUB_CLIENT_ID=client_id GITHUB_CLIENT_SECRET=secret ./main.py")
    exit()

app = Flask(__name__)  # Start flask application
app.url_map.strict_slashes = False  # No needed slash at end
app.secret_key = urandom(24)
# Set the client ID for OAuth2
app.config['GITHUB_CLIENT_ID'] = env("GITHUB_CLIENT_ID")
app.config['GITHUB_CLIENT_SECRET'] = env("GITHUB_CLIENT_SECRET")  # ^^
app.register_blueprint(app_views)  # Start blueprint
github_app = Github_login(app)  # Enable login to the oauth2


@app.route('/')
def index():
    ''' Index page to show '''
    return render_template('index.html')


@app.route('/login/')
def login():
    '''
    Login page to get the code key,
    this code key will be converted to an authorization key.
    '''
    if not request.cookies.get("userToken"):
        return github_app.authorize(scope="user, repo")
    return redirect(url_for('after_login'))


@app.route('/auth/')
@github_app.authorized_handler
def after_login(access_token):
    '''
    After login in github, user will be redirected here
    We receive the access_token thanks to the handler.
    This token will be used by the API to make requests as the user.
    '''
    if access_token is None:  # If the user doesn't have logged with github.
        return github_app.authorize(scope="user, repo")  # Redirect login.

    next_url = url_for('add_repos')
    resp = make_response(redirect(next_url))  # Redirect the user to /panel.
    # set the cookie with the token to api.
    resp.set_cookie('userToken', access_token)
    return resp


@app.route('/add_repos')
def add_repos():
    ''' add repositories to cookies. '''
    if not request.cookies.get("userToken"):  # If the cookie doesn't exist
        return github_app.authorize(scope="user, repo")

    userToken = request.cookies.get("userToken")
    user_session = Github(userToken)
    repos = user_session.get_user().get_repos()
    return render_template('add_repos.html', repos=repos)


@app.route('/panel', methods=['GET', 'POST'])
def panel():
    ''' Show repo selected, set a cookie for the repo, and show users. '''
    if not request.cookies.get("userToken"):  # If the cookie doesn't exist
        return github_app.authorize(scope="user, repo")

    userToken = request.cookies.get("userToken")
    user_session = Github(userToken)

    select = request.form.getlist('repos_list')  # Get the repo name selected.
    if not select:
        return redirect(url_for("add_repos"))
    users = []

    for repo in select:
        repository = user_session.get_repo(repo)
        collaborators = repository.get_collaborators()
        for collaborator in collaborators:
            if collaborator not in users:
                users.append(collaborator)
        # Pretty print, without the author of repo
    repo_name = "TESTING"

    response = make_response(render_template(
        'panel.html', repo_name=repo_name, users=users))
    response.set_cookie("repos", ", ".join(select))

    return response


if __name__ == "__main__":
    app.run()
