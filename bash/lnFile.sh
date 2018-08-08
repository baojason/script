#!/bin/bash
: <<END
using regex to match a pattern in "find -name <filename>" and
try to capture the specific pattern content. Use that content
to do further work -- making a soft link to an input file name.
For example:
jbao@cn-vm-bao:~/sumi$ ./lnFile.sh testtest.c
/bin/ln -s /home/jbao/dml/sumitomo-dpoe/FSU7100/Common/dml3/sdk/bcm-sdk/sdk/src/appl/dml/testtest.c ./FSU7100/FSR/MAKE/FSR714X/arad/BroadcomSDK/src/appl/dml/testtest.c
jbao@cn-vm-bao:~/sumi$
END

regex='->(.*)$'
reg2='(^.*\/).*$'
reg3='(\S*arad\S*)'
NAME="$1"
TARGET="NOTFOUND"
PATH2="EMPTY"

LNFILE=$(find -name DmlBcm.h)
if [[ $LNFILE =~ $reg3 ]]; then
    TARGET=${BASH_REMATCH[1]}
    if [[ $TARGET =~ $reg2 ]]; then
        PATH2=${BASH_REMATCH[1]}
    fi
fi

FULLNAME=$(ls -l $TARGET)
if [[ $FULLNAME =~ $regex ]]; then
    PATH=${BASH_REMATCH[1]}
    if [[ $PATH =~ $reg2 ]]; then
        PATH=${BASH_REMATCH[1]}
        OK="/bin/ln -s$PATH$NAME $PATH2$NAME"
        echo $OK
        eval "$OK"
    fi
fi

