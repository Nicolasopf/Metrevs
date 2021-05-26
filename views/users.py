#!/usr/bin/python3
''' View /users show data about each user requested by the customer '''
from views import app_views


@app_views.route('/users')
def show_user():
    ''' Show users... '''
    return 'hi'
