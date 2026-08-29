#!/usr/bin/env python3
#
# XR30 与 RAX3000M 的 LED GPIO 不同：
#   RAX3000M: 绿 GPIO9、蓝 GPIO12、红 GPIO35
#   XR30:     白 GPIO34、红 GPIO35
#
# 用法: python3 patch-xr30-leds.py <mt7981b-cmcc-rax3000m.dts>
import re
import sys


path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

if "\t\tled-running = &green_led;" not in text:
    raise SystemExit("led-running alias not found in " + path)

if '\tmodel = "CMCC RAX3000M";' not in text:
    raise SystemExit("RAX3000M model string not found in " + path)

text = text.replace(
    '\tmodel = "CMCC RAX3000M";',
    '\tmodel = "CMCC XR30";',
    1,
)

text = text.replace(
    "\t\tled-running = &green_led;",
    "\t\tled-running = &white_led;",
)
text = text.replace(
    "\t\tled-upgrade = &green_led;",
    "\t\tled-upgrade = &red_led;",
)

pattern = re.compile(
    r'\tgpio-leds \{\n'
    r'\t\tcompatible = "gpio-leds";\n'
    r'\n'
    r'\t\tgreen_led: led-0 \{.*?\n'
    r'\t\};\n'
    r'\};',
    re.DOTALL,
)
replacement = (
    "\tgpio-leds {\n"
    '\t\tcompatible = "gpio-leds";\n'
    "\n"
    "\t\twhite_led: led-0 {\n"
    "\t\t\tfunction = LED_FUNCTION_STATUS;\n"
    "\t\t\tcolor = <LED_COLOR_ID_WHITE>;\n"
    "\t\t\tgpios = <&pio 34 GPIO_ACTIVE_LOW>;\n"
    "\t\t};\n"
    "\n"
    "\t\tred_led: led-1 {\n"
    "\t\t\tfunction = LED_FUNCTION_STATUS;\n"
    "\t\t\tcolor = <LED_COLOR_ID_RED>;\n"
    "\t\t\tgpios = <&pio 35 GPIO_ACTIVE_LOW>;\n"
    "\t\t};\n"
    "\t};\n"
    "};"
)

text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit("gpio-leds block not found in " + path)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("patched XR30 LEDs:", path)

