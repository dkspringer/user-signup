from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		username = request.form.get('username')
		return render_template('welcome.html', name=username)
	else:
		return render_template('home.html')

if __name__ == '__main__':
	app.run()