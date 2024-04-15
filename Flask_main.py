import json

from flask import Flask,render_template

app = Flask(__name__)

#Reading the json file content
try:
    with open('player_details_3.json','r') as output_file:
        #output_data = output_file.read()
        output_data = json.load(output_file)
except Exception as arg:
    print("Faced below error while trying to access player batting details json")
    print(arg)

# Reading the batting leaderboard json file content
try:
    with open('batting_leaderboard.json','r') as outfile:
        output_data_2 = json.load(outfile)
except Exception as arg:
    print("Faced below error while trying to access batting leaderboard json")
    print(arg)

# Reading the player bowling details json file content
try:
    with open('batting_leaderboard.json','r') as outfile:
        output_data_bowling = json.load(outfile)
except Exception as arg:
    print("Faced below error while trying to access players bowling details json")
    print(arg)

# Reading the bowling leaderboard json file content
try:
    with open('batting_leaderboard.json','r') as outfile:
        output_data_bowling_2 = json.load(outfile)
except Exception as arg:
    print("Faced below error while trying to access bowling leaderboard json")
    print(arg)

# Reading the fielding leaderboard json file content
try:
    with open('batting_leaderboard.json','r') as outfile:
        output_data_fielding = json.load(outfile)
except Exception as arg:
    print("Faced below error while trying to access fielding leaderboard json")
    print(arg)

@app.route('/')
def home_ui():
    return render_template("Advanced_ui.html", jsonfile=output_data, jsonf_bat_lb=output_data_2)

@app.route('/bowling')
def bowling_ui():
    pass

@app.route('/fieling')
def fielding_ui():
    pass

if __name__ == '__main__':
    app.run()