#!/usr/bin/python3
import tkinter as tk

class graphBoard:
    def __init__(self, cvSize):
        # Check the cvSize
        if cvSize < 200 or cvSize > 800:
            raise ValueError("Wrong Canvas Size - %d" % (cvSize))
        self.cvSz = cvSize

        # Create a canvas for drawing
        self.rt = tk.Tk()
        self.cv = tk.Canvas(self.rt, width = self.cvSz, height = self.cvSz, bg = 'white')
        self.cv.pack()

    def run(self):
        # Go into the main loop to capture mouse clicks
        self.rt.mainloop()

if __name__=='__main__':
    gb = graphBoard(400)
    gb.run()
