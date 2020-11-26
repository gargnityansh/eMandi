from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from db_query import searchGame
from flask_cors import CORS
import json


app = Flask(__name__)
Bootstrap(app)
CORS(app)

@app.route('/')
def index():
	games = searchGame("%")
	print(games)
	print("\n this is going", jsonify(games))
	return render_template('index.html', games=games)
	#return jsonify(games)

@app.route('/search',  methods=['GET'])
def search():
	print("hello mr. how do you do",request.args.get('search'))
	if not request.args.get('search'):
		return "invalid search"
	game_list = searchGame(request.args.get('search'))
	if game_list == None:
		return "No such game is found"
	print("in the app.py : ",game_list)
	return render_template('index.html', games=game_list)
	#return jsonify(game_list)

if __name__ == "__main__":
	app.run(debug=True)