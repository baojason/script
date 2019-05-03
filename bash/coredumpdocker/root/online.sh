#!/bin/bash
usage=$(
cat <<EOF
$0 [OPTION[VALUE]]
-a: http address of the deb file to be installed as debug symbols
-b: http address of deb file to be installed as executable
-s: symbol file
-x: gdbcmd file
-h: help
EOF
)

SYMBOL="/root/symbolfile"
CMD="/root/gdbcmd_online_dev.txt"
DEB_DBG_FILE=""
DEB_EXE_FILE=""

GDB="gdbtui"

while getopts a:b:c:g:hs:x: option
do
    case "${option}" in
        a) DEB_DBG_FILE=${OPTARG};;
        b) DEB_EXE_FILE=${OPTARG};;
        s) SYMBOL=${OPTARG};;
        x) CMD=${OPTARG};;
        h) echo "$usage"
        exit 0;;
        *) echo "$usage"
        exit 1;;
    esac
done

if [ -z "$DEB_DBG_FILE" ] || [ -z "$DEB_EXE_FILE" ]; then
    echo "online debug development bcm.user..."
else
    # download and install dbg and exe deb files
    echo "online debug release bcm.user..."
    mkdir deb
    cd deb
    wget $DEB_DBG_FILE
    wget $DEB_EXE_FILE
    DEB_EXE_FILE=$(find . -type f -iname "dml_*.deb")
    DEB_DBG_FILE=$(find . -type f -iname "dml-dbg_*.deb")
    dpkg -i $DEB_EXE_FILE
    dpkg -i $DEB_DBG_FILE
    cd ..
    SYMBOL="/usr/local/bin/bcm.user"
fi

$GDB $SYMBOL -x $CMD

