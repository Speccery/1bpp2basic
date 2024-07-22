#!/bin/bash
xga99.py --aorg 0x6000 config.gpl -L config.lst -o config.bin
dd if=/dev/zero bs=1 count=$(expr 8192 - $(stat -f "%Dz" config.bin))  >> config.bin
# Add the firmware into the next 16K
dd if=../STM32EP/grommy2/Release/grommy2.bin bs=1 count=16K >> config.bin
