#!/usr/bin/python3
import tkinter as tk

class graphBoard:
    def __init__(self, cvSize):
        if cvSize < 200 or cvSize > 800:
            raise ValueError("Wrong Canvas Size - %d" % (cvSize))
        self.cvSz = cvSize

    def click(self, event):
        x, y = event.x, event.y
        xy = '{:>4}, {:>4}'.format(x,y)
        self.rt.title(xy)
        print(xy)

    def run(self):
        self.rt = tk.Tk()
        self.rt.bind('<Motion>', self.click)
        self.rt.mainloop()

if __name__=='__main__':
    gb = graphBoard(400)
    gb.run()
