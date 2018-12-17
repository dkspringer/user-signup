from flask import Flask, request, render_template, redirect, url_for
import re

app = Flask(__name__)

def check_password_match(password, verify):
	"""
	Verifies that the password and the verify password inputs match. Returns
	either an error message if they do not match or a an empty string if they do
	"""
	if not verify:
		return 'This field cannot be left blank'
	if password != verify:
		return 'Passwords do not match'
	return ''

def check_valid(input, input_type):
	"""
	Used to check valid format for both username and password
	"""
	if not input:
		return 'This field cannot be left blank'
	if len(input) < 3:
		return '{} may not be shorter 3 characters'.format(input_type)
	if len(input) > 20:
		return '{} may not be longer than 20 characters'.format(input_type)
	if ' ' in input:
		return '{} may not contain spaces'.format(input_type)
	return ''

def check_email(email):
	"""
	Checks that the e-mail, if given, conforms to a specified pattern.
	Defines the pattern of a valid e-mail address by defining smaller parts of
	an e-mail address and defining larger parts using those smaller parts. The
	overall requirements are adapted from the Wikipedia page on email addresses:
	https://en.wikipedia.org/wiki/Email_address#Syntax
	"""

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

		error_user = check_valid(username, 'Username')
		error_password = check_valid(password, 'Password')
		error_match = check_password_match(password, verify_password)
		error_email = check_email(email)

		if not (error_user or error_password or error_match or error_email):
			return render_template('welcome.html', name=username)
		return render_template('home.html', username=username, email=email, error_password=error_password,
							   error_user=error_user, error_match=error_match, error_email=error_email)

	else:
		return render_template('home.html')

if __name__ == '__main__':
	app.run()