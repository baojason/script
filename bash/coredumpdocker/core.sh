#!/bin/bash

usage=$(
cat <<EOF
$0 [OPTION[VALUE]]
-a: http address of the deb file to be installed as debug symbols (must be used with -b)
-b: http address of deb file to be installed as executable (must be used with -a)
-g: go into /bin/bash of docker coredump
-c: coredump file
-h: help
-m: manually decode
-o: online debugging
-p: package folder path (line dml build folder)
-s: symbol file
-t: tlc folder path, include usr/x86_64-buildroot-linux-gnu/sysroot

Examples:
1. Decoding release (Jenkins Build) exception report
   ./core.sh -c <exception tar.gz file> -a <debug deb file> -b <executable deb file>
   ./core.sh -a https://artifactory.adtran.com/artifactory/debian-local/pool/adpackage/main/d/dml/dml-dbg_2.2.29.1-e4.1.1.1-line_amd64.deb -b https://artifactory.adtran.com/artifactory/debian-local/pool/adpackage/main/d/dml/dml_2.2.29.1-e4.1.1.1-line_amd64.deb -c /home/jbao/win_repon/exception_report_core_dump_repon_olt-19.1-2626_REPON_OLT_2018_10_19_15_05_04_218396046.tar.gz

2. Decoding development (local build) exception report
   ./core.sh -mc <exception tar.gz file> -t <tool chain folder> -s <bcm.user symbol file>
   ./core.sh -mc /home/jbao/win_repon/exception_report_core_dump_repon_olt-19.1-2626_REPON_OLT_2018_10_19_15_05_04_218396046.tar.gz -t /home/jbao/Perforce/jbao_gwd/bld_repon_olt/tlc/ -s /home/jbao/addml/out/line/build/target/dml/FSU7100/FSR/MAKE/FSR714X/arad/BroadcomSDK/build/linux/user/fsr714x-2_6/bcm.user.dbg

3. Go into the docker to have everything done manually
   ./core.sh [-g]

4. Online debugging on release build
   ./core.sh -op <line-dml "adpkgdml/dml" build folder>  -a <debug deb file> -b <executable deb file>
   ./core.sh -op ~/addml -a https://artifactory.adtran.com/artifactory/debian-local/pool/adpackage/main/d/dml/dml-dbg_2.2.55.1-e4.1.1.1-line_amd64.deb -b https://artifactory.adtran.com/artifactory/debian-local/pool/adpackage/main/d/dml/dml_2.2.55.1-e4.1.1.1-line_amd64.deb

5. Online debugging on development bcm.user
   ./core.sh -ot <tool chain folder> -s <bcm.user symbol file> -p <line-dml "adpkgdml/dml" build folder>
   ./core.sh -op ~/addml -t ~/Perforce/jbao_gwd/tlc/ -s ~/addml/out/line/build/target/dml/FSU7100/FSR/MAKE/FSR714X/arad/BroadcomSDK/build/linux/user/fsr714x-2_6/bcm.user.dbg

EOF
)

COREDUMP="/home/$USER/coredump.tar.gz"
SYMBOL="/home/$USER/gdbsymbolfile"
TMPBUILD="/home/$USER/tmp/build"
TLC="/home/$USER"
PKG="/home/$USER"
DEB_DBG_FILE=""
DEB_EXE_FILE=""
MAN=false
ONLINE=false
BASHELL=false
touch $COREDUMP
touch $SYMBOL
mkdir -p $TMPBUILD

while getopts a:b:c:ghmop:s:t:u: option
do
    case "${option}" in
        a) DEB_DBG_FILE=${OPTARG};;
        b) DEB_EXE_FILE=${OPTARG};;
        c) COREDUMP=${OPTARG};;
        g) BASHELL=true;;
        m) MAN=true;;
        o) ONLINE=true;;
        p) PKG=${OPTARG};;
        s) SYMBOL=${OPTARG};;
        t) TLC=${OPTARG};;
        u) TMPBUILD=${OPTARG};;
        h) echo "$usage"
        exit 0;;
        *) echo "$usage"
        exit 1;;
    esac
done

if [ "$BASHELL" = true ]; then
    echo "go into bash..."
    echo "$#"
fi
COREDUMP_CMD=""
if [ "$BASHELL" = true ] || [ "$#" -eq 0 ]; then
    echo "go into bash..."
    COREDUMP_CMD="/bin/bash"
elif [ "$MAN" = true ]; then
    COREDUMP_CMD="/root/decode.sh"
elif [ "$ONLINE" = true ]; then
    if [ -z "$DEB_DBG_FILE" ] || [ -z "$DEB_EXE_FILE" ]; then
        COREDUMP_CMD="/root/online.sh"
    else
        COREDUMP_CMD="/root/online.sh -a$DEB_DBG_FILE -b$DEB_EXE_FILE -x /root/gdbcmd_online_rel.txt"
    fi
else
    if [ -z "$DEB_DBG_FILE" ] || [ -z "$DEB_EXE_FILE" ]; then
        echo "-a and -b are missing..."
        echo "$usage"
        exit 1
    fi
    BCMUSER="/usr/local/bin/bcm.user"
    COREDUMP_CMD="/root/decode.sh -s$BCMUSER -a$DEB_DBG_FILE -b$DEB_EXE_FILE"
fi

echo $COREDUMP_CMD
sudo docker run -it \
    -v $COREDUMP:/root/coredump.tar.gz \
    -v $SYMBOL:/root/symbolfile \
    -v $TLC:/root/tlc \
    -v $PKG:/root/package \
    -v $TMPBUILD:/tmp/build/bld_repon_olt coredump \
    $COREDUMP_CMD
