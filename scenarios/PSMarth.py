import melee
from random import *
from scenarios.TechSkill import *

class PSMarth():
    """

    """
    def __init__(self, dolphin, smashbot_port, opponent_port, controller):
        self.smashbot_port = smashbot_port
        self.opponent_port = opponent_port
        self.controller = controller

        self.ledge_roll = 0
        self.just_rolled = 0

        self.RUNNNNN = 0


    def act(self, gamestate):

        if self.smashbot_port not in gamestate.players:
            self.controller.release_all()
            return

        if gamestate.players[1].action == melee.Action.EDGE_HANGING:
            self.controller.press_button(melee.Button.BUTTON_R)
            self.ledge_roll = 1
            return
        elif self.ledge_roll == 1:
            self.controller.release_button(melee.Button.BUTTON_R)

        if self.RUNNNNN == 1:
            if abs(gamestate.players[1].x) > melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 15:
                onRight = gamestate.players[1].x > gamestate.players[2].x
                left_side = gamestate.players[1].x < 0
                if left_side and not onRight:
                    self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 1, 0.5)
                elif not left_side and onRight:
                    self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0, 0.5)
                else:
                    self.RUNNNNN = 0
                return
            return


        if abs(gamestate.players[1].x) > melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 15:
            self.RUNNNNN = 1
            if gamestate.players[1].x < 0:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 1, 0.5)
            else:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0, 0.5)
            return


        # 1 means the bot is to the right of the player, 2 means the bot is to the left of the player
        onRight = gamestate.players[1].x > gamestate.players[2].x
        if gamestate.distance > 95:
            #TechSkill.wavedash(gamestate, self.controller, int(not onRight), 4)
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, int(not onRight), 0.5)
            return
        elif gamestate.distance < 65:
            TechSkill.wavedash(gamestate, self.controller, int(onRight), 4)
            return
        else:
            TechSkill.power_sheild(gamestate, self.controller)
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0)
            return


        TechSkill.face_opponent(gamestate, self.controller)