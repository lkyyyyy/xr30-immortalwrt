#!/bin/bash
#
# 在 feeds update 之前追加第三方源。
# OpenClash 固定到已验证的提交，保证构建可复现、不跟快照漂移。
echo 'src-git openclash https://github.com/vernesong/OpenClash.git^c3a33c1d3407956fdf8f0e0b7c1a4c52e6ad9593' >> feeds.conf.default

