import os
import sys
import melee
import tkinter as tk
from tkinter import filedialog
from scenarios.RunningShine import RunningShine
from scenarios.PSMarth import PSMarth
from scenarios.LaserFalco import LaserFalco
from PIL import ImageTk

event_num = 0

window = tk.Tk()
path_frame = tk.Frame(window)

window.title("SSBM TRAINER v0.1")
window.geometry('500x410')

window.after(2000, None)

window.directory = filedialog.askdirectory()
dolphinPath = window.directory

file = filedialog.askopenfile(mode='r', filetypes=[('ISO', '*.iso')])
if file:
    meleePath = os.path.abspath(file.name)

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

def laserfalco():
    global event_num
    event_num = 3
    window.destroy()

header = ImageTk.PhotoImage(file = "./txt/header.png")
banner = tk.Label(image=header)
banner.pack()

photo = ImageTk.PhotoImage(file = "./txt/running_shine.png")
run_button = tk.Button(window, image=photo, command = runningshine)
run_button.pack()

photo2 = ImageTk.PhotoImage(file ="./txt/psmarth.png")
ps_button = tk.Button(window, image=photo2, command = psmarth)
ps_button.pack()

photo3 = ImageTk.PhotoImage(file ="./txt/falcolaser.png")
laser_button = tk.Button(window, image=photo3, command = laserfalco)
laser_button.pack()

tk.mainloop()



##################################################################################################################################
if event_num == 0:
    sys.exit()

agent1 = None

#console = melee.Console(path="C:/Users/forum/AppData/Roaming/Slippi Launcher/netplay")
console = melee.Console(path=dolphinPath)
controller = melee.Controller(console=console, port=1)
controller_human = melee.Controller(console=console, port=2,
                                    type=melee.ControllerType.GCN_ADAPTER)

#console.run("C:/Users/forum/Documents/roms/melee.iso")
console.run(meleePath)
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
elif event_num == 3:
    agent1 = LaserFalco(console, 1, 2, controller)
    character = melee.Character.FALCO
    stage = melee.Stage.POKEMON_STADIUM

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