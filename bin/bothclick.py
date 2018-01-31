import tkinter
import time

class App:
    def __init__(self, root):
        self.root = root
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False

        f = tkinter.Frame(width=100, height=100, background="cyan")
        f.pack()

        f.bind("<Button-1>", self.onAnyofTwoPressed)
        f.bind("<Button-3>", self.onAnyofTwoPressed)

        f.bind("<ButtonRelease-1>", self.resetPressedState)
        f.bind("<ButtonRelease-3>", self.resetPressedState)

    def onAnyofTwoPressed(self, event):
        if self.left_mouse_pressed and self.left_mouse_pressed <= time.time():
            self.left_mouse_pressed = False

        if self.right_mouse_pressed and self.right_mouse_pressed <= time.time():
            self.right_mouse_pressed = False

        if event.num==1:
            self.left_mouse_pressed = time.time() + 500
        if event.num==3:
            self.right_mouse_pressed = time.time() + 500


    def resetPressedState(self, event):
        if self.left_mouse_pressed and self.right_mouse_pressed:
            print('both pressed')
        elif self.left_mouse_pressed:
            print('left pressed')
        elif self.right_mouse_pressed:
            print('rigth pressed')

        self.left_mouse_pressed = False
        self.right_mouse_pressed = False

root=tkinter.Tk()
app = App(root)
root.mainloop()