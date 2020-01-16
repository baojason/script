import os

file_in = "Stud.txt"
file_out = "tmp.txt"
oldStr = ''
newStr = ''
with open(file_in, "rt") as fin:
    with open(file_out, "wt") as fout:
        for line in fin:
            fout.write(line.replace(oldStr, newStr))

os.rename(file_out, file_in)
