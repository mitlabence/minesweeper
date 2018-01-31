import tkinter as tk
from tkinter import messagebox
import numpy as np
import random, time

#https://stackoverflow.com/questions/24469090/detect-simultaneous-left-and-right-clicks-in-python-gui
#http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
#protocol handler
#known bugs:
#           *Both buttons pressed: when enough flags around, but at least one is in the wrong place, the mine does not get uncovered.
#           *Both buttons pressed: works on flagged tiles too.
#           *Sometimes more "you win" windows appear (4)
#To-do:
#           *Read how both buttons pressed should work (on flagged, on unknown, on known tiles)
#           *Debug multiple win/loss screens appearing; idea: insert a global boolean game_over, if it is true, it breaks considerneighbors loop etc.
#
class Minesweeper(tk.Frame):
    colour_name = {"": "gray", "1": "blue", "2": "sea green", "3": "red", "4": "dark orchid", "5": "firebrick",
                   "6": "cadet blue", "7": "black", "8": "saddle brown"}
    chosen_size = 0
    difficulty_name = ""
    num_of_mines = 0
    first_click = True
    tiles_left = 0
    button_array = []
    active_game = False

    def __init__(self, master = None):
        super().__init__(master)
        self.grid()
        self.mainMenu()
        self.lmb_pressed = False
        self.rmb_pressed = False
    def mainMenu(self):
        #new game button
        self.new_game = tk.Button(self, text = "New Game", command = self.newGame, width = 10)
        self.new_game.grid(row = 1,column = 1)

        #settings button
        self.settings = tk.Button(self, text = "Settings", command = self.settingsButton, width = 10)
        self.settings.grid(row = 2,column = 1)

        #quit button
        self.quit = tk.Button(self, text = "Quit", command = root.destroy, width = 10)
        self.quit.grid(row = 3,column = 1)

    def clearMainMenu(self):
        self.new_game.grid_remove()
        self.settings.grid_remove()
        self.quit.grid_remove()

    def newGameMenu(self):
        self.difficulty = tk.Label(self, text="Difficulty", width = 10)
        self.difficulty.grid(row = 1, column = 1)

        self.small = tk.Button(self, text = "Small", command = lambda: self.smallSize(), width = 10)
        self.small.grid(row = 2, column = 1)

        self.medium = tk.Button(self, text = "Medium", command = lambda: self.mediumSize(), width = 10)
        self.medium.grid(row = 3, column = 1)

        self.large = tk.Button(self, text = "Large", command = lambda: self.largeSize(), width = 10)
        self.large.grid(row = 4, column = 1)

        self.back_to_main = tk.Button(self, text = "Back", command = lambda : self.newGameBackToMain(), width = 10)
        self.back_to_main.grid(row = 5, column = 1)

    def createGameGrid(self):
        self.active_game = True
        top = tk.Toplevel()
        top.title(self.difficulty_name)

        def onClosingGameWindow():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.active_game = False
                top.destroy()

        top.protocol("WM_DELETE_WINDOW", onClosingGameWindow)
        self.button_array = np.empty([self.chosen_size, self.chosen_size, 4],
                                dtype = object)  # 0 button; 1: is_mine, 2: not clicked / clicked / flagged (n/y/f), 3: neighbouring mines
        for x in range(self.chosen_size):
            for y in range(self.chosen_size):
                self.button_array[x][y] = [tk.Button(top, anchor = tk.NW, relief=tk.SUNKEN, width = 2, height = 2), False, "n", ""]
                self.button_array[x][y][0].bind('<Button-1>', lambda event, k = x, l = y: self.firstClick(event, k, l, top))
                self.button_array[x][y][0].grid(row = x+1, column = y+1)

    def otherClicks(self, event, x, y, parent):
        if self.lmb_pressed and self.lmb_pressed <= time.time():
            self.lmb_pressed = False

        if self.rmb_pressed and self.rmb_pressed <= time.time():
            self.rmb_pressed = False
        if event.num==1:
            self.lmb_pressed = time.time() + 500
        if event.num==3:
            self.rmb_pressed = time.time() + 500

    def leftOrRightPressed(self, event):
        if self.lmb_pressed and self.lmb_pressed <= time.time():
            self.lmb_pressed = False
        if self.rmb_pressed and self.rmb_pressed <= time.time():
            self.rmb_pressed = False
        if event.num == 1:
            self.lmb_pressed = time.time() + 500
        if event.num == 3:
            self.rmb_pressed = time.time() + 500

    def bothButtonsPressed(self, x, y, parent):
        #Check if clicked-on tile has enough flags around it
        num_of_flags = 0
        for k in range(-1, 2):
            for l in range(-1, 2):
                if (x + k) >= 0 and (x + k) < self.chosen_size and (y + l) < self.chosen_size and (y + l) >= 0 and self.button_array[x + k][y + l][2] == "f":
                    num_of_flags += 1
        if self.button_array[x][y][2] == "f":
            num_of_flags -= 1
        if num_of_flags >= int(self.button_array[x][y][3]) and not(self.button_array[x][y][2] == "f"):
            self.revealNeighbors(x, y, parent)


    def buttonRelease(self, event, x, y, parent):
        if self.lmb_pressed and self.rmb_pressed:
            self.bothButtonsPressed(x, y, parent)
        elif self.lmb_pressed:
            if self.button_array[x][y][2] == "n":
                if self.button_array[x][y][1]:  # mine
                    self.showAll()
                    self.lostGame(parent)
                    return
                    """
                    self.button_array[x][y][0].config(bg="red")
                    self.button_array[x][y][2] = "y"
                    self.button_array[x][y][0].config(bg="red")
                    return
                    """
                self.buttonPressAnimation(x, y, parent)
                if self.button_array[x][y][3] == "":
                    self.considerNeighbors(x, y, parent)
        elif self.rmb_pressed:
            if self.button_array[x][y][2] == "n":
                self.button_array[x][y][0].config(bg="blue")
                self.button_array[x][y][2] = "f"
            elif self.button_array[x][y][2] == "f":
                self.button_array[x][y][0].config(bg="gainsboro")
                self.button_array[x][y][2] = "n"
        self.lmb_pressed = False
        self.rmb_pressed = False

    def buttonPressAnimation(self, x, y, parent):
        if self.button_array[x][y][2] == "n" and not(self.button_array[x][y][1]):
            #print(self.tiles_left)
            self.tiles_left -= 1
            self.button_array[x][y][0].config(bg="gray", text = self.button_array[x][y][3],
                                              fg = self.colour_name[self.button_array[x][y][3]])
            self.button_array[x][y][2] = "y"
        elif self.button_array[x][y][2] == "n" and self.button_array[x][y][1]:
            self.showAll()
            self.lostGame(parent)
            return
        #    self.button_array[x][y][0].config(bg="red")
        #    self.button_array[x][y][2] = "y"
        #    self.button_array[x][y][0].config(bg="red")
        if self.tiles_left == 0:
            self.winGame(parent)
            return

    def firstClick(self, event, x, y, parent):
        self.placeMines(x, y)
        self.tiles_left -= 1
        self.button_array[x][y][0].config(bg="gray")
        self.buttonPressAnimation(x, y, parent)
        for k in range(self.chosen_size):        #changes firstClick methods to click
            for l in range(self.chosen_size):
                self.button_array[k][l][0].bind('<Button-1>', lambda event, k = k, l = l: self.otherClicks(event, k, l, parent))
                self.button_array[k][l][0].bind('<Button-3>', lambda event, x = k, y = l: self.otherClicks(event, x, y, parent))
                self.button_array[k][l][0].bind('<ButtonRelease-1>', lambda event, k = k, l = l: self.buttonRelease(event, k, l, parent))
                self.button_array[k][l][0].bind('<ButtonRelease-3>', lambda event, k = k, l = l: self.buttonRelease(event, k, l, parent))
        self.button_array[x][y][0].config(text = self.button_array[x][y][3], fg = self.colour_name[self.button_array[x][y][3]])
        if self.button_array[x][y][3] == "":
            self.considerNeighbors(x, y, parent)

    def showNumbers(self):
        for k in range(0, self.chosen_size):
            for l in range(0, self.chosen_size):
                if self.button_array[k][l][1]:
                    self.button_array[k][l][0].config(bg = "red")
                else:
                    self.button_array[k][l][0].config(text = self.button_array[k][l][3])

    def considerNeighbors(self, x, y, parent):
        for k in range(-1, 2):
            for l in range(-1, 2):
                if (x + k) >= 0 and (x + k) < self.chosen_size and (y + l) < self.chosen_size and (y + l) >= 0 and self.button_array[x + k][y + l][2] == "n" and not(self.button_array[x+k][y+l][1]):
                    self.buttonPressAnimation(x + k, y + l, parent)
                    if self.button_array[x + k][y + l][3] == "":
                        self.considerNeighbors(x + k, y + l, parent)

    def revealNeighbors(self, x, y, parent):
        for k in range(-1, 2):
            for l in range(-1, 2):
                if (x + k) >= 0 and (x + k) < self.chosen_size and (y + l) < self.chosen_size and (y + l) >= 0 and self.button_array[x + k][y + l][2] != "f":
                    self.buttonPressAnimation(x + k, y + l, parent)
                    if self.button_array[x + k][y + l][3] == "":
                        self.considerNeighbors(x + k, y + l, parent)

    def convertToInt(self, x):
        if x == "":
            return 0
        else:
            return int(x)

    def placeMines(self, x, y): #places mines on first click
        i = 0
        while i < self.num_of_mines:
            x1 = random.randint(0, self.chosen_size - 1)
            y1 = random.randint(0, self.chosen_size - 1) #x, y coordinates of random mine placement
            if not(x == x1) and not(y == y1) and not(self.button_array[x1][y1][1]):
                self.button_array[x1][y1][1] = True
                self.button_array[x][y][2] = "y"
                for k in range(-1,2):
                    for l in range(-1,2):
                        if (x1+k)< self.chosen_size and (x1+k)>= 0 and (y1 + l) < self.chosen_size and (y1+l) >= 0:
                            self.button_array[x1+k][y1+l][3] = str(1 + self.convertToInt(self.button_array[x1+k][y1+l][3]))
                self.button_array[x1][y1][3] = str(self.convertToInt(self.button_array[x1][y1][3]) - 1)
                i += 1

    def smallSize(self):
        if not(self.active_game):
            self.tiles_left = 54
            self.difficulty_name = "Small"
            self.chosen_size = 8
            self.num_of_mines = 10
            self.createGameGrid()

    def mediumSize(self):
        if not(self.active_game):
            self.tiles_left = 119
            self.difficulty_name = "Medium"
            self.chosen_size = 12
            self.num_of_mines = 25
            self.createGameGrid()

    def largeSize(self):
        if not(self.active_game):
            self.tiles_left = 216
            self.difficulty_name = "Large"
            self.chosen_size = 16
            self.num_of_mines = 40
            self.createGameGrid()

    def clearNewGameMenu(self):
        self.difficulty.grid_remove()
        self.small.grid_remove()
        self.medium.grid_remove()
        self.large.grid_remove()
        self.back_to_main.grid_remove()

    def settingsMenu(self):
        self.back_button = tk.Button(self, text = "Back", command = lambda: self.settingsBackToMain(), width = 10)
        self.back_button.grid(row = 1, column = 1)

    def settingsBackToMain(self):
        self.clearSettingsMenu()
        self.mainMenu()

    def newGameBackToMain(self):
        self.clearNewGameMenu()
        self.mainMenu()

    def newGame(self):
        self.clearMainMenu()
        self.newGameMenu()

    def clearSettingsMenu(self):
        self.back_button.grid_remove()

    def settingsButton(self):
        self.clearMainMenu()
        self.settingsMenu()

    def showAll(self):
        for k in range(self.chosen_size):
            for l in range(self.chosen_size):
                if self.button_array[k][l][1]:
                    self.button_array[k][l][0].config(bg = "red")
                elif self.button_array[k][l][3] == "":
                    self.button_array[k][l][0].config(text = "")
                else:
                    self.button_array[k][l][0].config(text = self.convertToInt(self.button_array[k][l][3]), fg = self.colour_name[self.button_array[k][l][3]])

    def lostGame(self, parent):
        self. active_game = False
        lostWindow = tk.Toplevel(parent)
        lostWindow.minsize(width = 240, height = 320)
        lostWindow.title("You lost.")
        self.lost_label = tk.Label(lostWindow, text="you lost", width = 10)
        self.lost_button = tk.Button(lostWindow,text="Return to Main Menu", command = lambda: self.returnToMain(lostWindow, parent))
        self.lost_label.pack()
        self.lost_button.pack()

    def returnToMain(self, w, q):
        w.destroy()
        q.destroy()

    def winGame(self, parent):
        self.active_game = False
        winWindow = tk.Toplevel(parent)
        winWindow.title("You win.")
        winWindow.minsize(width = 240, height = 320)
        self.win_label = tk.Label(winWindow, text="you win", width = 10)
        self.win_button = tk.Button(winWindow, text="Return to Main Menu",
                                     command=lambda: self.returnToMain(winWindow, parent))
        self.win_label.grid(row = 0, column = 0)




root = tk.Tk()
app = Minesweeper(master=root)
app.mainloop()