#!/usr/bin/python3
''' View for the /reposrts to export a report of the data requeted. '''
from views import app_views
from github import Github as github_api


@app_views.route('/reports')
def show_reports():
    ''' Show reports... '''
    return 'hi'
