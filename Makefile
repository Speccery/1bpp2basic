# Makefile 2024-07-26

all: config.bin bin2hex.bin

config.bin: config.gpl screen.gpl
	xga99.py --aorg 0x6000 $< -L $*.lst -o $@

bin2hex.bin: bin2hex.asm
	xas99.py -b -R $< -L $*.lst

bin2hex.gpl: bin2hex.bin
	python3 bin2gpl.py --maxlen 34 $< $@
