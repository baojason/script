#!/usr/bin/python3
'''
  You have 4 cards each containing a number from 1 to 9. You need to judge whether they
  could operated through *, /, +, -, (, ) to get the value of 24.

  Example 1:
Input: [4, 1, 8, 7]
Output: True
Explanation: (8-4) * (7-1) = 24
Example 2:
Input: [1, 2, 1, 2]
Output: False

Note:

The division operator / represents real division, not integer division.
For example, 4 / (1 - 2/3) = 12.

Every operation done is between two numbers. In particular, we cannot use - as a unary 
operator. For example, with [1, 1, 1, 1] as input, the expression -1 - 1 - 1 - 1 is not allowed.

You cannot concatenate numbers together. For example, if the input is [1, 2, 1, 2], we cannot
write this as 12 + 12.
'''
import random
from simple_term_menu import TerminalMenu

class game24:
    def __init__(self, cards=[]):
        '''
        Generate random 4 numbers (1~13)
        '''
        self.cards = []
        if len(cards)==0:
            self.cards.append(random.randint(1,13))
            self.cards.append(random.randint(1,13))
            self.cards.append(random.randint(1,13))
            self.cards.append(random.randint(1,13))
        else:
            for i in cards:
                self.cards.append(i)
        self.operSigns=['+','-','-','*','/','/']

    def showCards(self):
        for c in self.cards:
            if c==1 :
                print("A ",end=''),
            elif c<=10:
                print('{:d} '.format(c),end=''),
            elif c==11:
                print("J ",end=''),
            elif c==12:
                print("Q ",end=''),
            elif c==13:
                print("K ",end=''),
        print()
    def __computeNewVals(self, vals, a, b):
        vals.append(a+b)
        vals.append(a-b)
        vals.append(b-a)
        vals.append(a*b)
        if b != 0:
            vals.append(a/b)
        if a != 0:
            vals.append(b/a)

    def __find24(self, cards):
        sz = len(cards)
        if sz < 1:
            return False
        if sz == 1:
            if abs(cards[0]-24)<0.0001:
                return True
            else:
                return False
        for i in range(sz):
            for j in range(i+1, sz):

                #operVals
                operVals = []
                self.__computeNewVals(operVals, cards[i], cards[j]);
                newVals = []
                for x in range(sz):
                    if x!=i and x!=j:
                        newVals.append(cards[x])
                for x in range(len(operVals)):
                    newVals.append(operVals[x])
                    if self.__find24(newVals)==True:
                        print ('{:.0f}<={:s}[{:.0f},{:.0f}],'.format(operVals[x], self.operSigns[x], cards[i],cards[j]),end=''),
                        return True
                    newVals.pop()
        return False
    def solve24(self):
        fcards =[]
        for i in self.cards:
            fcards.append(float(i))
        if not self.__find24(fcards):
            print ("Cannot solve this problem!!!")

def main():
    terminal_menu = TerminalMenu(["Random", "Input"])
    return terminal_menu.show()

if __name__ == '__main__':
    print ("Find a metod by using +-*/ with the following cards numbers that the result is 24")
    sel = main()
    #print('sel={:d}'.format(sel))
    cards = []
    if sel==1:
        a=input()
        a=a.split( )
        for i in a:
            if i.upper() == "A":
                cards.append(1)
            elif i.upper() == "J":
                cards.append(11)
            elif i.upper() == "Q":
                cards.append(12)
            elif i.upper() == "K":
                cards.append(13)
            else:
                cards.append(int(i))
        print (cards)
    g1 = game24(cards)
    g1.showCards()
    g1.solve24()
    print()
