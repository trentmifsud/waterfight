import time
class Player:
    def __init__(self, url, details):
        self.url = url
        self.details = details
        self.x = details['x']
        self.y = details['y']
        self.direction = details['direction']
        self.wasHit = details['wasHit']
        self.score = details['score']
    def to_dict(self):
        # ...
        dictionary = {}
        myTimestamp = time.time()
        dictionary['createdAt'] = myTimestamp
        dictionary['x'] = self.x
        dictionary['y'] = self.y
        dictionary['direction'] = self.direction
        dictionary['wasHit'] = self.wasHit
        dictionary['score'] = self.score
        return dictionary