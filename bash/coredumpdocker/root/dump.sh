#!/bin/bash
usage=$(
cat <<EOF
$0 [OPTION[VALUE]]
-c: coredump file
-s: symbol file
-x: gdbcmd file
-h: help
EOF
)

COREDUMP="/root/coredump.tar.gz"
SYMBOL="/root/symbolfile"
CMD="/root/gdbcmd.txt"

while getopts c:hs:x: option
do
    case "${option}" in
        c) COREDUMP=${OPTARG};;
        s) SYMBOL=${OPTARG};;
        x) CMD=${OPTARG};;
        h) echo "$usage"
        exit 0;;
        *) echo "$usage"
        exit 1;;
    esac
done

# untar coredump.tar.gz
tar -zxf $COREDUMP
cd core_dump
COREDUMP=$(find . -type f -iname "*-core-repon_olt*.gz")
gunzip $COREDUMP
COREDUMP=$(pwd)/$(find . -type f -iname "*-core-repon_olt*")
cd ..

# decode the the core dump with gdb
x86_64-linux-gdb -q -s $SYMBOL -c $COREDUMP -x $CMD
