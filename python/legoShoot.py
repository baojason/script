#! /usr/bin/python
from nxt.bluesock import BlueSock
from graphics import *
import time
import pygame
import nxt.locator
import re
import os
#import subprocess
#import nxt.direct
pygame.init()
pygame.mixer.init()
bang = pygame.mixer.Sound('bang.mp3')

class NXTBT:
    ID = '00:16:53:0B:AE:FD'
    CHANNEL = 0
    MAILBOX = 0
    slave = 0
    tgt = [ {'wait':0, 'score':0, 'hit':0},{'wait':0, 'score':0, 'hit':0},{'wait':0, 'score':0, 'hit':0}]
    totalScore = 0

    # Create socket to NXT brick
    sock = BlueSock(ID)

    def getTgt(self):
        return self.tgt

    def resetScore(self):
        self.totalScore = 0

    def getScore(self):
        return self.totalScore

    def resetTgt(self):
        for i in range(3):
            self.tgt[i]['score'] = 0
            self.tgt[i]['wait'] = 0
            self.tgt[i]['hit'] = 0

    def getRoundScore(self):
        total = 0
        for t in self.tgt:
            total += t['score']
        return total

    def getMaxWaitTime():
        maxWT = 0
        for t in self.tgt:
            if maxWT < t['wait']:
                maxWT = t['wait']
        return maxWT


    def openConnection(self):
        # On success, socket is non-empty
        if self.sock:
            # Connect to brick
            self.slave = self.sock.connect()
            return True
        else:
            return False
    def closeConnection(self):
        if self.sock:
            self.sock.close()
            return True
        else:
            return False

    def Cmd_EchoMsg(self, msg):
        if self.slave:
            cmdStr = "eo " + msg
            self.slave.message_write(self.CHANNEL, cmdStr)
            try:
                time.sleep(0.01)
                local_box, message = self.slave.message_read(self.MAILBOX+10, self.MAILBOX, True)
                #print local_box, message
                return message
            except nxt.error.DirProtError, e:
                pass
        return ""

    def Cmd_Shoot(self, msg, win):
        if self.slave:
            cmdStr = "sh " + msg
            self.slave.message_write(self.CHANNEL, cmdStr)
            wmsg=0
            wtgt=genTgtName(win)
            offset = 350
            target1 = Image(Point(win.getWidth()/2-offset, 550), "target.png")
            target2 = Image(Point(win.getWidth()/2, 550), "target.png")
            target3 = Image(Point(win.getWidth()/2+offset, 550), "target.png")
            wtime = [0,0,0]
            cwtime = [0,0,0]
            tS = [0,0,0]
            scoMsg = 0
            start = 0
            while True:
                try:
                    time.sleep(0.05)
                    local_box, message = self.slave.message_read(self.MAILBOX+10, self.MAILBOX, True)
                    #print local_box, message
                    if "end" in message:
                        print ("The end")
                        i = 0
                        for t in self.tgt:
                            print ("Target%d score: %d" % (i, t['score']))
                            i+=1
                        break
                    elif "tgt" in message:
                        print message
                        info = re.findall(r'\d+', message)
                        for i, j in zip(info[::2], info[1::2]):
                            self.tgt[int(i)]['wait'] = int(j)
                        i = 0
                        for t in self.tgt:
                            print ("tgt wait time: %u" % t["wait"])
                            wtime[i] = t["wait"]
                            i+=1
                        wmsg=genWMsg(win, wtime)
                        wmsg.draw(win)
                        wtgt.draw(win)
                        wmsgp = genWMsgPrompt(win)
                        wmsgp.draw(win)
                        start = 1
                    elif "wtm" in message:
                        info = re.findall(r'\d+', message)
                        currentTime = int(info[0])
                        for i in range(3):
                            if wtime[i]>(currentTime+200):
                                cwtime[i] = wtime[i]-currentTime
                            else:
                                cwtime[i] = 0
                        if wmsg:
                            wmsg.undraw()
                        wmsg=genWMsg(win, cwtime)
                        wmsg.draw(win)
                    elif "hit" in message:
                        #bang.play()
                        os.system('mpg321 -q bang.mp3 &')
                        print message
                        info = re.findall(r'\d+', message)
                        idx = int(info[0])
                        self.tgt[idx]['hit'] = 1
                        self.tgt[idx]['score'] = 10000 / int(info[1])
                        if scoMsg:
                            scoMsg.undraw()
                        self.totalScore += self.tgt[idx]['score']
                        scoMsg = genScore(win, self.totalScore)
                        scoMsg.draw(win)
                        tS[idx] = genTgtScore(win, self.tgt, idx)
                        tS[idx].draw(win)
                        if info[0]=='0':
                            target1.draw(win)
                        elif info[0]=='1':
                            target2.draw(win)
                        elif info[0]=='2':
                            target3.draw(win)

                except nxt.error.DirProtError, e:
                    pass

            time.sleep(2)
            '''
            if wmsg:
                wmsg.undraw()
            if wtgt:
                wtgt.undraw()
            target1.undraw()
            target2.undraw()
            target3.undraw()
            for i in range(3):
                if self.tgt[i]['hit'] == 1:
                    tS[i].undraw()
            '''



myNxt = NXTBT()

def genWMsgPrompt(win):
    message = Text(Point(win.getWidth()/2, 200),"Remaining Time")
    message.setTextColor('pink')
    message.setSize(30)
    return message

def genWMsg(win, wtime):
    space2 = '                          '
    message = Text(Point(win.getWidth()/2, 250),
            '{:<4}'.format(str(wtime[0])) + space2 + '{:<4}'.format(str(wtime[1])) + space2 +
            '{:<4}'.format(str(wtime[2])))
    message.setTextColor('red')
    message.setSize(30)
    return message

def genTgtName(win):
    space = '                             '
    message = Text(Point(win.getWidth()/2, 300), 'A' + space + 'B' + space + 'C')
    message.setTextColor('yellow')
    message.setSize(32)
    return message

def genTgtScore(win, tgt, tn):
    offset = (1-tn)*350
    tScore = Text(Point(win.getWidth()/2-50-offset, 760), str(tgt[tn]['score']) + '-POINT')
    tScore.setTextColor('yellow')
    tScore.setSize(32)
    return tScore

def typingTxt(win, tObj, msg, delay):
    os.system('mpg321 typeSound.mp3 &')
    for i in range(len(msg)):
        tObj.setText(msg[:i+1])
        time.sleep(delay)

def showStarting(win):
    msg = "GET READY !!!\n\nSTART SHOOTING !!!"
    wWidth = win.getWidth()
    wHeight = win.getHeight()
    t1 = Text(Point(wWidth/2, wHeight/2), "")
    t1.setFace("arial")
    t1.setStyle("bold")
    t1.setSize(30)
    t1.setTextColor("green")
    t1.draw(win)
    typingTxt(win, t1, msg, 0.08)
    time.sleep(0.5)
    t1.undraw()
    '''
    os.system('mpg321 -q grenade.mp3 &')
    message = Text(Point(win.getWidth()/2, 100), 'Get Ready...')
    message.setTextColor('blue')
    message.setSize(32)
    message.draw(win)
    time.sleep(1.5)
    message2 = Text(Point(win.getWidth()/2, 200), 'Start to shoot...')
    message2.setTextColor('red')
    message2.setSize(32)
    message2.draw(win)
    time.sleep(0.5)
    message.undraw()
    message2.undraw()
    '''

def genScore(win, score):
    scoreMsg = Text(Point(win.getWidth()/2, 50), 'SCORE: ' + str(score))
    scoreMsg.setTextColor('green')
    scoreMsg.setSize(32)
    return scoreMsg


def clearwin(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def shootWin():
    width = 1280
    height = 720
    win = GraphWin('SHOOTING GAME', width, height)
    win.setBackground(color_rgb(0,0,0))
    if myNxt.openConnection():
        while True:
            msg = myNxt.Cmd_EchoMsg("NXT Bluetooth is successfully set")
            if msg != "":
                print ("%s" % msg)
                break
            else:
                print ("waiting...")
        while True:
            showStarting(win)
            myNxt.resetScore()
            myNxt.resetTgt()
            myNxt.Cmd_Shoot("target 1", win)
            if myNxt.getRoundScore() != 0:
                myNxt.resetTgt()
                clearwin(win)
                myNxt.Cmd_Shoot("target 2", win)
            scoMsg = genScore(win, myNxt.getScore())
            scoMsg.draw(win)
            win.getMouse()
            clearwin(win)

    myNxt.closeConnection()
    '''
    while True:
        hit1 = 0
        hit2 = 0
        hit3 = 0
        message = Text(Point(win.getWidth()/2, win.getHeight()/2), 'Click anywhere to start.')
        message.setTextColor('white')
        message.setSize(20)
        message.draw(win)
        win.getMouse()
        message.undraw()

        space = '                             '
        message = Text(Point(win.getWidth()/2, 300), 'A' + space + 'B' + space + 'C')
        message.setTextColor('yellow')
        message.setSize(32)
        message.draw(win)
        time.sleep(1)

        tgt = myNxt.getTgt()

        for i in range(100):
            space2 = '                          '
            message2 = Text(Point(win.getWidth()/2, 250),
                    '{:<4}'.format(str(a[0])) + space2 + '{:<4}'.format(str(a[1])) + space2 + '{:<4}'.format(str(a[2])))
            message2.setTextColor('red')
            message2.setSize(30)
            message2.draw(win)
            if i==10:
                if hit1 == 0:
                    target1.draw(win)
                    hit1 = 1
            if i==50:
                if hit2 == 0:
                    target2.draw(win)
                    hit2 = 1
            if i==90:
                if hit3 == 0:
                    target3.draw(win)
                    hit3 = 1
            time.sleep(0.1)
            message2.undraw()
            a[0] -= 500
            a[1] -= 500
            a[2] -= 500

        target1.undraw()
        target2.undraw()
        target3.undraw()
        message.undraw()
    '''
    win.getMouse()
    win.close()
'''
Main function
'''
if __name__=="__main__":
    print("NXT Shooting Game!")
    shootWin()
    '''
    if myNxt.openConnection():
        while True:
            msg = myNxt.Cmd_EchoMsg("NXT Bluetooth is successfully set")
            if msg != "":
                print ("%s" % msg)
                break
            else:
                print ("waiting...")
        myNxt.Cmd_Shoot("target 1")
    myNxt.closeConnection()
    '''
