# Makefile 2024-07-26

all: config.bin bin2hex.bin

config.bin: config.gpl screen.gpl
	xga99.py --aorg 0x6000 $< -L config.lst -o config.bin

bin2hex.bin: bin2hex.asm
	xas99.py -R $< -L bin2hex.lst

