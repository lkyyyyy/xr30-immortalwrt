#!/usr/bin/env python3
"""Derive a dedicated XR30 NAND image profile from ImmortalWrt's RAX3000M profile."""

import re
import sys


path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

if "define Device/cmcc_xr30" in text:
    print("XR30 profile already present:", path)
    raise SystemExit(0)

match = re.search(
    r"define Device/cmcc_rax3000m\n.*?\nendef\n\nTARGET_DEVICES \+= cmcc_rax3000m",
    text,
    re.DOTALL,
)
if not match:
    raise SystemExit("cmcc_rax3000m device profile not found in " + path)

profile = """define Device/cmcc_xr30
  DEVICE_VENDOR := CMCC
  DEVICE_MODEL := XR30 NAND
  DEVICE_DTS := mt7981b-cmcc-xr30
  $(call Device/cmcc_rax3000m_common)
  DEVICE_DTS_OVERLAY := mt7981b-cmcc-rax3000m-nand
  ARTIFACTS := nand-preloader.bin nand-bl31-uboot.fip
  ARTIFACT/nand-preloader.bin := mt7981-bl2 spim-nand-ddr4
  ARTIFACT/nand-bl31-uboot.fip := mt7981-bl31-uboot cmcc_rax3000m-nand
endef
TARGET_DEVICES += cmcc_xr30"""

# Keep the official NAND/eMMC overlays and compatible IDs so existing XR30
# installations using the RAX3000M-compatible layout can sysupgrade safely.
text = text[: match.end()] + "\n\n" + profile + text[match.end() :]

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("added XR30 NAND profile:", path)

