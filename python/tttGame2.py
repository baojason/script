#!/usr/bin/python3
import tkinter as tk

class rectData:
    def __init__(self, cv, tag, pt1, pt2, color='lightgrey'):
        self.tag = tag
        self.pt1 = pt1
        self.pt2 = pt2
        self.color = color
        cv.create_rectangle(self.pt1[0], self.pt1[1], self.pt2[0], self.pt2[1],
                fill = self.color, tag = self.tag, outline = '')

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

        # Draw a rectangle shape
        offset = 20
        x1 = offset
        y1 = offset
        x2 = self.cvSz - x1
        y2 = self.cvSz - y1
        self.bgcv = rectData(self.cv, 'myBackgroud', (x1,y1), (x2,y2))

    def run(self):
        # Go into the main loop to capture mouse clicks
        self.rt.mainloop()

if __name__=='__main__':
    gb = graphBoard(400)
    gb.run()
