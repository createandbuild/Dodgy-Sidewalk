from pygame.constants import K_DOWN, K_UP, KEYDOWN, KEYUP, QUIT
from mdp import gameBot


class PedestrianBot(gameBot):
    def __init__(self, force_game_fps=10, run_real_time=False):
        super(PedestrianBot, self).__init__(force_game_fps=force_game_fps, run_real_time=run_real_time)
        self.pedestrianCounter = 0

    def get_keys_pressed(self, screen_array, reward, terminal):
        if reward != 0:
            self.pedestrianCounter += reward

    def reward(self):
        # import must be done here because otherwise importing would cause the game to start playing
        from game import pedestrianCounter

        return pedestrianCounter, pedestrianCounter != 0

    def start(self):
        from game import main

        main()


if __name__ == '__main__':
    player = PedestrianBot()
    player.start()
