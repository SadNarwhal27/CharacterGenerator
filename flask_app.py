from CardBuilder import CardTemplates
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/character', methods=['POST'])
def create_character():
    card = CardTemplates().create_NPC()
    return render_template('npc_created.html', card=card)

if __name__ == '__main__':
    app.run(debug=True)
