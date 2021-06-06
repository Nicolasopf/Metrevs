#!/usr/bin/python3
''' View /repos show repo information processed. '''
from views import app_views
from flask import render_template, request
from github import Github


def prs_request(token, repo):
    ''' Retrieves:
    Total PRs: prs
    Open PRs: open_prs
    Closed PRs: closed
    Merged PRs: merged
    Merged without review: merged_no_review
    No of comments in PRs: comments
    No of reviews in PRs: reviews
    '''
    user_session = Github(token)  # Start connection using the auth_token
    repo = user_session.get_repo(repo)  # Select the repo from cookie.

    pulls = repo.get_pulls(state='all')

    prs = pulls.totalCount
    open_prs = 0
    closed = 0

    merged = 0
    comments = 0
    merged_no_review = 0
    reviews = 0
    for pr in pulls:
        if pr.state == "closed":
            closed += 1
            if pr.merged:
                merged += 1
                if pr.get_reviews().totalCount == 0:  # Check if its reviewed
                    merged_no_review += 1
        else:
            open_prs += 1
        comments += pr.comments
        reviews += pr.get_reviews().totalCount

    return prs, open_prs, closed, merged, comments, merged_no_review, reviews


@app_views.route('/repos')
def show_repo_info():
    ''' Show the info for the repo selected. This repo is located at cookie. '''
    if not request.cookies.get("repo") or not request.cookies.get("userToken"):
        return redirect(url_for(panel))

    token = request.cookies.get("userToken")
    repo = request.cookies.get("repo")

    prs, open_prs, closed, merged, comments, merged_no_review, reviews\
        = prs_request(token, repo)

    return render_template('repos.html', prs=prs, open_prs=open_prs, closed=closed,
                           merged=merged, comments=comments, merged_no_review=merged_no_review, reviews=reviews)
