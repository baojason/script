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
    def __init__(self, cvSize, gameSize):
        # Check the cvSize and gameSize
        if cvSize < 200 or cvSize > 800 or gameSize < 3 or gameSize > 19:
            raise ValueError("Wrong Canvas Size - %d" % (cvSize))
        self.cvSz = cvSize
        self.gSz = gameSize

        # Create a canvas for drawing
        self.rt = tk.Tk()
        self.cv = tk.Canvas(self.rt, width = self.cvSz, height = self.cvSz, bg = 'white')
        self.cv.pack()

        # Draw a rectangle shape
        offset = 10
        x1 = offset
        y1 = offset
        x2 = self.cvSz - x1
        y2 = self.cvSz - y1
        self.bgcv = rectData(self.cv, 'myBackgroud', (x1,y1), (x2,y2))

        # Draw a title
        self.rt.title("Tic Tac Toe")

        # Draw lattices
        self.latticeSz = int((self.cvSz - 2 * offset) / self.gSz)
        for i in range(self.gSz+1):
            xi = x1 + i * self.latticeSz
            yi = y1 + i * self.latticeSz
            self.cv.create_line(x1, yi, x2, yi)  # Draw a vertical line
            self.cv.create_line(xi, y1, xi, y2)  # Draw a horizontal line

    def run(self):
        # Go into the main loop to capture mouse clicks
        self.rt.mainloop()

if __name__=='__main__':
    gb = graphBoard(400, 4)
    gb.run()
