import json

from flask import Flask,render_template

app = Flask(__name__)

#Reading the json file content
with open('player_details_3.json','r') as output_file:
    #output_data = output_file.read()
    output_data = json.load(output_file)

@app.route('/')
def home_ui():
    return render_template("Advanced_ui.html", jsonfile=output_data)

if __name__ == '__main__':
    app.run()