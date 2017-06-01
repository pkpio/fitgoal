import os
from flask import Flask, render_template, request

# constants
FITBIT_AUTH_BASE = "https://www.fitbit.com/oauth2/authorize?response_type=code&scope=activity&expires_in=604800"

app = Flask(__name__, static_url_path='/static')

@app.route('/account/login')
def account_login():
	"""
	Login page for user to start the login process.
	"""
	auth_url = FITBIT_AUTH_BASE + "&client_id={}&redirect_uri={}".format(os.environ['FITBIT_APP_ID'], request.url_root + "account/edit")
	return render_template('login.html', fitbit_auth_url=auth_url)

@app.route('/account/edit', methods=['GET'])
def account_edit():
	"""
	Login validation and account edit
	"""
	return request.args.get('code', '')

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
