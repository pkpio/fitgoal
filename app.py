import os
from flask import Flask, render_template, request
from fitbit.api import FitbitOauth2Client
import fitbit
from flask.ext.sqlalchemy import SQLAlchemy
from activity import FitbitActivity
import json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
START_DATE = "2017-01-01" # Tracking from start of 2017

from models import *
client_id = os.environ['FITBIT_APP_ID']
client_secret = os.environ['FITBIT_APP_SECRET']
verification_code = os.environ['FITBIT_VERIFICATION_CODE']
oauth = FitbitOauth2Client(client_id, client_secret)

@app.route('/')
def account_login():
	"""
	Login page for user to start the login process.
	"""
	url,_ = oauth.authorize_token_url(redirect_uri=request.url_root + "auth", 
		scope=['activity', 'profile'])
	return render_template('login.html', fitbit_auth_url=url)

@app.route('/auth', methods=['GET'])
def account_edit():
	"""
	Login validation and account edit
	"""
	oauth.fetch_access_token(request.args.get('code', ''), request.url_root + "auth")
	return render_template('account_edit.html', access_token=oauth.session.token['access_token'], 
		refresh_token=oauth.session.token['refresh_token'], 
		token_expiry_at=oauth.session.token['expires_at'])

@app.route('/save', methods=['GET', 'POST'])
def account_finish():
	"""
	Finalize account setup. Save user handle and keys.
	"""
	activities = []
	if request.form.get('Running', None):
		activities.append('Run')
	if request.form.get('Biking', None):
		activities.append('Bike')
	try:
		fitbit_client = fitbit.Fitbit(client_id, client_secret, 
			access_token=request.form['access_token'], 
			refresh_token=request.form['refresh_token'])
		profile = fitbit_client.user_profile_get()
		user = User(
			username=request.form['username'],
			fitbitid=profile['user']['encodedId'],
			access_token=request.form['access_token'], 
			refresh_token=request.form['refresh_token'], 
			token_expires_at=request.form['token_expiry_at'],
			target=request.form['target'], activities=activities
			)
		db.session.add(user)
		db.session.commit()
	except Exception as e:
		return "Unable to save to database."
	return render_template('save.html', username=user.username)

@app.route('/graphs/<username>')
def user_graphs(username):
	"""
	Graphs of user.
	"""
	user = User.query.filter_by(username=username).first()
	if not user:
		return 'User {} not found'.format(username)
	return render_template('graphs.html', distances=user.distances, target=user.target)

def update_data(user):
	"""
	Update data for given user.
	"""
	fitbit_activity = FitbitActivity(client_id, client_secret, access_token=user.access_token, 
		refresh_token=user.refresh_token, token_expires_at=user.token_expires_at,
		types=user.activities)
	user.distances = fitbit_activity.get_distances()
	user.access_token = fitbit_activity.access_token();
	user.refresh_token = fitbit_activity.refresh_token();
	user.token_expires_at = fitbit_activity.token_expires_at();
	db.session.commit()

@app.route('/update/<username>')
def update_manual(username):
	"""
	Update data for given username.
	"""
	user = User.query.filter_by(username=username).first()
	if not user:
		return 'User {} not found'.format(username)
	update_data(user)
	return render_template('update.html', graph_url='/graphs/{}'.format(user.username))

@app.route('/update', methods=['POST'])
def update_fitbit_push():
	"""
	This endpoint is called by fitbit whenever there is a new activity for a user. Update by push.
	"""
	fitbitid = json.loads(request.data)[0]['ownerId']
	user = User.query.filter_by(fitbitid=fitbitid).first()
	if user:
		update_data(user)
	return 'thanks fitbit', 204

@app.route('/update', methods=['GET'])
def verify_subscription():
	"""
	This endpoint is called by fitbit for verification of subscription endpoint.
	"""
	received_code = request.args.get('verify', '')
	print(verification_code)
	if received_code == verification_code:
		return 'correct', 204
	else:
		return 'incorrect', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
