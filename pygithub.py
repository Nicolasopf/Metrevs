#!/usr/bin/python3
from github import Github as Github_api
from flask import Flask, render_template, request, url_for, redirect
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
    next_url = url_for('auth_key')
    if access_token is None:
        return github_app.authorize()
    return redirect(next_url)


@app.route('/auth_key/')
def auth_key():
    ''' Time ti play with the auth_key '''
    # First create a Github instance
    # using an access token
    print(token)
    g = Github_api(token)

    # Then play with Github objects:
    for repo in g.get_user().get_repos():
        print(repo.name)


if __name__ == "__main__":
    app.run()
