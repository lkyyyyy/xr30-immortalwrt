#!/bin/bash
#
# 在 feeds 安装完成后应用补丁和自定义文件。

# 从官方 RAX3000M NAND 定义派生独立 XR30 profile，再应用 XR30 灯光差异。
cp target/linux/mediatek/dts/mt7981b-cmcc-rax3000m.dts \
  target/linux/mediatek/dts/mt7981b-cmcc-xr30.dts
python3 ../scripts/patch-xr30-leds.py target/linux/mediatek/dts/mt7981b-cmcc-xr30.dts
python3 ../scripts/add-xr30-profile.py target/linux/mediatek/image/filogic.mk

# feeds/install may have cached the target-device Kconfig before the custom
# profile existed. Force make defconfig to regenerate it with cmcc_xr30.
rm -rf tmp

# 自定义文件（uci-defaults 等）随镜像打包
mkdir -p files
cp -a ../files/. files/
chmod +x files/etc/uci-defaults/*.sh

