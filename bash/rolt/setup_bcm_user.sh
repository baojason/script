#!/bin/sh
###############################################################################
#                                                                             #
#  setup bcm.user - takes optional argument of new bcm.user path              #
#                 - moves new bcm.user into place                             #
#                 - launches bcm restart script to run in background          #
#                                                                             #
###############################################################################

if [ -n "$1" ]; then
  if [ -e "$1" ]; then
    rm -f /usr/local/bin/bcm.user
    if mv -f "$1" /usr/local/bin/bcm.user; then
      echo File "$1" moved into place
    else
      echo Move of file "$1" failed
      exit 1
    fi
  else
    echo File "$1" not found
    exit 1
  fi
fi
/etc/init.d/restart_bcm_user.sh &>/dev/null &disown;
