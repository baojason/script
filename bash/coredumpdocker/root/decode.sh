#!/bin/bash
usage=$(
cat <<EOF
$0 [OPTION[VALUE]]
-a: http address of the deb file to be installed as debug symbols
-b: http address of deb file to be installed as executable
-c: coredump file
-s: symbol file
-x: gdbcmd file
-h: help
EOF
)

COREDUMP="/root/coredump.tar.gz"
SYMBOL="/root/symbolfile"
CMD="/root/gdbcmd.txt"
CMD_DECODE_RELEASE="/root/gdbcmd_decoderelease.txt"
DEB_DBG_FILE=""
DEB_EXE_FILE=""

GDB="x86_64-linux-gdb"
# Check if GDB exist
if [ -z "$(command -v $GDB)" ]; then
    GDB="gdb"
fi

while getopts a:b:c:g:hs:x: option
do
    case "${option}" in
        a) DEB_DBG_FILE=${OPTARG};;
        b) DEB_EXE_FILE=${OPTARG};;
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

if [ -z "$DEB_DBG_FILE" ] || [ -z "$DEB_EXE_FILE" ]; then
    # decode the the core dump generated against development build (manually)
    $GDB -q -s $SYMBOL -c $COREDUMP -x $CMD
else
    # download and install dbg and exe deb files
    mkdir deb
    cd deb
    wget $DEB_DBG_FILE
    wget $DEB_EXE_FILE
    DEB_EXE_FILE=$(find . -type f -iname "dml_*.deb")
    DEB_DBG_FILE=$(find . -type f -iname "dml-dbg_*.deb")
    dpkg -i $DEB_EXE_FILE
    dpkg -i $DEB_DBG_FILE
    cd ..

    # decode the the core dump generated against release build
    $GDB -q -s $SYMBOL -c $COREDUMP -x $CMD_DECODE_RELEASE
fi

