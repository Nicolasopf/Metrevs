#!/usr/bin/python3
''' Starts flask application. Allow github oauth2 login and view /panel'''


from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_github import GitHub as Github_login
from flask import Blueprint
from views import app_views
from github import Github


app = Flask(__name__)  # Start flask application
app.url_map.strict_slashes = False  # No needed slash at end
app.secret_key = "b'\xd7\x9b\x14fc|\xee\x85d9\x84Ol\x0f\x02.\x9b\x01\xb2\xdd\xf3\xe4\x88\x92'"
# Set the client ID for OAuth2
app.config['GITHUB_CLIENT_ID'] = 'f3a06304f838d1f05b3c'
app.config['GITHUB_CLIENT_SECRET'] = '8f1cfe79f990bbd3a0340e265f66a2a222a4da8f'  # ^^
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
    ''' add repositories to local storage '''
    if not request.cookies.get("userToken"):  # If the cookie doesn't exist
        return github_app.authorize(scope="user, repo")

    userToken = request.cookies.get("userToken")
    user_session = Github(userToken)
    repos = user_session.get_user().get_repos()
    return render_template('add_repos.html', repos=repos)


@app.route('/panel', methods=['GET', 'POST'])
def panel():
    ''' Show repo selected, set a cookie for the repo, and show users.
    Pending: Save users selected to show the information about them in some repo
    '''
    if not request.cookies.get("userToken"):  # If the cookie doesn't exist
        return github_app.authorize(scope="user, repo")

    userToken = request.cookies.get("userToken")
    user_session = Github(userToken)

    select = request.form.getlist('repos_list')  # Get the repo name selected.
    repo = user_session.get_repo(select[0])
    users = repo.get_collaborators()
    # Pretty print, without the author of repo
    repo_name = repo.name

    response = make_response(render_template(
        'panel.html', repo_name=repo_name, users=users))
    response.set_cookie("repos", ", ".join(select))
    # cookies = request.cookies.get("repo")
    # if cookies:
    #     if select not in cookies:
    #         cookies = cookies + ", " + select
    #     response.set_cookie("repo", cookies)
    # else:
    #     response.set_cookie("repo", select)
    print(request.cookies.get("repo"))
    print(response)
    return response


if __name__ == "__main__":
    app.run()
