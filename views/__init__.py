#!/usr/bin/python3
''' Initialize blueprint object '''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/')
from views.teams import *
from views.reviews import *
from views.users import *
from views.repos import *
from views.reports import *
