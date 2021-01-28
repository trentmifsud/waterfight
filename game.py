import time
import numpy
from scipy import spatial
import math
import logging
import os
from player import Player
from  game_state import Game_State
from game_intelligence import Game_Intelligence

moves = ['F', 'T', 'L', 'R']
default_move = moves[1]

class Game:

    def __init__(self, game_data, db):
        
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
        self.logger = logging.getLogger(__name__)
        self.db = db

        self.links = game_data["_links"]
        self.my_url = self.links['self']['href']
        self.arena = game_data["arena"]
        
        self.dimensions = self.arena['dims']
        self.state = self.arena['state'] 
        # get past 10 records.

        self.historic_state = db.get_data_firestore()
        self.game_intelligence = Game_Intelligence(self.historic_state)

        postiive = ('Am I scoring positively : %s ' % self.game_intelligence.am_I_scoring_positively())
        winning = ('Am I winning %s : ' % self.game_intelligence.am_I_winning())
        camped = ('Am I being camped %s : ' % self.game_intelligence.am_I_being_camped())
        self.logger.info(postiive  + ' ' + winning + ' ' + camped)

        
        self.players = []
        for i, (k, v) in enumerate(self.state.items()):
            #print(k)
            if k == self.my_url :
                self.my_player = Player(k,v)
            else:
                self.players.append(Player(k,v))
        
        self.game_state = Game_State(self.my_player, self.players, self.dimensions, self.db)
        

    def get_dims(self):
        return  dimensions

    def get_next_move(self):
        #for each play - in this case it is represented as a link
        #my_player = self.players[self.my_url]
        x = []
        y = []
        coordinates = []

        for player in self.players:
            if player.wasHit is False : # if they are hit, don't hit again
                x.append(player.x)
                y.append(player.y)
                coordinates.append((player.x,player.y))

        my_location = [(self.my_player.x,self.my_player.y)]
        
        distance, closest_player_location = find_index_of_nearest_co(coordinates,my_location)
        #cardinal_dir, degree = direction_lookup(closest_player_location[0], self.my_player.x, closest_player_location[1], self.my_player.y)
        cardinal_dir, degree = direction_lookup(self.my_player.x, closest_player_location[0], self.my_player.y, closest_player_location[1])
        
        cp_x = str(closest_player_location[0])
        cp_y = str(closest_player_location[1])
        #cp = 'closest neighbour : %s,%s' % (cp_x,cp_y)

        #self.logger.debug(cp)
        me = ' ME : %s, XY : %s%s, ' % (self.my_player.direction , self.my_player.x, self.my_player.y)
        more = ' Them : dist %s, %s, CN_XY : %s%s, deg : %s' % (distance, cardinal_dir, cp_x,cp_y, degree)

        self.logger.info(me  + more)


        return_val =  check_valid_return_value(self,'F') 
        if distance <= 3 and self.my_player.direction == cardinal_dir :
            self.logger.info('throwing because distance is one and I am facing opponent')
            return_val = 'T'
        elif distance >4 and self.my_player.direction == cardinal_dir : 
            #facing correct way, just move towards them
            self.logger.info('moving towards opponent because I am facing them')
            return_val =  check_valid_return_value(self,'F') 
        elif self.my_player.direction != cardinal_dir :
            #rotate towards player using cardinal_dir
            self.logger.info('rotating towards opponent as I am not facing them')
            if degree == 90 or degree == 360 or degree == 0:
                return_val =  'R'
            elif degree == 180:
                return_val =  'R'  #we need to turn
            elif degree >= 270:
                return_val =  'L'
            else:
                return_val = default_move

        self.logger.info('I will return %s', return_val)
        return return_val

def check_valid_return_value(self, return_val):
    
    if return_val != 'F' :
        return return_val
    
    if self.my_player.direction == 'N' :
        new_y = self.my_player.y - 1
        if new_y <= 0:
            # rotate - DO not go forward
            return_val = 'R'
    elif self.my_player.direction == 'W' :
        new_x = self.my_player.x - 1
        if new_x <= 0:
            # rotate - DO not go forward
            return_val = 'R'
    elif self.my_player.direction == 'S' :
        new_y = self.my_player.y + 1
        if new_y >= Arena.dimensions[1]:
            # rotate - DO not go forward
            return_val = 'R'
    elif self.my_player.direction == 'E' :
        new_x = self.my_player.x + 1
        if new_x >= Arena.dimensions[0]:
            # rotate - DO not go forward
            return_val = 'R'

    #self.logger.info('X %s ,Y %s, dir %s, Arena %s', self.my_player.x, self.my_player.y, return_val, Arena.dimensions)
    
    return return_val

def find_index_of_nearest_co(coordinates, my_location):
    distance,index = spatial.KDTree(coordinates).query(my_location)
    return distance.item(0), coordinates[index.item(0)]

def direction_lookup(origin_x, destination_x, origin_y, destination_y ):

    deltaX = destination_x - origin_x
    deltaY = destination_y - origin_y
    degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180

    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:

        degrees_final = degrees_temp
    compass_brackets = ["N", "E", "S", "W", "N"]
    compass_lookup = round(degrees_final / 90)
    rounded_degrees = round(degrees_final / 90) * 90
    #print(compass_brackets[compass_lookup])
    #print(rounded_degrees)
    return compass_brackets[compass_lookup], rounded_degrees

