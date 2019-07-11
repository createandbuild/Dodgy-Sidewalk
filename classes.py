class Player:
    def __init__(self, botX, botY):
        self.botX = botX
        self.botY = botY

class Pedestrian:
    def __init__(self, pedestrianList):
        self.pedestrianList = pedestrianList

class State:
    def __init__(self, bot, pedestrian):
        self.bot = bot
        self.pedestrian = pedestrian
