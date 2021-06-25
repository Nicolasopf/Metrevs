#!/usr/bin/python3
''' View /repos show repo information processed. '''
from views import app_views
from flask import render_template, request, make_response, redirect, url_for
from github import Github
from datetime import datetime


def review_data(token, repo, users, start_date, end_date):
    """ Return the reviews data for each user in dictionary.
    Developer
    Reviews requests
    Reviews count
    Reviews done
    Average review in PR
    PR/s = Pull Request/s
    """
    user_session = Github(token)  # Start connection using the auth_token
    repo = user_session.get_repo(repo)  # Select the repo from cookie.

    pulls = repo.get_pulls(state='all')

    collaborators = repo.get_collaborators()
    users_in_repo = []
    for collaborator in collaborators:
        users_in_repo.append(collaborator.login)

    dict_users = {}
    for user in users:
        if user in users_in_repo:
            dict_users[user] = {'requests': 0, 'open_prs': 0, 'closed': 0, 'merged': 0, 'comments': 0, 'merged_no_review': 0, 'reviews': 0,
                                'comment_hours': 0, 'review_hours': 0, 'merged_hours': 0, 'merged_commit_hours': 0, 'merged_comments_hours': 0, 'merged_review_hours': 0}

    print('a')
    for pr in pulls:
        pull_date = pr.created_at
        try:
            if start_date == 0:
                pass
            elif start_date < pull_date and end_date > pull_date:
                pass
            else:
                continue
        except:
            pass

        user = pr.user.login
        if user not in dict_users.keys():
            continue

        for page in pr.get_review_requests():
            print(page)
            for request in page:
                dict_users[user]['requests'] += 1

    print(dict_users)

    return dict_users, users_in_repo


@app_views.route('/reviews', methods=["GET", "POST"])
def show_review_info():
    ''' Show the info for the repo selected. This repo is located at cookie. '''
    if not request.cookies.get("repos") or not request.cookies.get("userToken"):
        return redirect(url_for('add_repos'))

    users = request.form.getlist("username")

    date = request.form.get("trip-start")
    if date:
        temp_date = []
        for num in date.split("-"):
            temp_date.append(int(num))
        start_date = datetime(temp_date[0], temp_date[1], temp_date[2])
    else:
        start_date = 0

    date = request.form.get("trip-end")
    if date:
        temp_date = []
        for num in date.split("-"):
            temp_date.append(int(num))
        end_date = datetime(temp_date[0], temp_date[1], temp_date[2])
    else:
        end_date = datetime.now()

    token = request.cookies.get("userToken")
    repos = request.cookies.get("repos").split(", ")

    user_list = []
    repos_data = {}
    for repo in repos:
        tmp_users = []
        repos_data[repo], tmp_users = review_data(
            token, repo, users, start_date, end_date)
        user_list.append(tmp_users)

    resp = make_response(render_template(
        'reviews.html', repos_data=repos_data))
    return resp
