#!/bin/sh
# 开启 MTK 硬件 NAT：flow offload + hardware offload
uci set firewall.@defaults[0].flow_offloading='1'
uci set firewall.@defaults[0].flow_offloading_hw='1'
uci commit firewall

exit 0

