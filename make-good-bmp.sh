
# DIRLIB=~/Library/Mobile\ Documents/4R6749AYRE~com~pixelmatorteam~pixelmator/Documents
# echo $DIRLIB/grommy2-update-edited.png
# cp "$DIRLIB/grommy2-update-edited.png" grommy2-update-edited.png
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