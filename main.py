import os
import logging
import random
from flask import Flask, request, jsonify
import json
import numpy
from arena import *

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)


def handlegame():
    try:
        jsonData = request.get_json()
        game_data = json.loads(json.dumps(jsonData))
        logger.info(game_data)
        links = game_data["_links"]
        my_url = links['self']['href']
        arena = game_data["arena"]
        play_arena = Arena(arena['dims'], arena['state'], my_url)
        return play_arena.get_next_move()
    except Exception as err:
        print(err)
        logger.error(err)
        return default_move

        
    #response = make_response(next_move,200)

@app.route("/game", methods=['POST'])
def move():
    request.get_data()
    #logger.info(request.json)
    return handlegame()

    #flip = ['0', '1'] # all possible faces
    #res = flip[random.randrange(len(flip))]
    #if res == 0:
    #    return 'T'
    #else :
     #   return moves[random.randrange(len(moves))]

@app.route("/", methods=['GET'])
def default():
    document = """<html>
    <head>
    <style type="text/css">
        h1 { color: red; }
    </style>
    </head>
    <body><h1>Hello, world.</h1></body>
    </html>"""

    response = make_response(document,200)
    return response

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))