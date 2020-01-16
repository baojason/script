#!/bin/sh
###############################################################################
#                                                                             #
#  restart bcm - restarts bcm.user and services                               #
#                                                                             #
###############################################################################

stop_services()
{
  /etc/init.d/service_supervisor stop line_dml_startup_daemon
  /etc/init.d/S081_start_udhcpc stop
  /etc/init.d/S081_start_udhcpc stop6
  /etc/init.d/S073_wpa_supplicant.sh stop
}

start_services()
{
  /etc/init.d/S073_wpa_supplicant.sh start
  /etc/init.d/S081_start_udhcpc start
  /etc/init.d/S081_start_udhcpc start6
  /etc/init.d/S992_set_static_ipv4.sh start
  /etc/init.d/S993_set_static_ipv6.sh start
  /etc/init.d/service_supervisor start line_dml_startup_daemon
}

stop_services
/etc/init.d/S061_init_bcm.sh restart
start_services
