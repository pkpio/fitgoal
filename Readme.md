# Setup
------------------------

Local
-------
- Init a virtual environment `python3 -m venv env`
- [Optional] Install [autoenv](https://github.com/kennethreitz/autoenv) `pip install autoenv==1.0.0`
- Activate virtual environment and variables `source .env`
- Install dependencies in virtual environment `pip install -r requirements.txt`

Heroku
--------
Below steps are required only of you want to deploy the app to Heroku.

- Install [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli), [login](https://devcenter.heroku.com/articles/heroku-cli#getting-started) and [add your ssh key to heroku](https://devcenter.heroku.com/articles/keys#adding-keys-to-heroku)
- Create a Heroku app `heroku create YOUR-APP-NAME` (pick a app name)
- Add remote branch `git remote add heroku git@heroku.com:YOUR-APP-NAME.git`


# Running
------------------------

Locally
--------
- Execute `python app.py`
- Access app at http://localhost:5000/

Heroku
--------
- Push code to Heroku `git push heroku master`
- Access app at https://YOUR-APP-NAME.herokuapp.com/



