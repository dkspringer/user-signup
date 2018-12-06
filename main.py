from flask import Flask, request, render_template

app = Flask(__name__)

def check_password_match(password, verify):
	return password == verify

def check_valid_username(username):
	if len(username) < 3:
		return 'Username may not be shorter 3 characters'
	if len(username) > 20:
		return 'Username may not be longer than 20 characters'
	if ' ' in username:
		return 'Username may not contain spaces'
	return ''

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		verify_password = request.form.get('verify')
		email = request.form.get('email')

		return render_template('welcome.html', name=username)
	else:
		return render_template('home.html')

if __name__ == '__main__':
	app.run()