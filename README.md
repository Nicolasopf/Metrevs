# WayDev_clone
Create a web platform to evaluate team perfomance in GitHub repositories.

## Install
### Requirement: ubuntu 18:04
Installation from zero.
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo pip3 install GitHub-Flask
sudo pip3 install PyGithub
```

### Start application
```
python3 github_login.py
```

You can go to the website at port http://127.0.0.1:5000.

## Why you..?
### Use GitHub-Flask and PyGithub too?
GitHub-Flask give a solution with a database and you need the DB in order to use the api, which we don't want. We prefer to use the api with the authorized_key from cookie by using PyGithub and use GitHub-Flask only for the authentication OAuth2 login.

## Authors
Nicolás Urrea - nico15935746@gmail.com
Diego Ahumada - Xvongola23@gmail.com
Daniel Amado - danielfep.am@gmail.com
