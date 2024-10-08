# 1bpp2basic
## Version history

## 2024-08-18 added command line parameters
Now the source and destination filenames can be given with the mandatory --src and --dest tags.
```
python3 1bpp2basic.py --src grommy2-update-edited-mogrify.bmp --dest update.bas
```
The conversion is a bit tedious, so I wrote a shell script which uses imagemagick to convert the picture. This script uses the **xdt99** suite to add the resulting basic program to a disk image which can be easily loaded with js99er.net. Below the file names are quite tedious, but it all starts with the "grommy2-update-edited.png" file and ends with the update.bas BASIC program.
```
convert  -monochrome grommy2-update-edited.png grommy2-update-edited.bmp
cp grommy2-update-edited.bmp grommy2-update-edited-mogrify.bmp
mogrify -compress none -format bmp -define bmp:BMP3 grommy2-update-edited-mogrify.bmp
rm update.bas
python3 1bpp2basic.py --src grommy2-update-edited-mogrify.bmp --dest update.bas
xbas99.py update.bas
# delete old version
xdm99.py diska.dsk -d update.prg
# add new version
echo adding UPDATE.prg
xdm99.py diska.dsk -a UPDATE.prg
```


### 2023-11-26 Now also generates GPL
The code also creates `screen.gpl` file. I also wrote a quick GPL code `config.gpl` which includes the generated screen.gpl file and renders it on screen - this is code is based partially to the GPL code in the Mini Memory module.
Compile with xdt99 toolchain like this:
```
xga99.py --aorg 0x6000 config.gpl -L config.lst -o config.bin
```
The BASIC version is still created as well.

### Initial version
Simple tool to convert 1 bit per pixel BMP files to TI-99/4A BASIC programs. Note that this (stupid) version has a lot of stuff hardcoded, including the BMP header length. This of course make no sense, but consider the program as a quick-and-dirty implementation. Otherwise known as enterprise software.

The benefit of the simple implementation is that code has no dependencies to python frameworks, it is plain vanilla python3.

The program transforms a picture like this:

![grommy2a_config](https://github.com/Speccery/1bpp2basic/assets/18168418/2ab06a5c-b370-4058-82b5-58e0de39696a)

via some steps into a basic program which draws this as captures from the output of the js99er.net emulator:

![Basic program output in js99er.net emulator](https://github.com/Speccery/1bpp2basic/assets/18168418/752cab1f-cd05-4ba3-8aaa-9fd6e045ef45)


## Purpose and "architecture"
I am no graphics designer, but still it is much faster for me to use graphics program to design graphics rather than writing character defitions in hex, the old fashioned way.

Even though the current version spits out a BASIC program (called SCREEEN.BAS by default), it is trivial to change the program to do the output in any format as this is very simple python code. But at the moment out comes a TI BASIC program.

### The *smarts*
The function **alloc_char** is the function which implements "the algorithm", in this case a brute force trivial one.
The input parameter *my_char* is an array of 8 integers, for the 8 pixel rows of the character cell.
The code checks if this matches one of the existing characters. If not, define a new one.
Note: no check is made against any upper boundary... Meaning the code will happily
allocate more user defined characters than actually available in TI Basic.

### The resulting BASIC program
The Basic program has two kinds of entries of interest.

1. Character defintions such as `1030 CALL CHAR(97, "000000030F1F3F3F")` define the character code - in this case 97 - to have a certain shape based on the input picture. The code defines as many characters as needed to describe the graphics. This can easily overflow the codes available in TI BASIC, where the last valid code is 159.
2. Screen definition. There are 768 character cells, and each contains a character such as the 97 above. 
The definition is done so that the very first characted defined (i.e. in top left corner) is assumed to be the *common* background character, often space, and the screen is initially filled with that. Then the produced code has entries like below, which use a subroutine to draw a string of characters with CALL HCHAR.
```1770 X=8
1780 Y=3
1790 A$="234567489:;<=>?@AB"
1800 GOSUB 1650
```
Note that there is an offset, in this case 50, which is used to map character codes into characters in the string A$. The way the program is set up is that it defines the characters starting from the character code 96. 
However, when creating the strings, 50 is substracted so that the A$ strings going to the subroutine contain "easy" to enter characters.
The subroutine adds back the offset. You can change this behaviour by modifying the code.


## The workflow
### Steps
- Do your design in any graphics drawing program, my tool of choice is Pixelmator for macos. 
- Make the resolution 256*192. 
- Export from the tool some universal format, in my case I export to PNG. 
- Then convert from there to 1 bit per pixel BMP format. I use ImageMagick for that purpose. 

On a Mac the commands are (using command line):
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

### Convert to binary
I use the xdt99 suite to convert the resulting BASIC program, in ASCII text format, to a binary version (i.e. tokenized version). The resulting file is SCREEN.PRG
```
perik in ~/Developer/1bpp2basic on main λ xbas99.py SCREEN.BAS
perik in ~/Developer/1bpp2basic on main λ ls -l *.prg
-rw-r--r--  1 perik  staff  2950 Nov 22 19:36 SCREEN.prg
```
The all that remains is to take this program file to an actual TI computer or emulator of your choice and run it.
