import os
from flask import Flask, render_template, request
from fitbit.api import FitbitOauth2Client
from flask.ext.sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
oauth = FitbitOauth2Client(os.environ['FITBIT_APP_ID'], os.environ['FITBIT_APP_SECRET'])

@app.route('/account/login')
def account_login():
	"""
	Login page for user to start the login process.
	"""
	url,_ = oauth.authorize_token_url(redirect_uri=request.url_root + "account/edit", 
		scope=['activity'])
	return render_template('login.html', fitbit_auth_url=url)

@app.route('/account/edit', methods=['GET'])
def account_edit():
	"""
	Login validation and account edit
	"""
	oauth.fetch_access_token(request.args.get('code', ''), request.url_root + "account/edit")
	return render_template('account_edit.html', access_token=oauth.session.token['access_token'], 
		refresh_token=oauth.session.token['refresh_token'])

@app.route('/account/finish', methods=['POST'])
def account_finish():
	"""
	Finalize account setup. Save user handle and keys.
	"""
	activities = []
	if request.form['Running']:
		activities.append('Running')
	if request.form['Bike']
		activities.append('Bike')
	try:
		user = User(username=request.form['username'], access_token=request.form['access_token'], 
			refresh_token=request.form['refresh_token'], target=request.form['target'], 
			activities=activities)
		db.session.add(user)
		db.session.commit()
	except Exception as e:
		return "Unable to save to database."
	return "Finish account setup"

@app.route('/user/<username>')
def user_graphs(username):
	"""
	Graphs of user.
	"""
	return "Show graphs page of user"

@app.route('/user/<username>/update')
def user_update(username):
	"""
	Update data for given user.
	"""
	return "Update data for user"

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
