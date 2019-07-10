from pygame.constants import K_DOWN, K_UP, KEYDOWN, KEYUP, QUIT
from mdp import PyGamePlayer


class PedestrianBot(PyGamePlayer):
    def __init__(self, force_game_fps=10, run_real_time=False):
        super(PedestrianBot, self).__init__(force_game_fps=force_game_fps, run_real_time=run_real_time)
        self.pedestrianCounter = 0

    def get_keys_pressed(self, screen_array, feedback, terminal):
        # TODO: put an actual learning agent here
        return [K_DOWN]

    def reward(self):
        # import must be done here because otherwise importing would cause the game to start playing
        from game import pedestrianCounter

        return pedestrianCounter, pedestrianCounter != 0

    def start(self):
        super(PedestrianBot, self).start()

        import game


if __name__ == '__main__':
    player = PedestrianBot()
    player.start()
