import melee
import random
from melee.enums import Action, Button, Character

class TechSkill():

    neutral = [Action.STANDING, Action.DASHING, Action.TURNING, \
               Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
    edge = [Action.EDGE_HANGING, Action.EDGE_CATCHING, Action.EDGE_GETUP_SLOW, \
            Action.EDGE_GETUP_QUICK, Action.EDGE_ATTACK_SLOW, Action.EDGE_ATTACK_QUICK, Action.EDGE_ROLL_SLOW,
            Action.EDGE_ROLL_QUICK]
    onEdge = [Action.EDGE_HANGING, Action.EDGE_CATCHING]

    def jump_cancel_frames(gamestate):
        """
        returns number of frames (int) when the character should be pressing another input to jump cancel (This was found by taking their jumpsquat animation and
        subtracting 2, for some reason I found that this always worked better)
        This is easily modifyable if someone finds that this number does not work for them as it did for me
        """
        if gamestate.players[0].character == Character.FOX or gamestate.players[0].character == Character.POPO or gamestate.players[0].character == Character.KIRBY or \
                gamestate.players[0].character == Character.SAMUS or gamestate.players[0].character == Character.SHEIK or gamestate.players[0].character == Character.PICHU or \
                gamestate.players[0].character == Character.PICHU:
            return 1
        elif gamestate.players[0].character == Character.DOC or gamestate.players[0].character == Character.MARIO or gamestate.players[0].character == Character.LUIGI or \
                gamestate.players[0].character == Character.CPTFALCON or gamestate.players[0].character == Character.YLINK or gamestate.players[0].character == Character.NESS or \
                gamestate.players[0].character == Character.MARTH or gamestate.players[0].character == Character.GAMEANDWATCH:
            return 2
        elif gamestate.players[0].character == Character.FALCO or gamestate.players[0].character == Character.PEACH or gamestate.players[0].character == Character.YOSHI or \
                gamestate.players[0].character == Character.DK or gamestate.players[0].character == Character.JIGGLYPUFF or gamestate.players[0].character == Character.MEWTWO or \
                gamestate.players[0].character == Character.ROY:
            return 3
        elif gamestate.players[0].character == Character.GANONDORF or gamestate.players[0].character == Character.ZELDA or gamestate.players[0].character == Character.LINK:
            return 4
        elif gamestate.players[0].character == Character.BOWSER:
            return 6

    def wavedash(gamestate, controller, direction, js):
        if gamestate.players[1].action in [melee.Action.STANDING, melee.Action.DASHING, melee.Action.WALK_FAST,
                                           melee.Action.WALK_SLOW, melee.Action.TURNING_RUN, melee.Action.RUNNING,
                                           melee.Action.DOWN_B_GROUND_START, melee.Action.DOWN_B_GROUND,
                                           melee.Action.CROUCHING, melee.Action.CROUCH_END, melee.Action.CROUCH_START]:
            controller.press_button(melee.Button.BUTTON_X)
            return
        elif gamestate.players[1].action == melee.Action.KNEE_BEND:
            if gamestate.players[1].action_frame == js:
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


    def defend(gamestate, controller):
        blocking = [Action.SHIELD_STUN, Action.SPOTDODGE, Action.SHIELD_REFLECT, Action.SHIELD]
        # If we blocked, stop blocking
        if gamestate.players[0].action in blocking:
            controller.release_button(Button.BUTTON_L)
            controller.tilt_analog(Button.BUTTON_MAIN, .5, .5)
            return
        hitframe = melee.framedata.FrameData.in_range(gamestate.players[1], gamestate.players[0], gamestate.stage)
        framesTillHit = hitframe - gamestate.players[1].action_frame
        # SpotDodge
        if melee.framedata.FrameData.is_grab(gamestate.players[1].character, gamestate.players[1].action):
            # Can they grab us tho?
            if framesTillHit > 3:
                controller.press_button(Button.BUTTON_L)
                controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
                return
        if framesTillHit < 5:
            controller.press_button(Button.BUTTON_L)
            return

    def power_sheild(gamestate, controller):
        if gamestate.players[1].action not in [melee.Action.STANDING, melee.Action.DASHING, melee.Action.CROUCHING]:
            return
        for proj in gamestate.projectiles:
            if abs(proj.position.x - gamestate.players[1].x) <= 4:
                controller.press_button(melee.Button.BUTTON_R)
            else:
                controller.release_button(melee.Button.BUTTON_R)
        return
