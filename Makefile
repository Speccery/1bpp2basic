# Makefile 2024-07-26

config.bin: config.gpl screen.gpl
	xga99.py --aorg 0x6000 config.gpl -L config.lst -o config.bin
