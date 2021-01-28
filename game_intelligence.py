import datetime
import math
from google.cloud import firestore
import time
from player import Player
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




class Game_Intelligence(object):
    
    successive_hits = 0
    bossy_player = None
    currently_retreating = False
    my_player = None
    other_players = None
    dimensions = None
    my_score_trend = None
    recent_score_for_trends = []
    recent_score_for_trends_size = 10
    recent_score_for_trends_index = 0
    successive_hits_threshold = 5
    camping_threshold = 10


    def __init__(self,historic_state):
        self.historic_state_array = []
        self.this_round_players = []
        self.historic_state = historic_state
        for state in self.historic_state:
            self.historic_state_array.append(self.historic_state[state])
        self.process_historic_state()

    def process_historic_state(self):
        
        count = 0
        self.all_players = []
        for state in self.historic_state_array:
            print(state)
            self.links = state["_links"]
            self.my_url = self.links['self']['href']
            self.arena = state["arena"]        
            self.dimensions = self.arena['dims']

            for i, (k, v) in enumerate(self.arena['state'].items()):
                #print(k)
                if k == self.my_url and self.my_player == None:
                    self.my_player = Player(k,v)
                else:
                    self.this_round_players.append(Player(k,v))
            
            self.all_players.append(self.this_round_players.copy())
            self.this_round_players.clear()
            count = count +1


    def am_I_scoring_positively(self):
        first_score = 0
        last_score = 0

        first = self.all_players[0]
        last = self.all_players[len(self.all_players)-1]
        for person in first:
            if person.url == self.my_url :
                first_score = person.score
        
        for person in last:
            if person.url == self.my_url :
                last_score = person.score

        if last_score > first_score :
            return True
        return False


    def am_I_winning(self):

        my_score = 0
        best_score = 0
        last = self.all_players[len(self.all_players)-1]
        
        for person in last:
            if person.url == self.my_url :
                my_score = person.score
            elif best_score < person.score:
                best_score = person.score

        if my_score >= best_score :
            return True
        return False

    def am_I_being_camped(self):

        #determine if someone is near me and firing
        camping_counter = {}
        for players in self.all_players:
            my_x = -1
            my_y = -1
            for player in players:
                if player.url == self.my_url :
                    my_x == player.x
                    my_y == player.y
            for player in players:
                if player.url != self.my_url :
                    res = abs(my_x-player.x+my_y-player.y)
                    if abs(my_x-player.x+my_y-player.y) == 1:
                        camping_counter[player.url] += 1
        
        for i, k in enumerate(camping_counter):
            if k >= camping_threshold-1 :
                print("camping : " + k)
                return True

        return False
       