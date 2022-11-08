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

        self.wd = 0

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

        # 1 means the bot is to the right of the player, 2 means the bot is to the left of the player
        onRight = gamestate.players[1].x > gamestate.players[2].x
        if gamestate.distance > 75:
            TeckSkill.wavedash(gamestate, self.controller, int(not onRight), 4)
        else:
            if abs(gamestate.players[1].x) > (melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 40):
                near_left_ledge = gamestate.players[1].x < 0
                TeckSkill.wavedash(gamestate, self.controller, int(near_left_ledge), 4)
            else:
                TeckSkill.wavedash(gamestate, self.controller, int(onRight), 4)


        TeckSkill.face_opponent(gamestate, self.controller)
