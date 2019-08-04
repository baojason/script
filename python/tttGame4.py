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

        self.latticeSz = int((self.cvSz - 2 * offset) / self.gSz)
        x1 = offset
        y1 = offset
        x2 = x1 + self.gSz * self.latticeSz
        y2 = y1 + self.gSz * self.latticeSz

        self.bgcv = rectData(self.cv, 'myBackgroud', (x1,y1), (x2,y2))

        # Draw a title
        self.rt.title("Tic Tac Toe")

        # Draw lattices
        for i in range(self.gSz+1):
            xi = x1 + i * self.latticeSz
            yi = y1 + i * self.latticeSz
            self.cv.create_line(x1, yi, x2, yi)  # Draw a vertical line
            self.cv.create_line(xi, y1, xi, y2)  # Draw a horizontal line

        # Create a string message
        self.strMsg = tk.StringVar()
        tk.Label(self.rt, textvariable=self.strMsg, font=("Helvetica", 16)).pack()

        # bind left mouse click within the self.bgcv shape
        self.cv.tag_bind(self.bgcv.tag, '<Button-1>', self.click)

    def click(self, event):
        x, y = event.x - self.bgcv.pt1[0], event.y - self.bgcv.pt1[1]
        # convert x,y to lattice coordinate. E.g.  The lattice at the second row,
        # and the third column would be assoicated (3-1,2-1) as the x,y
        x, y = int(x / self.latticeSz), int(y / self.latticeSz)
        xy = '{:>4}, {:>4}'.format(x,y)
        self.strMsg.set(xy)

    def run(self):
        # Go into the main loop to capture mouse clicks
        self.rt.mainloop()

if __name__=='__main__':
    gb = graphBoard(600, 19)
    gb.run()
