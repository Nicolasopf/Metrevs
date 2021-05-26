#!/usr/bin/python3
''' Starts flask application. Allow github oauth2 login and view /panel'''


from github import Github as Github_api
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_github import GitHub as Github_login
from flask import Blueprint
from views import app_views


app = Flask(__name__)  # Start flask application
app.url_map.strict_slashes = False  # No needed slash at end
# Set the client ID for OAuth2
app.config['GITHUB_CLIENT_ID'] = 'f3a06304f838d1f05b3c'
app.config['GITHUB_CLIENT_SECRET'] = '8f1cfe79f990bbd3a0340e265f66a2a222a4da8f'  # ^^
app.register_blueprint(app_views) # Start blueprint
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
    return redirect(url_for('auth_key'))


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

    next_url = url_for('panel')
    resp = make_response(redirect(next_url))  # Redirect the user to /panel.
    # set the cookie with the token to api.
    resp.set_cookie('userToken', access_token)
    return resp


@app.route('/panel/')
def panel():
    ''' Show main panel for the user. '''
    if not request.cookies.get("userToken"):  # If the cookie doesn't exist
        return github_app.authorize(scope="user, repo")

    # Display the template html for the user to select where to go.
    return render_template('panel.html')


if __name__ == "__main__":
    app.run()
