#!/usr/bin/python3
''' View /repos show repo information processed requested by the user '''
from views import app_views


@app_views.route('/repos')
def show_repos():
    ''' Show repos information.. '''
    return 'hi'
