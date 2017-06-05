import os
from flask import Flask, render_template, request
from fitbit.api import FitbitOauth2Client
import fitbit
from flask.ext.sqlalchemy import SQLAlchemy
from activity import FitbitActivity
from rq import Queue
from rq.job import Job
from worker import conn
from convertor import Convertor

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)
START_DATE = "2017-01-01" # Tracking from start of 2017

from models import *
client_id = os.environ['FITBIT_APP_ID']
client_secret = os.environ['FITBIT_APP_SECRET']
verification_code = os.getenv('FITBIT_VERIFICATION_CODE', '')
oauth = FitbitOauth2Client(client_id, client_secret)

def auth_redirect_url():
	base_domain = request.url_root[request.url_root.find('://'):]
	protocol = 'https' if 'DYNO' in os.environ else 'http'
	return "{}{}auth".format(protocol, base_domain)

@app.route('/')
def account_login():
	"""
	Login page for user to start the login process.
	"""
	print(auth_redirect_url())
	url,_ = oauth.authorize_token_url(redirect_uri=auth_redirect_url(), 
		scope=['activity', 'profile'])
	return render_template('login.html', fitbit_auth_url=url)

@app.route('/auth', methods=['GET'])
def account_edit():
	"""
	Login validation and account edit
	"""
	oauth.fetch_access_token(request.args.get('code', ''), auth_redirect_url())
	return render_template('account_edit.html', access_token=oauth.session.token['access_token'], 
		refresh_token=oauth.session.token['refresh_token'], 
		token_expiry_at=oauth.session.token['expires_at'])

def get_selected_activities():
	activities = []
	if request.form.get('Walking', None):
		activities.append('Walk')
	if request.form.get('Running', None):
		activities.append('Run')
		activities.append('Treadmill')
	if request.form.get('Biking', None):
		activities.append('Bike')
	if request.form.get('Swimming', None):
		activities.append('Swim')
	if request.form.get('Rowing', None):
		activities.append('Rowing')
		activities.append('Rowing Machine')
	if request.form.get('Hiking', None):
		activities.append('Hike')
	return activities


@app.route('/save', methods=['GET', 'POST'])
def account_finish():
	"""
	Finalize account setup. Save user handle and keys.
	"""
	fitbit_client = fitbit.Fitbit(client_id, client_secret, 
		access_token=request.form['access_token'], 
		refresh_token=request.form['refresh_token'])
	profile = fitbit_client.user_profile_get()
	dbuser = User.query.filter_by(fitbitid=profile['user']['encodedId']).first()
	newuser = User(
		fitbitid=profile['user']['encodedId'],
		fullname=profile['user']['fullName'],
		access_token=request.form['access_token'], 
		refresh_token=request.form['refresh_token'], 
		token_expires_at=request.form['token_expiry_at'],
		target=request.form['target'], activities=get_selected_activities()
		)
	if dbuser:
		newuser.id = dbuser.id
	db.session.merge(newuser)
	db.session.commit()
	fitbit_client.subscription(subscription_id=newuser.fitbitid, subscriber_id="1", 
		collection='activities')
	update_data(newuser.fitbitid)
	return render_template('save.html', username=newuser.fullname, fitbitid=newuser.fitbitid)

@app.route('/graphs/<fitbitid>')
def user_graphs(fitbitid):
	"""
	Graphs of user.
	"""
	user = User.query.filter_by(fitbitid=fitbitid).first()
	if not user:
		return 'User {} not found'.format(fitbitid)
	# update if data is older than a day
	if len(user.distances) < Convertor(START_DATE).daysSinceStart('today') + 1:
		update_data(fitbitid)
		user = User.query.filter_by(fitbitid=fitbitid).first()
	return render_template('graphs.html', fullname=user.fullname, distances=user.distances, 
		target=user.target)

def update_data(fitbitid):
	"""
	Update data for user with given fitbitid.
	"""
	user = User.query.filter_by(fitbitid=fitbitid).first()
	if not user:
		return None
	fitbit_activity = FitbitActivity(client_id, client_secret, access_token=user.access_token, 
		refresh_token=user.refresh_token, token_expires_at=user.token_expires_at,
		types=user.activities)
	user.distances = fitbit_activity.get_distances()
	user.access_token = fitbit_activity.access_token();
	user.refresh_token = fitbit_activity.refresh_token();
	user.token_expires_at = fitbit_activity.token_expires_at();
	db.session.commit()
	return user

@app.route('/update', methods=['POST'])
def update_fitbit_push():
	"""
	This endpoint is called by fitbit whenever there is a new activity for a user. Update by push.
	"""
	fitbitid = request.get_json()[0]['ownerId']
	jobid = q.enqueue_call(func='app.update_data', args=(fitbitid,), result_ttl=5000)
	print("scheduled update for {} with jobid: {}".format(fitbitid, jobid))
	return 'thanks fitbit', 204

@app.route('/update', methods=['GET'])
def verify_subscription():
	"""
	This endpoint is called by fitbit for verification of subscription endpoint.
	"""
	received_code = request.args.get('verify', '')
	if received_code == verification_code:
		return 'correct', 204
	else:
		return 'incorrect', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
