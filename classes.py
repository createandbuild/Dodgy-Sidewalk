class Bot:
    def __init__(self, botX, botY):
        self.botX = botX
        self.botY = botY

class Pedestrian:
    def __init__(self, pedestrianX, pedestrianY):
        self.pedestrianX = pedestrianX
        self.pedestrianY = pedestrianY

class State:
    def __init__(self, bot, pedestrian):
        self.bot = bot
        self.pedestrian = pedestrian
