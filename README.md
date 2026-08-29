# ImmortalWrt 固件构建工程（XR30 NAND / RAX3000M 通刷）

用 GitHub Actions 构建 CMCC XR30 NAND（256MB 闪存 + 512MB 内存）可用的 ImmortalWrt v24.10.6 稳定版固件。
设备 profile 使用官方稳定版的 `cmcc_rax3000m`（官方固件 NAND/eMMC 通刷），并内置 XR30 灯光补丁。

## 已内置功能

- Android / iPhone USB 网络共享（RNDIS、NCM、ipheth、usbmuxd）
- 5G USB 通信模块（QMI、MBIM、NCM、AT 拨号：uqmi / umbim / comgt）
- USB 硬盘挂载与 Samba 共享（ext4、vfat、exfat、ntfs3，Windows 可发现）
- 硬件加速 HNAT（MTK PPE + nftables flow offload，首次启动自动开启）
- OpenClash（Clash 内核可在 OpenClash 界面内下载）
- LuCI 中文界面

## 使用方法

1. 在 GitHub 新建一个仓库，把本目录所有文件推上去。
2. 打开仓库的 **Actions** 页面，选择 **Build ImmortalWrt for XR30 NAND**，点击 **Run workflow**。
3. 默认使用官方稳定版 `v24.10.6`，构建完成后在本次运行的 **Artifacts** 中下载固件。
4. NAND 版刷 `...cmcc_rax3000m-squashfs-sysupgrade.itb`（U-Boot 或 LuCI sysupgrade）。

软件源使用官方稳定版 tag `v24.10.6`，不是 snapshot。

## 后续添加功能

两种方式，不用改工作流：

- 编辑 `config/xr30.config`，加一行 `CONFIG_PACKAGE_包名=y`，然后推送到仓库自动重新构建。
- 在 Actions 的 **Run workflow** 里填写 `extra_packages`，例如：
  `kmod-usb-printer luci-app-ttyd`

想升级到其他官方稳定版时，在 Run workflow 里把 `source` 改为 `v25.12.1` 等 tag 即可。

## XR30 灯光说明

XR30 与 RAX3000M 的 LED GPIO 不同：

- RAX3000M：绿 GPIO9、蓝 GPIO12、红 GPIO35
- XR30：白 GPIO34、红 GPIO35

`scripts/patch-xr30-leds.py` 会在构建时把 DTS 改成 XR30 的灯位并更新 `led-running` 等状态灯。
如果之后要刷回普通 RAX3000M，删除该脚本调用再构建即可。

## 目录结构

```text
.github/workflows/build.yml   GitHub Actions 构建流程
config/xr30.config            固件功能配置种子
scripts/diy-part1.sh          feeds 更新前执行（追加 OpenClash 源）
scripts/diy-part2.sh          feeds 安装后执行（灯光脚本和自定义文件）
scripts/patch-xr30-leds.py    XR30 灯光 DTS 修改脚本
files/etc/uci-defaults/      首次启动脚本（开启 HNAT）
```

