# 1bpp2basic
Simple tool to convert 1 bit per pixel BMP files to TI-99/4A BASIC programs.

## Purpose
I am no graphics designer, but still it is much faster for me to use graphics program to design graphics rather than writing character defitions in hex, the old fashioned way.

## The workflow
Do your design in any graphics drawing program, my tool of choice is Pixelmator for macos. Make the resolution 256*192. Export from the tool some universal format, in my case I export to PNG. Then convert from there to 1 bit per pixel BMP format. I use ImageMagick for that purpose. On a Mac the commands are (using command line):
```
# I use homebrew, the command below installs the imagemagick tools.
# Of course only done once.
brew install imagemagick

# Use one of the tools to convert to 1 bit per pixel.
convert -monochrome grommy2.png grommy2-1bpp.bmp

# Convert to the old BMP V3 format.
mogrify -compress none -format bmp -define bmp:BMP3 grommy2-1bpp.bmp
# Now the bmp picture is ready.
```

Then run the program which does the job, i.e. converts the 1bpp picture to a Basic program for the TI-99/4A:
```
python3 1bpp2basic.py
```

