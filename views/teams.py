#!/usr/bin/python3
''' View for /teams show teams data processed '''
from views import app_views


@app_views.route('/teams')
def show_teams():
    ''' Show teams... '''
    return 'hi'
