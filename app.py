import os
from flask import Flask, render_template, request
from fitbit.api import FitbitOauth2Client

app = Flask(__name__, static_url_path='/static')
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
	return oauth.session.token['access_token']

@app.route('/account/finish', methods=['POST'])
def account_finish():
	"""
	Finalize account setup. Save user handle and keys.
	"""
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

@app.route('/widget/sum/<username>')
def widget_sum(username):
	"""
	Widget for sum of distances for user.
	"""
	return "Graph shows the cumm. distance covered vs cumm. target"

@app.route('/widget/diff/<username>')
def widget_diff(username):
	"""
	Widget for diff of distance for user.
	"""
	return "Graph shows the difference between cumm. sum vs cumm. target"

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
