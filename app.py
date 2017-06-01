import os
from flask import Flask

app = Flask(__name__, static_url_path='/static')

@app.route('/account/auth')
def account_auth():
    return 'Authenticate with Fitbit or Google'

@app.route('/account/edit')
def account_edit():
	return "Update account info after successful authentication"

@app.route('/account/finish')
def account_finish():
	return "Finish account setup"

@app.route('/user/<username>')
def user_graphs(username):
	return "Show graphs page of user"

@app.route('/widget/sum/<username>')
def widget_sum(username):
	return "Graph shows the cumm. distance covered vs cumm. target"

@app.route('/widget/diff/<username>')
def widget_diff(username):
	return "Graph shows the difference between cumm. sum vs cumm. target"

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
