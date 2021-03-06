#!/usr/bin/python3
''' View /repos show repo information processed. '''
from views import app_views
from flask import render_template, request, make_response, redirect, url_for
from github import Github
from datetime import datetime


def division(num1, num2):
    ''' divide two numbers. '''
    if num1 > 0 and num2 > 0:
        return num1 / num2
    return 0


def get_hours(datetime1, datetime2):
    ''' Get the difference in hours. '''
    try:
        if datetime1 > datetime2:
            time_from_created = datetime1 - datetime2
        else:
            time_from_created = datetime2 - datetime1
        return time_from_created.seconds / 3600
    except:
        return 0


def average_float(num1, pulls):
    ''' Return in float of two points, the result. '''
    result = 0
    if num1 > 0 and pulls > 0:
        result = num1 / pulls
    return "{:.2f}".format(result)


def prs_requests(token, repo, users, start_date, end_date):
    '''
    Function with all requests needed to get data; prs = pull requests.
    Retrieves:
    Total PRs: prs
    Open PRs: open_prs
    Closed PRs: closed
    Merged PRs: merged
    Merged without review: merged_no_review
    No of comments in PRs: comments
    No of reviews in PRs: reviews
    AVG comments PRs: comment_avg
    AVG time to first comment in PRs: avg_time_first_comment
    AVG time to first review: avg_time_first_review
    AVG time merge from create: avg_time_merge_create
    AVG time merge from first commit: avg_time_first_commit
    AVG time merge from first comment: avg_time_merge_comment
    AVG time merge from first review: avg_time_merge_review
    '''
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
            dict_users[user] = {'prs': 0, 'open_prs': 0, 'closed': 0, 'merged': 0, 'comments': 0, 'merged_no_review': 0, 'reviews': 0,
                                'comment_hours': 0, 'review_hours': 0, 'merged_hours': 0, 'merged_commit_hours': 0, 'merged_comments_hours': 0, 'merged_review_hours': 0}

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
        dict_users[user]['prs'] += 1
        if pr.state == "closed":
            dict_users[user]['closed'] += 1
            if pr.merged:
                dict_users[user]['merged'] += 1
                if pr.get_reviews().totalCount == 0:  # Check if its reviewed
                    dict_users[user]['merged_no_review'] += 1
                # Get the avg time to merge from create:
                merged_date = pr.merged_at
                dict_users[user]['merged_hours'] += get_hours(
                    pull_date, merged_date)

            # Get the avg time to merge from first commit:
            try:
                commit_date = pr.get_commits()[0].commit.committer.date
                dict_users[user]['merged_commit_hours'] += get_hours(
                    merged_date, commit_date)
            except:
                pass

            # Get the avg time to merge from first comment:
            try:
                comment_date = pr.get_issue_comments()[0].created_at
                dict_users[user]['merged_comments_hours'] += get_hours(
                    merged_date, comment_date)
            except:
                pass

            # Get the avg time to merge from first review:
            try:
                review_date = pr.get_reviews()[0].submitted_at
                dict_users[user]['merged_review_hours'] += get_hours(
                    merged_date, review_date)
            except:
                pass
        else:
            dict_users[user]['open_prs'] += 1

        dict_users[user]['comments'] += pr.comments
        dict_users[user]['reviews'] += pr.get_reviews().totalCount
        # Get the avg time to first comment
        try:
            comment_date = pr.get_issue_comments()[0].created_at
            dict_users[user]['comment_hours'] += get_hours(
                pull_date, comment_date)
        except:
            pass

        # Get the avg time to first review:
        try:
            review_date = pr.get_reviews()[0].submitted_at
            time_from_created = subtract(pull_date, review_date)
            dict_users[user]['review_hours'] += get_hours(
                pull_date, review_date)
        except:
            pass

    # Get the percentages:
    for user in dict_users.keys():
        tmp = dict_users[user]
        tmp['comment_avg'] = average_float(tmp['comments'], tmp['prs'])
        tmp['avg_time_first_comment'] = average_float(
            tmp['comment_hours'], tmp['prs'])
        tmp['avg_time_first_review'] = average_float(
            tmp['review_hours'], tmp['prs'])
        tmp['avg_time_merge_create'] = average_float(
            tmp['merged_hours'], tmp['merged'])
        tmp['avg_time_first_commit'] = average_float(
            tmp['merged_commit_hours'], tmp['merged'])
        tmp['avg_time_merge_comment'] = average_float(
            tmp['merged_comments_hours'], tmp['merged'])
        tmp['avg_time_merge_review'] = average_float(
            tmp['merged_review_hours'], tmp['merged'])

    return dict_users, users_in_repo


@app_views.route('/repos', methods=["GET", "POST"])
def show_repo_info():
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
        repos_data[repo], tmp_users = prs_requests(token, repo, users, start_date, end_date)
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

    '''
    Set cookie for charts:
    Format: "," for each item, "-" for each chart.
    '''
    resp = make_response(render_template('repos.html', repos_data=repos_data,
    final_user_list=final_user_list))
    prs = 0
    open_prs = 0
    closed = 0
    time_merge = ""
    comments = ""
    merged = ""
    for key, user in repos_data[repo].items():
        prs += user['prs']
        open_prs += user['open_prs']
        closed += user['closed']
        time_merge += "{}:{}, ".format(key,
                                       float(user['avg_time_merge_create']))
        comments += "{}:{}, ".format(key, user['comments'])
        merged += "{}:{}, ".format(key, user['merged'])

    resp.set_cookie("chartsData", "{}, {}, {}-{}-{}-{}".format(prs,
                                                               open_prs, closed, time_merge, comments, merged))
    return resp
