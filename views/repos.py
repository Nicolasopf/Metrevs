#!/usr/bin/python3
''' View /repos show repo information processed. '''
from views import app_views
from flask import render_template, request
from github import Github


def division(num1, num2):
    ''' divide two numbers. '''
    if num1 > 0 and num2 > 0:
        return num1 / num2
    return 0


def subtract(datetime1, datetime2):
    try:
        return (datetime1 - datetime2)
    except:
        return 0


def prs_requests(token, repo):
    ''' Retrieves:
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

    prs = pulls.totalCount
    open_prs = 0
    closed = 0

    merged = 0
    comments = 0
    merged_no_review = 0
    reviews = 0
    comment_hours = 0
    review_hours = 0
    merged_hours = 0
    merged_commit_hours = 0
    merged_comments_hours = 0
    merged_review_hours = 0

    for pr in pulls:
        if pr.state == "closed":
            closed += 1
            if pr.merged:
                merged += 1
                if pr.get_reviews().totalCount == 0:  # Check if its reviewed
                    merged_no_review += 1

            # Get the avg time to merge from create:
            merged_date = pr.merged_at
            time_from_created = subtract(pull_date, merged_date)
            if not isinstance(time_from_created, int):
                merged_hours += time_from_created.seconds / 3600

            # Get the avg time to merge from first commit:
            try:
                commit_date = pr.get_commits()[0].commit.committer.date
                time_from_created = subtract(merged_date, commit_date)
                if not isinstance(time_from_created, int):
                    merged_commit_hours += time_from_created.seconds / 3600
            except:
                continue

            # Get the avg time to merge from first comment:
            try:
                comment_date = pr.get_issue_comments()[0].created_at
                time_from_created = subtract(merged_date, commit_date)
                if not isinstance(time_from_created, int):
                    merged_comments_hours += time_from_created.seconds / 3600
            except:
                continue

            # Get the avg time to merge from first review:
            try:
                review_date = pr.get_reviews()[0].submitted_at
                time_from_created = subtract(merged_date, review_date)
                if not isinstance(time_from_created, int):
                    merged_review_hours += time_from_created.seconds / 3600
            except:
                continue
        else:
            open_prs += 1

        comments += pr.comments
        reviews += pr.get_reviews().totalCount

        pull_date = pr.created_at

        # Get the avg time to first comment
        try:
            comment_date = pr.get_issue_comments()[0].created_at
            time_from_created = subtract(pull_date, comment_date)
            if not isinstance(time_from_created, int):
                comment_hours += time_from_created.seconds / 3600
        except:
            continue

        # Get the avg time to first review:
        try:
            review_date = pr.get_reviews()[0].submitted_at
            time_from_created = subtract(pull_date, review_date)
            if not isinstance(time_from_created, int):
                review_hours += time_from_created.seconds / 3600
        except:
            continue

    # Get the percentages:
    comment_avg = '{:.2f}'.format(division(comments, prs))
    avg_time_first_comment = '{:.2f}'.format(
        division(comment_hours, pulls.totalCount))
    avg_time_first_review = '{:.2f}'.format(
        division(review_hours, pulls.totalCount))
    avg_time_merge_create = '{:.2f}'.format(
        division(merged_hours, pulls.totalCount))
    avg_time_first_commit = '{:.2f}'.format(
        division(merged_commit_hours, pulls.totalCount))
    avg_time_merge_comment = '{:.2f}'.format(
        division(merged_comments_hours, pulls.totalCount))
    avg_time_merge_review = '{:.2f}'.format(
        division(merged_review_hours, pulls.totalCount))

    return prs, open_prs, closed, merged, comments, merged_no_review, reviews,\
        comment_avg, avg_time_first_comment, avg_time_first_review,\
        avg_time_merge_create, avg_time_first_commit, avg_time_first_comment,\
        avg_time_merge_comment, avg_time_merge_review


@app_views.route('/repos')
def show_repo_info():
    ''' Show the info for the repo selected. This repo is located at cookie. '''
    if not request.cookies.get("repo") or not request.cookies.get("userToken"):
        return redirect(url_for(panel))

    token = request.cookies.get("userToken")
    repo = request.cookies.get("repo")

    prs, open_prs, closed, merged, comments, merged_no_review, reviews,\
        comment_avg, avg_time_first_comment, avg_time_first_review,\
        avg_time_merge_create, avg_time_first_commit, avg_time_first_comment,\
        avg_time_merge_comment, avg_time_merge_review = prs_requests(
            token, repo)

    return render_template('repos.html', prs=prs,
                           open_prs=open_prs,
                           closed=closed,
                           merged=merged,
                           comments=comments,
                           merged_no_review=merged_no_review,
                           reviews=reviews,
                           comment_avg=comment_avg,
                           avg_time_first_comment=avg_time_first_comment,
                           avg_time_first_review=avg_time_first_review,
                           avg_time_merge_create=avg_time_merge_create,
                           avg_time_first_commit=avg_time_first_commit,
                           avg_time_merge_comment=avg_time_merge_comment,
                           avg_time_merge_review=avg_time_merge_review)
