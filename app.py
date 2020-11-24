from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from db_query import searchGame


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
	if not request.form.get('search'):
		return "invalid search"
	game_list = searchGame(request.form.get('search'))
	if game_list == None:
		return "No such game is found"
	return str(game_list)
if __name__ == "__main__":
	app.run(debug=True)