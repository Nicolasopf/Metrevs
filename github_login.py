#!/usr/bin/python3
from github import Github as Github_api
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_github import GitHub as Github_login


app = Flask(__name__)  # Start flask application
app.url_map.strict_slashes = False  # No needed slash at end
# Set the client ID for OAuth2
app.config['GITHUB_CLIENT_ID'] = 'f3a06304f838d1f05b3c'
app.config['GITHUB_CLIENT_SECRET'] = '8f1cfe79f990bbd3a0340e265f66a2a222a4da8f'  # ^^
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
    # If cookie X is not present:
    return github_app.authorize()


@app.route('/panel/')
@github_app.authorized_handler
def after_login(access_token):
    ''' After login in github, user will be redirected here. '''
    if access_token is None:  # If the user doesn't have logged with github.
        return github_app.authorize()  # Try to authorize again.

    next_url = url_for('auth_key')
    resp = make_response(redirect(next_url))  # Redirect the user to auth_key.
    # set the cookie with the token to api.
    resp.set_cookie('userToken', access_token)
    return resp


@app.route('/auth_key/')
def auth_key():
    ''' Time ti play with the auth_key '''
    if not request.cookies.get("userToken"):  # If the cookie doesn't exist
        return github_app.authorize()

    # From the cookies, get the user token to do requests.
    token = request.cookies.get('userToken')
    print(token)
    # First create a Github api instance
    g = Github_api(token)

    # Then play with Github objects:
    repo_list = []
    for repo in g.get_user().get_repos():
        repo_list.append(repo.name)
    return "<br>".join(repo_list)


if __name__ == "__main__":
    app.run()
