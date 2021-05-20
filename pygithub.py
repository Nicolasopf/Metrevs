from github import Github

# First create a Github instance
# using an access token
g = Github("here should be the access token")


# Then play with Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)
