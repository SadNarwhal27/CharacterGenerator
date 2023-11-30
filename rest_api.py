from CardBuilder import CardTemplates
from flask import Flask, request
import os

app = Flask(__name__)

@app.get('/npc')
def get_npc():
    data_filters = dict(request.args) # Turns url arguments into filter dictionary
    card = CardTemplates().create_NPC(data_filters)
    return card

@app.get('/item')
def get_item():
    data_filters = dict(request.args)
    card = CardTemplates().create_item(data_filters)
    return card

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
