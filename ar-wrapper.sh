#!/bin/bash
# This is a wrapper for ar in GNU bin-utils
# It is intended as a mitigation for a bug in gcc-ar
# Rename toolchain/x86_64-linux/arm-none-eabi/bin/ar to ar_
# then copy this script to toolchain/x86_64-linux/arm-none-eabi/bin and rename to ar
$(dirname $0)/ar_ $(echo $@ | sed "s/-@/@/g")