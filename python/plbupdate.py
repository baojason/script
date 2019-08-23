#!/usr/bin/python3
'''
Tool plbupdate.py
Used to update ONU MAC inside the OAM messages written in BRCM playback file (plb)
usage: plbupdate.py [-h] [-r R] [-o O] fname newmac
'''
import os
import argparse
import glob
import errno

defaultOutFile = '__noNewFile__'
defaultOldMac = '<ONU_MAC>'
path = os.path.join('output')

class replaceStrInFile:
    ''' Replace a string with another one inside a file '''
    def __init__(self, fileName, newStr, oldStr=defaultOldMac, newFileName=defaultOutFile):
        self.fileName = fileName
        self.oldStr = oldStr
        self.newStr = newStr
        self.newFileName = newFileName

    def updateFileName(self, fileName):
        self.fileName = fileName

    def updateNewFileNameWithPath(self):
        self.newFileName = os.path.join(path, self.fileName)

    def updateNewFileNameAsTempl(self):
        fname, extension = os.path.splitext(self.fileName)
        self.newFileName = os.path.join(path, fname + '_Templ' + extension)

    def doReplace(self):
        file_out = 'tmp.txt'
        newFile = False
        if self.newFileName != defaultOutFile:
            newFile = True
            file_out = self.newFileName
        with open(self.fileName, "rt") as fin:
            with open(file_out, "wt") as fout:
                for line in fin:
                    fout.write(line.replace(self.oldStr, self.newStr))
        if not newFile:
            os.rename(file_out, self.fileName)
        return True

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mac', help='NEW ONU MAC address')
    parser.add_argument('-f', help='Input a plb filename')
    parser.add_argument('-r', help='OLD MAC address to be replaced, (skip this when using template plb file)')
    parser.add_argument('-o', help='Input an output filename')
    parser.add_argument('-a','--all', help='Update All plb files', action='store_true')
    args = parser.parse_args()
    #print(args)
    #print(args.r)

    try:
        os.makedirs(path)
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    if args.all:
        replaceObject = replaceStrInFile("filename", args.mac,
                                         args.r if args.r != None else defaultOldMac,
                                         "outfile")
        for f in glob.glob("OAM*.plb"):
            replaceObject.updateFileName(f)
            replaceObject.updateNewFileNameWithPath()
            replaceObject.doReplace()
        print("Done for all plb files")
    else:
        replaceObject = replaceStrInFile(args.fname, args.newmac,
                                         args.r if args.r != None else defaultOldMac,
                                         args.o if args.o != None else defaultOutFile)
        if replaceObject.doReplace():
            print("Successfully update the plb file \"%s\" with ONU MAC \"%s\"" % (replaceObject.fileName,
                   replaceObject.newStr))
