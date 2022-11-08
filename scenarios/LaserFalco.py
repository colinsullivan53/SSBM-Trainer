import melee
from random import *

class LaserFalco():
    """

    """
    def __init__(self, dolphin, smashbot_port, opponent_port, controller):
        self.smashbot_port = smashbot_port
        self.opponent_port = opponent_port
        self.controller = controller
        self.framedata = melee.framedata.FrameData()
        self.laser_height = 0

    def act(self, gamestate):

        if self.smashbot_port not in gamestate.players:
            self.controller.release_all()
            return

