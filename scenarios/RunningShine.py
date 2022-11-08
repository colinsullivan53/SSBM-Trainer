import melee
import random
from scenarios.TechSkill import *

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

        self.danger = 0

        self.dash = 0 #0 if dashed left, 1 if dashed right
        self.escape = 0
        self.close_bound = 50
        self.far_bound = 70

        self.runshine = 0
        self.shinelag = 0

        self.wd_back = 0
        self.ledge_roll = 0


    def act(self, gamestate):

        # If not in current game, let go of controller
        if self.smashbot_port not in gamestate.players:
            self.controller.release_all()
            return

        def edge_check(): #If the play is too close to the edge, dash away from the edge
            if abs(gamestate.players[1].x) > (
                    melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 6.6):  # 3*fox dash speed
                self.dash = 0
                if gamestate.players[1].x < 0:
                    self.dash = 1
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, .5)
                self.escape = 1
                return

        def air_handler(): #If the play is not grounded, deal
            self.controller.empty_input()
            return

        def dashback():
            if self.dash == 0:
                self.dash = 1
            else:
                self.dash = 0
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
            return

        # 1 means the bot is to the right of the player, 2 means the bot is to the left of the player
        onRight = gamestate.players[1].x > gamestate.players[2].x

        # If in hitlag or hitstun, wait
        if gamestate.players[1].hitlag_left > 0 or gamestate.players[1].hitstun_frames_left > 0:
            self.controller.empty_input()
            return

        # If on angel platform, drop through
        if gamestate.players[1].action == melee.Action.ON_HALO_WAIT:
            self.controller.release_all()
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0)
            return


        if gamestate.players[1].action == melee.Action.EDGE_HANGING:
            self.controller.press_button(melee.Button.BUTTON_R)
            self.ledge_roll = 1
            return
        elif self.ledge_roll == 1:
            self.controller.release_button(melee.Button.BUTTON_R)

        # If not grounded, deal
        if not gamestate.players[1].on_ground:
            air_handler()
            return

        # If stuck in the corner, dash through for 5 frames
        if self.escape > 0 and self.escape < 6:
            self.escape += 1
            self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
            return
        else: # Else set escape variable to false
            self.escape = 0

        edge_check()

        # Do nothing if in turn (standing turn or dash turn around)
        if gamestate.players[1].action == melee.Action.TURNING:
            self.controller.empty_input()
            return

        # Wavedash Back
        # To call, set self.wd_back equal to 1, press jump, and loop back through
        if self.wd_back > 0 and self.wd_back < 5:
            self.wd_back += 1
            if abs(gamestate.players[1].x) > (melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 30):
                near_left_ledge = gamestate.players[1].x < 0
                TechSkill.wavedash(gamestate, self.controller, int(near_left_ledge), 3)
            else:
                TechSkill.wavedash(gamestate, self.controller, int(onRight), 3)
        elif self.wd_back > 4:
            self.wd_back = 0


        # Code for handling the running shine from a dash dance
        juke = random.randint(1,100)
        if self.runshine > 0 and gamestate.distance > 5:
            if juke >= 70 and gamestate.distance > 20:
                self.controller.press_button(melee.Button.BUTTON_X)
                self.wd_back = 1
                self.runshine = 0
                return
            else:
                self.dash = int(onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                self.runshine += 1
                return
        elif self.runshine == -1:
            self.controller.release_button(melee.Button.BUTTON_B)
            self.runshine = 0
        elif gamestate.distance < 6:
                self.runshine = -1
                self.shinelag = 1
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 0)
                self.controller.press_button(melee.Button.BUTTON_B)
                return

        # Code for after shine hit, wavedashes either away from the ledge or away from the opponent
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
            self.wd_back = 1
            return
        elif self.shinelag == -1:
            self.shinelag = 0


        if gamestate.players[1].action == melee.Action.TURNING_RUN:
            self.wd_back = 1
            self.controller.press_button(melee.Button.BUTTON_X)
            return

        # If in knockdown, roll randomly
        if gamestate.players[1].action in [melee.Action.LYING_GROUND_UP, melee.Action.LYING_GROUND_DOWN]:
            roll = random.randint(0, 3)
            if roll <= 1:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.5, 1)
                return
            elif roll == 2:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 1, 0.5)
                return
            else:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, 0, 0.5)
                return


        # Code for deciding dash dance lengths
        # If farther than 70 distance units, dash towards for 6 frames then away for two
        if gamestate.distance > self.far_bound:
            if onRight and gamestate.players[1].facing:
                dashframe = 2
            elif onRight and not gamestate.players[1].facing:
                dashframe = 6
            elif not onRight and gamestate.players[1].facing:
                dashframe = 6
            elif not onRight and not gamestate.players[1].facing:
                dashframe = 2
        # If closer than 50 distance units, dash away for 6 frames and towards for 2
        elif gamestate.distance <= self.close_bound:
            if onRight and gamestate.players[1].facing:
                dashframe = 6
            elif onRight and not gamestate.players[1].facing:
                dashframe = 2
            elif not onRight and gamestate.players[1].facing:
                dashframe = 2
            elif not onRight and not gamestate.players[1].facing:
                dashframe = 6
        # If in between 50 and 70 distance units, dash for 4 frames both ways
        else:
            dashframe = 4



        edge_check() # Check if too close to edge before we dash dance
        shine = random.randint(1,100) # probability of starting running shining (if possible) on this frame

        # Dash dance code for timing the dash backs and handing non-dashing action states
        # If standing
        if gamestate.players[1].action == melee.Action.STANDING:
            self.controller.release_all()
            # If we are farther than 70 distance units, dash towards
            if gamestate.distance > self.far_bound:
                self.dash = int(not onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            # If we are closer than 50 distance units, dash away
            elif gamestate.distance <= self.close_bound:
                self.dash = int(onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            # If we are in between 50 and 70 distance units, dash away
            else:
                self.dash = int(onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
        elif gamestate.players[1].action == melee.Action.DASHING:
            if gamestate.distance > 22 and shine > 86 and (abs(gamestate.players[2].x) >
                                                           ( melee.stages.EDGE_GROUND_POSITION[gamestate.stage] - 6.6)):
                self.runshine = 1
                self.dash = int(not onRight)
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return
            elif gamestate.players[1].action_frame == dashframe:
                dashback()
            elif gamestate.players[1].action == melee.Action.DASHING and gamestate.players[1].action_frame >= 8:
                dashback()
            else:
                self.controller.tilt_analog(melee.Button.BUTTON_MAIN, self.dash, 0.5)
                return

