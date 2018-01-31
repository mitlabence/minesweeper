import tkinter as tk
import numpy as np
import random
class Minesweeper(tk.Frame):
    chosen_size = 0
    difficulty_name = ""
    num_of_mines = 0
    first_click = True

    def __init__(self, master = None):
        grid_size = 0
        super().__init__(master)
        self.grid()
        self.mainMenu()

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
        top = tk.Toplevel()
        global chosen_size, difficulty_name, button_array
        top.title(difficulty_name)
        button_array = np.empty([chosen_size, chosen_size, 4],
                                dtype=object)  # 0 button; 1: is_mine, 2: not clicked / clicked / flagged (n/y/f), 3: neighbouring mines
        for x in range(chosen_size):
            for y in range(chosen_size):
                button_array[x][y] = [tk.Button(top, anchor = tk.NW, command = lambda x = x, y = y: self.firstClick(x,y)), False, "n", 0]
                button_array[x][y][0].grid(row = x+1, column = y+1, padx = 0, pady = 0)

    def otherClicks(self, x, y):
        global button_array
        button_array[x][y][0].config(relief=tk.SUNKEN, bg = "gray")
        button_array[x][y][2] = "y"
        if button_array[x][y][1]:
            button_array[x][y][0].config(bg = "red")
            return
        if button_array[x][y][3] == 0:
            self.showNeighbors(x,y)

    def firstClick(self, x, y):
        global button_array, num_of_mines
        self.PlaceMines(x, y)
        button_array[x][y][0].config(relief=tk.SUNKEN, bg="gray", text=str(button_array[x][y][3]))
        button_array[x][y][2] = "y"
        for k in range(chosen_size):        #changes firstClick methods to click
            for l in range(chosen_size):
                button_array[k][l][0].config(command = lambda x = k, y = l: self.otherClicks(x, y))
        button_array[x][y][0].config(text = button_array[x][y][3])
        if button_array[x][y][3] == 0:
            self.showNeighbors(x,y)

    def showNeighbors(self, x, y):
        for k in range(-1, 2):
            for l in range(-1, 2):
                if (x + k) >= 0 and (x + k) < chosen_size and (y + l) < chosen_size and (y + l) >= 0 and button_array[x + k][y + l][2] == "n":
                    button_array[x + k][y + l][0].config(relief = tk.SUNKEN, bg = "gray", text = str(button_array[x+k][y+l][3]))
                    button_array[x + k][y + l][2] = "y"
                    if button_array[x + k][y + l][3] == 0:
                        self.showNeighbors(x + k, y + l)

    def PlaceMines(self, x, y): #places mines on first click
        global button_array, num_of_mines
        i = 0
        while i < num_of_mines:
            x1 = random.randint(0, chosen_size - 1)
            y1 = random.randint(0, chosen_size - 1) #x, y coordinates of random mine placement
            if not(x == x1) and not(y == y1) and not(button_array[x1][y1][1]):
                button_array[x1][y1][1] = True
                button_array[x][y][2] = "y"
                for k in range(-1,2):
                    for l in range(-1,2):
                        if (x1+k)<chosen_size and (x1+k)>= 0 and (y1 + l) < chosen_size and (y1+l) >= 0:
                            button_array[x1+k][y1+l][3] += 1
                button_array[x1][y1][3] -= 1
                i += 1

    def smallSize(self):
        global chosen_size, difficulty_name, num_of_mines
        difficulty_name = "Small"
        chosen_size = 8
        num_of_mines = 10
        self.createGameGrid()

    def mediumSize(self):
        global chosen_size, difficulty_name, num_of_mines
        difficulty_name = "Medium"
        chosen_size = 12
        num_of_mines = 25
        self.createGameGrid()

    def largeSize(self):
        global chosen_size, difficulty_name, num_of_mines
        difficulty_name = "Large"
        chosen_size = 16
        num_of_mines = 40
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

root = tk.Tk()
app = Minesweeper(master=root)
app.mainloop()