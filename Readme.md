# Fitgoal Intro
------------------------
Tracks total distance covered by Fitbit user in this year using [simple graphs](https://fitgoal.pkp.io/graphs/347TCH). Activities to track can be selected by the user.


# Setup
------------------------
These instructions are for deploying your own version of this app. For normal use, you can just use the [website](https://fitgoal.pkp.io).

Local
-------
- Init a virtual environment `python3 -m venv env`
- Install [autoenv](https://github.com/kennethreitz/autoenv) `pip install autoenv==1.0.0`
- Activate virtual environment and variables `cd .` or `source .env`
- Install dependencies in virtual environment `pip install -r requirements.txt`
- (Optional) Install Redis, if you want to test subscriptions locally. On Mac run `brew install redis`

Heroku (optional)
--------
Below steps are required only if you want to deploy the app to Heroku.

- Install [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli) and [login](https://devcenter.heroku.com/articles/heroku-cli#getting-started)
- Create a Heroku app `heroku create HEROKU-APP-NAME` (pick your app name)
- Set deploy configuration `heroku config:set APP_SETTINGS=config.StagingConfig`
- Enable Redis `heroku addons:create heroku-redis:hobby-dev`

Fitbit
-------
Create a [Fitbit app](https://dev.fitbit.com/apps/new) with below values.

- OAuth 2.0 Application Type: `Server`
- Callback URL:

```
http://localhost:5000/account/edit
http://HEROKU-APP-NAME.herokuapp.com/auth
https://HEROKU-APP-NAME.herokuapp.com/auth
```
- Add a subscriber (only for heroku or remote deployments)
```
Default
Endpoint URL: https://HEROKU-APP-NAME.herokuapp.com/update
Type: JSON Body
Subscriber ID: 1
```
- For local setup, create a file named `.secrets` with following template and values of your Fitbit app
```shell
export FITBIT_APP_ID="OAuth 2.0 Client ID"
export FITBIT_APP_SECRET="Client Secret"
```
- For heroku setup, run following commands using values of your Fitbit app
```shell
heroku config:set FITBIT_APP_ID="OAuth 2.0 Client ID"
heroku config:set FITBIT_APP_SECRET="Client Secret"
heroku config:set FITBIT_VERIFICATION_CODE="Subscriber Verification Code"
```

Setup Database
--------
- Install [Postgres](https://www.postgresql.org/download/) and open Postgres shell `psql`
- Create a database `create database fitgoal;` and exit `\q`
- Setup local database `python manage.py db upgrade`
- Enable Postgres on Heroku `heroku addons:create heroku-postgresql:hobby-dev`
- Setup heroku database `heroku run python manage.py db upgrade`


# Running
------------------------

Locally
--------
- Execute `python app.py`
- (Optional) Do these only if you want to test Subscriptions locally
	- Start Redis server in a new terminal `redis-server`
	- Start worker in a new terminal `python worker.py`

Heroku
--------
- Push code to Heroku `git push heroku`
- Verify Subscribers endpoint from your [Fitbit app's page](https://dev.fitbit.com/apps).
