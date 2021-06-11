#!/usr/bin/python3
''' View for the /reposrts to export a report of the data requeted. '''
import flask
import gspread
from views import app_views
import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask import request, redirect, session, render_template
from views.repos import prs_requests, get_hours, average_float, division

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this aplication
CLIENT_SECRETS_FILE = "client_secret.json"


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/spreadsheets']

API_SERVICE_NAME = 'drive'

API_VERSION = 'v2'


@app_views.route('/reports')
def show_reports():
    ''' Show reports... '''
    return render_template('reports.html')


@app_views.route('/generate')
def generate_reports():
    ''' Generate reports in a google sheet '''

    if 'credentials' not in session:
        return redirect('authorize')

    if not request.cookies.get("repo") or not request.cookies.get("userToken"):
        return redirect(flask.url_for('app_views.panel'))

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    client = gspread.authorize(credentials)

    token = request.cookies.get("userToken")
    repo = request.cookies.get("repo")

    prs, open_prs, closed, merged, comments, merged_no_review, reviews,\
        no_merged_total, closed_no_merged, comment_avg, avg_time_first_comment,\
        avg_time_first_review, avg_time_merge_create, avg_time_first_commit,\
        avg_time_first_comment, avg_time_merge_comment, avg_time_merge_review\
        = prs_requests(token, repo)

    data_name = ['Total PRs', 'Open PRs', 'Closed PRs', 'No merged PRs closed',
                 'No merged including open', 'Merged without review', 'No of comments in PRs',
                 'No of reviews in PRs', 'AVG comments PRs', 'AVG time to first comment in PRs',
                 'AVG time to first review', 'AVG time merge from create', 'AVG time merge from first commit',
                 'AVG time merge from first comment', 'AVG time merge from first review']

    data_values = [prs, open_prs, closed, merged,
                   closed_no_merged, no_merged_total, merged_no_review,
                   comments, reviews, comment_avg, avg_time_first_comment,
                   avg_time_first_review, avg_time_merge_create, avg_time_first_commit,
                   avg_time_merge_comment, avg_time_merge_review]

    try:
        sheet = client.open("GitHub-Report").get_worksheet(0)
    except:
        sheet = client.create("GitHub-Report")
        sheet = client.open("GitHub-Report").get_worksheet(0)

    write = sheet.update('A1:P2', [data_name, data_values])
    print(sheet)

    return flask.jsonify(prs)


@ app_views.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    flow.redirect_uri = flask.url_for(
        'app_views.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable incremental authorization. Recommended as a best practice.
        # include_granted_scopes='true',
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission.
        access_type='offline')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@ app_views.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for(
        'app_views.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(flask.url_for('app_views.show_reports'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
