import os
import sys
import melee
import tkinter as tk
import pickle
from tkinter import filedialog
from scenarios.RunningShine import RunningShine
from scenarios.PSMarth import PSMarth
from scenarios.LaserFalco import LaserFalco
from PIL import ImageTk

event_num = 0
selected_melee = 0
selected_dolphin = 0
dolphinPath = ""
meleePath = ""

window = tk.Tk()
path_frame = tk.Frame(window)

window.title("SSBM TRAINER v0.1")
window.geometry('500x410')
window.after(2000, None)
def save_data():
    global data
    data = {"Dolphin": dolphinPath, "Melee": meleePath}
    with open('./txt/file.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def dolphin_path():
    window.directory = filedialog.askdirectory()
    global dolphinPath
    dolphinPath = window.directory

    global selected_dolphin
    global selected_melee
    selected_dolphin = 1
    if selected_melee == 1:
        path_frame.destroy()
        save_data()

def melee_path():
    file = filedialog.askopenfile(mode='r', filetypes=[('ISO', '*.iso')])
    if file:
        global meleePath
        meleePath = os.path.abspath(file.name)

        global selected_dolphin
        global selected_melee
        selected_melee = 1
        if selected_dolphin == 1:
            path_frame.destroy()
            save_data()

if os.path.isfile("./txt/file.pickle"):
    path_frame.destroy()
    selected_dolphin = 1
    selected_melee = 1
    with open('./txt/file.pickle', 'rb') as handle:
        data = pickle.load(handle)
        meleePath = data["Melee"]
        dolphinPath = data["Dolphin"]
else:
    dolphin_button = tk.Button(path_frame, text="Select Dolphin Path",command = dolphin_path)
    dolphin_button.pack()
    melee_button = tk.Button(path_frame, text="Select Melee Path", command = melee_path)
    melee_button.pack()
    path_frame.pack()

full_char_list = ["Dr.Mario","Mario","Luigi","Bowser","Peach","Yoshi","DK","C.Falcon","Ganondorf",
                  "Falco","Fox","Ness","Ice Climbers","Kirby","Samus","Zelda","Link","Y.Link",
                  "Pichu","Pikachu","Jiggly-Puff","Mewtwo","Mr.Game & Watch","Marth","Roy"]

def runningshine():
    global event_num
    event_num = 1
    if selected_melee == 1 and selected_dolphin == 1:
        window.destroy()
def psmarth():
    global event_num
    event_num = 2
    if selected_melee == 1 and selected_dolphin == 1:
       window.destroy()

def laserfalco():
    global event_num
    event_num = 3
    if selected_melee == 1 and selected_dolphin == 1:
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
