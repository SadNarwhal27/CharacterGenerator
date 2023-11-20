from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/npc', methods=['GET','POST'])
def create_npc():
    race = request.form.get('race')
    gender = request.form.get('gender')
    backstory = request.form.get('backstory')

    # Production
    response = requests.get(os.getenv('API_URL') + f"/npc?race={race}&gender={gender}&backstory={backstory}")

    # For testing
    # response = requests.get('http://127.0.0.1:5001/' + f"/npc?race={race}&gender={gender}&backstory={backstory}")

    return render_template('npc_created.html', response=response.json())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
