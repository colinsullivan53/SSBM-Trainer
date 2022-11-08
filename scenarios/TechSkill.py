import melee
import random


class TechSkill():

    def wavedash(gamestate, controller, direction, js):
        if gamestate.players[1].action in [melee.Action.STANDING, melee.Action.DASHING, melee.Action.WALK_FAST,
                                           melee.Action.WALK_SLOW, melee.Action.TURNING_RUN, melee.Action.RUNNING,
                                           melee.Action.DOWN_B_GROUND_START, melee.Action.DOWN_B_GROUND]:
            controller.press_button(melee.Button.BUTTON_X)
            return
        elif gamestate.players[1].action == melee.Action.KNEE_BEND:
            if gamestate.players[1].action_frame == js - 1:
                controller.tilt_analog(melee.Button.BUTTON_MAIN, direction, 0.2)
                controller.press_button(melee.Button.BUTTON_R)
            return
        else:
            controller.release_all()
            return


    def face_opponent(gamestate, controller):
        # 1 means the bot is to the right of the player, 2 means the bot is to the left of the player
        onRight = gamestate.players[1].x > gamestate.players[2].x

        if onRight:
            if not gamestate.players[1].facing:
                return
            else:
                controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.25, 0.5)
                return
        else:
            if not gamestate.players[1].facing:
                controller.tilt_analog(melee.Button.BUTTON_MAIN, 0.75, 0.5)
                return
            else:
                return

    def power_sheild(gamestate, controller):
        if melee.ProjectileType.FALCO_LASER in gamestate.projectiles:
            controller.press_button(melee.Button.BUTTON_R)
        else:
            controller.release_button(melee.Button.BUTTON_R)
            return
