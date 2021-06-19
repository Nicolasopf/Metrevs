# Metrevs
Web platform to evaluate developers performance in GitHub repositories.
![image](https://user-images.githubusercontent.com/69660332/122605133-a59bd300-d03c-11eb-877b-6b7589836048.png)

## Install
### Requirement: ubuntu 18:04
Installation from zero.
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo pip3 install GitHub-Flask
sudo pip3 install gspread
sudo pip3 install PyGithub
```

### Start application
If you want to test or use in your localhost, don't forget to create an OAuth app in https://github.com/settings/developers
Also, use the client_id and client_secret as environment variables when executing main.py.

```
GITHUB_CLIENT_ID=id GITHUB_CLIENT_SECRET=secret main.py
```

You can go to the website at port http://127.0.0.1:5000.

## Why you..?
### Use GitHub-Flask and PyGithub too?
GitHub-Flask give a solution with a database and you need the DB in order to use the api, which we don't want. We prefer to use the api with the authorized_key from cookie by using PyGithub and use GitHub-Flask only for the authentication OAuth2 login.

## Authors
Nicolás Urrea - nico15935746@gmail.com\
Diego Ahumada - Xvongola23@gmail.com\
Daniel Amado - danielfep.am@gmail.com
