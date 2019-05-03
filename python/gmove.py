#!/usr/bin/python
from graphics import *
import time
import os

WIDTH, HEIGHT = 400, 400
RADIUS = 40


def typingTxt(win, tObj, msg, delay):
    os.system('mpg321 typeSound.mp3 &')
    for i in range(len(msg)):
        tObj.setText(msg[:i+1])
        time.sleep(delay)

def main():
    #win = GraphWin('Lab Four', WIDTH, HEIGHT,autoflush=False)
    win = GraphWin('Lab Four', WIDTH, HEIGHT)
    wWidth = win.getWidth()
    wHeight = win.getHeight()

    '''
    c = Circle(Point(100, 50), RADIUS)
    c.draw(win)
    c.setFill('red')

    s = Rectangle(Point(300, 300), Point(350, 350))
    s.draw(win)
    s.setFill('blue')

    #myImage = Image(Point(25,25), 'tenor.gif')
    #myImage.draw(win)

    while c.getCenter().getX() < WIDTH - RADIUS:
        c.move(0.1, 0)
        s.move(-0.1, 0)
        #time.sleep(0.1)
        update(30)
    #s.undraw()
    '''
    msg = "GET READY !!!\n\nSTART SHOOTING !!!"
    t1 = Text(Point(wWidth/2, wHeight/2), "")
    t1.setFace("arial")
    t1.setStyle("bold")
    t1.setSize(18)
    t1.setTextColor("brown")
    t1.draw(win)
    typingTxt(win, t1, msg, 0.1)

    win.getMouse()
    win.close()

main()
