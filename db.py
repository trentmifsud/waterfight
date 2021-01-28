import datetime
import math

import time
from player import Player
import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore

class Db:
    
    def __init__(self, game_state_json):
        self.record_limit = 10
        self.SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
        try:
            if self.SECRET_KEY is False:
                cred = credentials.Certificate('sec/drtrentgame-bf9347d2d419.json')
                firebase_admin.initialize_app(cred)
        except Exception as err:
            print(err)

        self.db = firestore.client()
        myTimestamp = time.time()
        self.db.collection(u'game_state').document(str(myTimestamp)).set(game_state_json)
    
    def get_data_firestore(self):

        try:
            game_states = self.db.collection(u'game_state')

            results = game_states.get()
            results.reverse()
            #if len(results) > self.record_limit :
                # we will have to batch delete
             #   pass
            dictionary = {}
            counter = 0
            for doc in results:
                if counter < self.record_limit :
                    dictionary[doc.id] = doc.to_dict()
                    counter = counter +1
                else:
                    self.db.collection(u'game_state').document(doc.id).delete()
            return dictionary
        except Exception as err:
            print(err)
            return None
        
    def removekey(d, key):
        r = dict(d)
        del r[key]
        return r