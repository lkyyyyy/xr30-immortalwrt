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

if not re.search(r"(?m)^define Device/cmcc_rax3000m(?:\s|$)", text):
    raise SystemExit("cmcc_rax3000m device profile not found in " + path)
if not re.search(r"(?m)^define Device/cmcc_rax3000m_common(?:\s|$)", text):
    raise SystemExit("cmcc_rax3000m common profile not found in " + path)

# Anchor the insertion to the TARGET_DEVICES line. The surrounding blank
# lines in filogic.mk have changed between releases and are not significant.
match = re.search(
    r"(?m)^TARGET_DEVICES\s*\+=\s*cmcc_rax3000m\s*$",
    text,
)
if not match:
    raise SystemExit("cmcc_rax3000m target registration not found in " + path)

profile = """define Device/cmcc_xr30
  DEVICE_VENDOR := CMCC
  DEVICE_MODEL := XR30 NAND
  DEVICE_DTS := mt7981b-cmcc-xr30
  SUPPORTED_DEVICES := cmcc,rax3000m
  $(call Device/cmcc_rax3000m_common)
  DEVICE_DTS_OVERLAY := mt7981b-cmcc-rax3000m-nand
  ARTIFACTS :=
endef
TARGET_DEVICES += cmcc_xr30"""

# Keep the official NAND overlay and compatible ID so existing XR30
# installations using the RAX3000M-compatible layout can sysupgrade safely.
# Do not emit bootloader artifacts: normal sysupgrade does not need them, and
# rebuilding or flashing a bootloader unnecessarily increases recovery risk.
text = text[: match.end()] + "\n\n" + profile + text[match.end() :]

if text.count("define Device/cmcc_xr30") != 1 or text.count(
    "TARGET_DEVICES += cmcc_xr30"
) != 1:
    raise SystemExit("XR30 profile injection validation failed for " + path)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("added XR30 NAND profile:", path)
