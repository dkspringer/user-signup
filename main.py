from flask import Flask, request, render_template, redirect, url_for
import re

app = Flask(__name__)

def check_password_match(password, verify):
	if not password or not verify:
		return 'You must submit a password'
	if password != verify:
		return 'Passwords do not match'
	return ''

def check_valid_username(username):
	if len(username) < 3:
		return 'Username may not be shorter 3 characters'
	if len(username) > 20:
		return 'Username may not be longer than 20 characters'
	if ' ' in username:
		return 'Username may not contain spaces'
	return ''

def check_email(email):
	if not email:
		return ''

	special = "!#$%&'*+\-\/=?^_`{|}~" # special characters allowed
	alpha = "a-zA-Z"
	num = "0-9"
	chars = alpha+num+special # permitted characters
	dotted = '[{0}](\.?[{1}]+)*'.format(chars, chars)
	domain = '\.[a-zA-Z]{2,3}' # i.e. '.com' or '.edu'

	pattern_string = '^{0}@{1}{2}$'.format(dotted, dotted, domain)
	pattern = re.compile(pattern_string)

	if not re.match(pattern, email):
		return 'Invalid email address'
	else:
		return ''



@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		verify_password = request.form.get('verify')
		email = request.form.get('email')

		msg_user = check_valid_username(username)
		msg_passwd = check_password_match(password, verify_password)
		msg_email = check_email(email)

		if not (msg_user or msg_passwd or msg_email):
			return render_template('welcome.html', name=username)
		return redirect(url_for('index', msg_user=msg_user,
						msg_passwd=msg_passwd, msg_email=msg_email))

	else:
		# Error messages
		msg_user = request.args.get('msg_user')
		msg_passwd = request.args.get('msg_passwd')
		msg_email = request.args.get('msg_email')

		return render_template('home.html', msg_user=msg_user,
							   msg_passwd=msg_passwd, msg_email=msg_email)

if __name__ == '__main__':
	app.run()