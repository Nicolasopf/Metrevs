#!/usr/bin/python3
''' View /repos show repo information processed. '''
from views import app_views
from flask import render_template, request, make_response, redirect, url_for
from github import Github
from datetime import datetime, timedelta


def review_requests(token, repo, users, start_date, end_date):
    """ Return the reviews data for each user in dictionary.
    Developer = dict_user[user]
    Reviews requests = dict_user['requests']
    Reviews received = dict_user['received']
    Reviews done = dict_user['done']
    Average review in PR = dict_user['avg_received_prs']
    Average time per review = dict_user['avg_time_review']
    PR/s = Pull Request/s
    """
    user_session = Github(token)  # Start connection using the auth_token
    repo = user_session.get_repo(repo)  # Select the repo from cookie.

    pulls = repo.get_pulls(state='all')
    total_prs = 0

    collaborators = repo.get_collaborators()
    users_in_repo = []
    for collaborator in collaborators:
        users_in_repo.append(collaborator.login)

    dict_users = {}
    for user in users:
        if user in users_in_repo:
            dict_users[user] = {'counted_pr': False, 'pending': 0, 'done': 0,
                                'commented': 0, 'request_changes': 0,
                                'approved': 0, 'avg_review_pr': 0,
                                'time_review': [], 'avg_time_reviews': 0}

    review_states = {'CHANGES_REQUESTED': 'request_changes',
                     'COMMENTED': 'commented', 'APPROVED': 'approved'}

    for pr in pulls:
        total_prs += 1
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

        for page in pr.get_review_requests():
            for request in page:
                if dict_users.get(request.login):
                    dict_users[request.login]['pending'] += 1

        time_reviews = []
        for review in pr.get_reviews():
            reviewer = review.user.login
            if reviewer in dict_users.keys():
                dict_users[reviewer]['counted_pr'] = True
                dict_users[reviewer]['done'] += 1
                dict_users[reviewer]['time_reviews'].append(
                    review.submitted_at)
                for key, value in review_states.items():
                    if review.state == key:
                        dict_users[reviewer][value] += 1

        # Check if user requested in this pr:
        for user, dic in dict_users.items():
            if len(time_reviews) > 1:
                timedeltas = []
                for i in range(len(time_reviews) - 1):
                    timedeltas.append(time_reviews[i + 1] - time_reviews[i])
                    avg_time = sum(timedeltas, timedelta()) / len(timedeltas)
                    dict_users[user]['time_reviews'].append(avg_time)
            else:
                ''' Nothing or get the avg the pr open and review? '''
                pass

    """ Set the avg for review in prs """
    for user in dict_users.keys():
        # Get the average reviews received from here:
        if total_prs < dict_users[user]['done']:
            dict_users[user]['avg_review_pr'] = "{:.2f}".format(
                total_prs / dict_users[user]['done'])
        else:
            dict_users[user]['avg_review_pr'] = "{:.2f}".format(
                dict_users[user]['done'] / total_prs)
        # Until here.
        # Get the avg time per review:
        try:
            avg_time = sum(dict_users[user]['time_reviews'], timedelta(
            )) / len(dict_users[user]['time_reviews'])
            dict_users[user]['avg_time_reviews'] = avg_time
        except:
            pass

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
        repos_data[repo], tmp_users = review_requests(
            token, repo, users, start_date, end_date)
        user_list.append(tmp_users)

    final_user_list = []
    for users in user_list:
        if (isinstance(users, list)):
            for user in users:
                if user not in final_user_list:
                    final_user_list.append(user)
        else:
            if users not in final_user_list:
                final_user_list.append(group)

    resp = make_response(render_template(
        'reviews.html', repos_data=repos_data, final_user_list=final_user_list))
    return resp
