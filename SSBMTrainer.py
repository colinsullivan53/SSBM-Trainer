import sys

import melee
import tkinter as tk
from RunningShine import RunningShine
from PSMarth import PSMarth
from LaserFalco import LaserFalco
from PIL import ImageTk, Image

event_num = 0

window = tk.Tk()
stacking_frame = tk.Frame(window)
stacking_frame.pack()

window.title("SSBM TRAINER v0.1")
window.geometry('500x200')

full_char_list = ["Dr.Mario","Mario","Luigi","Bowser","Peach","Yoshi","DK","C.Falcon","Ganondorf",
                  "Falco","Fox","Ness","Ice Climbers","Kirby","Samus","Zelda","Link","Y.Link",
                  "Pichu","Pikachu","Jiggly-Puff","Mewtwo","Mr.Game & Watch","Marth","Roy"]

def runningshine():
    global event_num
    event_num = 1
    window.destroy()
def psmarth():
    global event_num
    event_num = 2
    window.destroy()

header = ImageTk.PhotoImage(file = "./header.png")
banner = tk.Label(image=header)
banner.pack()

photo = ImageTk.PhotoImage(file = "./running_shine.png")
run_button = tk.Button(window, image=photo, command = runningshine)
run_button.pack()

photo2 = ImageTk.PhotoImage(file ="./psmarth.png")
ps_button = tk.Button(window, image=photo2, command = psmarth)
#ps_button.pack()


tk.mainloop()



##################################################################################################################################
if event_num == 0:
    sys.exit()

agent1 = None

console = melee.Console(path="C:/Users/forum/AppData/Roaming/Slippi Launcher/netplay")
controller = melee.Controller(console=console, port=1)
controller_human = melee.Controller(console=console, port=2,
                                    type=melee.ControllerType.GCN_ADAPTER)

console.run("C:/Users/forum/Documents/roms/melee.iso")
console.connect()

controller.connect()
controller_human.connect()

if event_num == 1:
    agent1 = RunningShine(console, 1, 2, controller)
    character = melee.Character.FOX
    stage = melee.Stage.FINAL_DESTINATION
elif event_num == 2:
    agent1 = PSMarth(console, 1, 2, controller)
    character = melee.Character.MARTH
    stage = melee.Stage.FINAL_DESTINATION

while True:
    gamestate = console.step()
    controller.release_all()
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        agent1.act(gamestate)
        controller.flush()
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            character,
                                            stage,
                                            "",
                                            autostart=True,
                                            swag=True)