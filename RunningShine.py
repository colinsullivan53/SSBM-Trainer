import melee
import random

class RunningShine():
    """
    Fox dash dancing across the stage from you...
    Eating your lasers and evading your approaches...
    Waiting for the perfect opportunity...TO SHINE!!!
    """
    def __init__(self, dolphin, smashbot_port, opponent_port, controller):
        self.smashbot_port = smashbot_port
        self.opponent_port = opponent_port
        self.controller = controller
        self.console = dolphin
        self.framedata = melee.framedata.FrameData()

        self.dash = 0 #0 if dashed left, 1 if dashed right
        self.escape = 0

        self.runshine = 0
        self.shinelag = 0
        self.justshined = 0
        self.shinecount = 0

    def act(self, gamestate):

        def edge_check():
            if abs(gamestate.players[1].x) > (
                    melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 6.6):  # 3*fox dash speed
                self.dash = 0
                if gamestate.players[1].x < 0:
                    self.dash = 1
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, .5)
                self.escape = 1
                return

        onRight = gamestate.players[1].x > gamestate.players[2].x

        if self.escape > 0 and self.escape < 6:
            self.escape += 1
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
            return
        else:
            self.escape = 0

        if self.runshine > 0 and gamestate.distance > 5:
            edge_check()
            self.dash = int(not onRight)
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
            self.runshine += 1
            return
        elif gamestate.distance < 6:
            if self.shinecount > 2:
                self.controller.release_button(melee.Button.BUTTON_B)
                self.runshine = 0
            else:
                edge_check()
                self.runshine = -1
                self.shinelag = 1
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0)
                self.controller.press_button(melee.Button.BUTTON_B)
                self.shinecount += 1
                return
        elif self.runshine == -1:
            self.controller.release_button(melee.Button.BUTTON_B)
            self.runshine = 0

        if self.shinelag == 1:
            if gamestate.players[1].hitlag_left > 0 or gamestate.players[1].hitstun_frames_left > 0:
                self.controller.empty_input()
                return
            else:
                self.shinelag = 2
                self.controller.press_button(melee.Button.BUTTON_X)
        elif self.shinelag != 0 and self.shinelag < 4:
            self.shinelag += 1
            self.controller.empty_input()
            return
        elif self.shinelag >= 4:
            self.shinelag = -1
            if abs(gamestate.players[1].x) > (melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 10):
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, int(gamestate.players[1].x < 0), 0)
            else:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, int(not onRight), 0)
            self.controller.press_button(melee.Button.BUTTON_R)
            return
        elif self.shinelag == -1:
            self.controller.release_button(melee.Button.BUTTON_R)
            self.shinelag = 0


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



        if gamestate.players[1].action == melee.Action.TURNING:
            self.controller.empty_input()
            return


        edge_check()

        shine = random.randint(1,50)
        if gamestate.players[1].action == melee.Action.STANDING:
            if gamestate.distance > 70:
                self.dash = int(not onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            elif gamestate.distance <= 50:
                self.dash = int(onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
        elif gamestate.players[1].action == melee.Action.DASHING:
            if gamestate.distance > 22 and shine == 5:
                self.runshine = 1
                self.dash = int(not onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            elif gamestate.players[1].action_frame == dashframe:
                if self.dash == 0:
                    self.dash = 1
                else:
                    self.dash = 0
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            else:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return

