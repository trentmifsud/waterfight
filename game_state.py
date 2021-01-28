import datetime
import math
from google.cloud import firestore
import time
from player import Player
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




class Game_State(object):
    
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

    def __init__(self,me, other_players, dimensions, db):

        self.my_player == me
            #start new
        self.successive_hits = 0
        self.bossy_player = None
        self.my_player = me
        self.other_players = other_players
        self.dimensions = dimensions
        self.db = None

        if self.my_player.wasHit :
            self.successive_hits = successive_hits +1
        else :
            self.successive_hits = 0
        
        self.bossy_player =  other_players[0]

        for player in self.other_players : 
            if player.score >= self.bossy_player.score :
                self.bossy_player = player
        
        #keep track of recent scores
        #if len(self.recent_score_for_trends) <= self.recent_score_for_trends_size :
        #    self.recent_score_for_trends[recent_score_for_trends_index] = self.my_player.score
        
          
    # how am I doing?
    def am_I_scoring_positively():
        if (self.recent_score_for_trends[len(self.recent_score_for_trends)] >= self.recent_score_for_trends[0]):
            return True
        else :
            return False
    
    def am_I_unhurt():
        if(self.successive_hits > self.successive_hits_threshold):
            return True
        else:
            return False


    
    def am_I_near_bossy_player():
        if(self.bossy_player != None):
            eDistance = math.dist([self.my_player.X, self.my_player.Y], [self.bossy_player.X, self.bossy_player.Y]) 
            if(eDistance <= 1):
                return True
        return False

    def get_bossy_player():
        return self.bossy_player


    #  defend (run) or offensive (fire)
    def should_I_attack():
        if(self.am_I_winning() and self.am_I_unhurt()) : 
            return True
        if(self.am_I_unhurt() == False):
            return False
        if(self.am_I_winning() == False and self.am_I_unhurt() == True):
            return True
       

    def print_game_info():
        me = ' Hits : %s, BP : %s, Positive : %s' % (successive_hits, bossy_player, am_I_scoring_positively())
        print(me)
        me = ' Unhurt : %s, Near BP : %s, Attack : %s' % (am_I_unhurt, am_I_near_bossy_player, should_I_attack())
        print(me)