from arena import *
import os
import sys
from flask import Flask
from flask import request, make_response
from flask.wrappers import Response
import json
from flask import jsonify
import logging
import numpy


app = Flask(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

@app.route("/game",  methods = ['GET', 'POST'])
def game_handler():
    logger.info(request.json)
    
    #print(request)
    if request.method == 'POST':
        jsonData = request.get_json()
        game_data = json.loads(json.dumps(jsonData))
        links = game_data["_links"]
        my_url = links['self']['href']
        arena = game_data["arena"]
        play_arena = Arena(arena['dims'], arena['state'], my_url)
        next_move = play_arena.get_next_move()
        response = make_response(next_move,200)
        return response
    if request.method == 'GET':
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
    else :
        status_code = make_response("X",200)
        return status_code

if __name__ == "__main__":
    print('starting')
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]
