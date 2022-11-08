import melee
from random import *

class PSMarth():
    """

    """
    def __init__(self, dolphin, smashbot_port, opponent_port, controller):
        self.smashbot_port = smashbot_port
        self.opponent_port = opponent_port
        self.controller = controller
        self.framedata = melee.framedata.FrameData()
        self.laser_frame = 0;

    def act(self, gamestate):

        if self.smashbot_port not in gamestate.players:
            self.controller.release_all()
            return

        if (gamestate.distance > 35):
            side = gamestate.players[1].x > gamestate.players[2].x #False is bot on left of player, true is bot to the right of player
            if side:
                if gamestate.players[1].facing:
                    self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.25, 0.5)
                    self.controller.release_all()
                else:
                    self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0)
                    return
            else:
                if gamestate.players[1].facing:
                    self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0)
                    return
                else:
                    self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.75, 0.5)
                    self.controller.release_all()