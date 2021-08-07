#!/usr/bin/python3
''' View /repos show repo information processed. '''
from views import app_views
from flask import render_template, request, make_response, redirect, url_for
from github import Github
from datetime import datetime, timedelta


def review_requests(token, repo, developers, reviewers, start_date, end_date):
    """ PR/s = Pull Request/s
    Return a dictionary with the
    """
    user_session = Github(token)  # Start connection using the auth_token
    repo = user_session.get_repo(repo)  # Select the repo from cookie.

    pulls = repo.get_pulls(state='all')

    collaborators = repo.get_collaborators()


    users = {}
    users['reviewers'] = {}
    users['developers'] = {}

    for collaborator in collaborators:
        user_name = collaborator.login
        if user_name in reviewers:
            users['reviewers'][user_name] = {'pending': 0,
                                             'done': 0,
                                             'avg_done': 0,
                                             'time_reviews': [],
                                             'final_times': []}
        if user_name in developers:
            users['developers'][user_name] = {'pending': 0,
                                              'received': 0,
                                              'total_prs': 0}

    # To make a readable code:
    reviewers = users['reviewers']
    developers = users['developers']

    total_prs = 0
    for pull in pulls:
        user = pull.user.login

        if user not in developers:
            continue

        # To make shorter lines and readable code:
        developer = developers[user]

        developer['total_prs'] += 1
        total_prs += 1

        pull_date = pull.created_at
        try:
            if start_date == 0:
                pass
            elif start_date < pull_date and end_date > pull_date:
                pass
            else:
                continue
        except:
            pass

        # Get reviews pending here:
        for page in pull.get_review_requests():
            for request in page:
                developer['pending'] += 1
                if reviewers.get(request.login): # check if reviewer exist.
                    reviewers[request.login]['pending'] += 1 #+1 review pending

        # Check the reviews done and received.
        for review in pull.get_reviews():
            reviewer = review.user.login
            if reviewers.get(reviewer):
                developer['received'] += 1
                reviewers[reviewer]['done'] += 1
                reviewers[reviewer]['time_reviews'].append(review.submitted_at)

        for user, dic in reviewers.items():
            if len(dic['time_reviews']) > 1:
                timedeltas = []
                for i in range(len(dic['time_reviews']) - 1):
                    timedeltas.append(dic['time_reviews'][i + 1] - dic['time_reviews'][i])
                    avg_time = sum(timedeltas, timedelta()) / len(timedeltas)
                    reviewers[user]['final_times'].append(avg_time)
            else:
                ''' Nothing or get the avg the pr open and review? '''
                pass

    """ Set the avg for review in prs """
    for user in reviewers.keys():
        # Get the average reviews received from here:
        if total_prs < reviewers[user]['done']:
            reviewers[user]['avg_done'] = "{:.2f}".format(
                total_prs / reviewers[user]['done'])
        else:
            reviewers[user]['avg_done'] = "{:.2f}".format(
                reviewers[user]['done'] / total_prs)
        # Until here.
        # Get the avg time per review:
        try:
            avg_time = sum(reviewers[user]['time_reviews'], timedelta(
            )) / len(reviewers[user]['time_reviews'])
            reviewers[user]['avg_time_reviews'] = avg_time
        except:
            pass

    return users


def get_data(token, repos):
    """ Get the repos users when the method is GET """
    repos_data = {}
    users_in_repos = []
    user_session = Github(token)

    for repo_name in repos:
        repos_data[repo_name] = {}
        repo = user_session.get_repo(repo_name)
        collaborators = repo.get_collaborators()
        for collaborator in collaborators:
            if collaborator.login not in users_in_repos:
                users_in_repos.append(collaborator.login)

    return repos_data, users_in_repos


@app_views.route('/reviews', methods=["GET", "POST"])
def show_review_info():
    ''' Show the info for the repo selected. This repo is located at cookie. '''
    token = request.cookies.get("userToken")
    repos = request.cookies.get("repos")

    if not token or not repos:
        return redirect(url_for('add_repos'))

    repos = repos.split(", ")

    ''' Structure of repos_data:
    repos_data[repo] = {}
    '''
    repos_data, users_in_repos = get_data(token, repos)

    if request.method == "GET":
        return render_template('reviews.html', repos_data=repos_data,
                               final_user_list=users_in_repos)

    # Get the users to interact with:
    developers = request.form.getlist("devs")
    reviewers = request.form.getlist("reviewers")

    if not developers or not reviewers:
        return render_template('reviews.html', repos_data=repos_data,
        final_user_list=users_in_repos)

    ''' GET THE DATES FROM HERE: '''
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
    ''' UNTIL HERE NO MORE DATES '''

    repos_data = {}
    for repo in repos:
        repos_data[repo] = review_requests(
            token, repo, developers, reviewers, start_date, end_date)

    resp = make_response(render_template(
        'reviews.html', repos_data=repos_data, final_user_list=users_in_repos))
    return resp
