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

        self.laser = 0
        self.laser_height = [0, 1, 1, 3, 0, 1, 3, 0, 2, 2, 3, 3, 1, 3, 1, 3, 0, 2]
        self.laser_count = 0
        self.laser_length = 18

        self.dash = 0  # 0 if dashed left, 1 if dashed right
        self.escape = 0
        self.pivot = 0

    def act(self, gamestate):

        height = randint(0, 17)
        def edge_check():
            if abs(gamestate.players[1].x) > (
                    melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 11):  # 3*fox dash speed
                self.dash = 0
                if gamestate.players[1].x < 0:
                    self.dash = 1
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, .5)
                self.escape = 1
                return

        onRight = gamestate.players[1].x > gamestate.players[2].x

        if gamestate.players[1].hitlag_left > 0 or gamestate.players[1].hitstun_frames_left > 0:
            self.controller.empty_input()
            return

        if self.smashbot_port not in gamestate.players:
            self.controller.release_all()
            return

        if self.escape > 0 and self.escape < 7:
            self.escape += 1
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
            return
        else:
            self.escape = 0

        edge_check()

        if self.laser > 0 and self.laser < 6:
            self.laser += 1
            return
        elif self.laser == 6:
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, int(not onRight), 0.5)
            self.laser += 1
            return
        elif self.laser == 7:
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0.5)
            self.laser += 1
            return
        elif self.laser >= 8:
            self.controller.press_button(melee.Button.BUTTON_B)
            self.laser += 1
            return
        elif self.laser >= 9:
            self.controller.release_button(melee.Button.BUTTON_B)
            if gamestate.players[1].action_frame > 1 and not gamestate.players[1].on_ground:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, int(not onRight), 0.5)
                self.laser = 0
            else:
                self.laser += 1
            return

        if gamestate.distance > 70:
            if onRight and gamestate.players[1].facing:
                dashframe = 3
            elif onRight and not gamestate.players[1].facing:
                dashframe = 6
            elif not onRight and gamestate.players[1].facing:
                dashframe = 6
            elif not onRight and not gamestate.players[1].facing:
                dashframe = 3
        elif gamestate.distance <= 50:
            if onRight and gamestate.players[1].facing:
                dashframe = 6
            elif onRight and not gamestate.players[1].facing:
                dashframe = 3
            elif not onRight and gamestate.players[1].facing:
                dashframe = 3
            elif not onRight and not gamestate.players[1].facing:
                dashframe = 6
        else:
            dashframe = 4

        las = randint(1,100)

        if gamestate.players[1].action == melee.Action.STANDING:
            if gamestate.distance > 60 and las >= 50:
                self.controller.press_button(melee.Button.BUTTON_X)
                self.laser = 1
                return
            elif gamestate.distance <= 60:
                self.dash = int(onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
        elif gamestate.players[1].action == melee.Action.DASHING:
            if gamestate.players[1].action_frame == dashframe:
                if self.dash == 0:
                    self.dash = 1
                else:
                    self.dash = 0
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            else:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return

