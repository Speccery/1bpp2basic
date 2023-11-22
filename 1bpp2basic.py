# 1bpp-to-tiles
# Convert a 1 bit-per-pixel bitmap picture to
# tiles. Intended for use with TI-99/4A stuff.
# The input picture is assumed to be simple BMP file.
#
# Picture assumed to have resolution of 256*192
#
# Use tools from imagemagick to convert pictures:
# convert -monochrome grommy2.png grommy2-1bpp.bmp
# cp grommy2-1bpp.bmp grommy2t2.bmp
# mogrify -compress none -format bmp -define bmp:BMP3 grommy2t2.bmp
#
# Started 2023-11-22 EP
#

### config start ###
source_bmp = "grommy2a_config-1bpp.bmp"
offset_to_bits = 0x92   # hardcoded, not good...
first_char = 96
width = 256
height = 192
basic_filename="SCREEN.BAS"
### config end ###

cells = (width*height) >> (3+3)
udg = []
charmap = [first_char] * cells 
charmap_count = [0] * cells
current_char = first_char

# Load the source picture as a binary blob
pict_file = open(source_bmp, "rb")
data = pict_file.read()
pict_file.close()

# print(len(data))
# print(data[0])

# some silly validation
if data[0] != ord('B') or data[1] != ord('M'):
    print("Error bitmap format not good.")
    exit(2)

print(f"File was read, size {len(data)}.")
if len(data) != offset_to_bits + width*height/8:
    print("image size not matching expecation")
    exit(2)

if int(height) & 7 != 0:
    print(f"height {height} not multiple of 8")
    exit(2)

if int(width) & 7 != 0:
    print(f"width {width} not multiple of 8")
    exit(2)


# In the BMP format the picture is upside down.
# Here x is in bytes not pixels, so each increment of x is 8 pixels.
def get_pict_byte(x : int, y : int):
    o = offset_to_bits + x + (height - 1 - y)*(width >> 3)
    # print(f"x={x} y={y} offset={o}")
    return data[ o ]

# my_char is an array of 8 integers, for the 8 pixel rows of the character cell.
# See if this matches one of the existing characters. If not, define a new one.
# Note: no check is made against any upper boundary... Meaning the code will happily
# allocate more user defined characters than actually available in TI Basic.
def alloc_char( my_char : [] ):
    global current_char
    if len(my_char) != 8:
        print(f"error, character definition not 8 bytes {len(my_char)}")
    index = first_char
    for c in udg:
        # compare the present character with my_char, if it matches, return this
        if c == my_char:
            # print(f"Reusing char {index}")
            charmap_count[index - first_char] += 1
            return index
        index += 1
    # no match, allocate a new char
    udg.append( my_char )
    print(f"allocated new char {current_char}: ", end=" ")
    for bits in my_char:
        print(f"{bits:02x} ", end=" ")
    print()
    charmap_count[current_char - first_char] = 1
    current_char += 1
    return current_char-1
    

for y in range(height >> 3):
    for x in range(width >> 3):
        # Here we iterate across the character cells and allocate new characters if 
        # existing data is not matching present character.
        myc = []
        for y2 in range(8):
            myc.append(get_pict_byte(x, y*8+y2))
            # print(f"{hex(myc[y2])} ", end=" ")
        # print()
        charmap[ y*(width >> 3) + x] = alloc_char( myc )

print(f"defined {current_char-first_char} characters")
print("Usage statistics of chars:")
for i in range(first_char, current_char):
    print(f"{i},{charmap_count[i-first_char]}", end=" ")
    if i != current_char-1:
        if (i-first_char) % 4 == 3:
            print(", ")
        else:
            print(",   ", end=" ")
    else:
        print()

##########################################
# Create a basic program defing the screen
fout = open(basic_filename, "wt")
line_num = 1000
print(f"{line_num} REM CREATED FROM {source_bmp}", file=fout)
print(f"{line_num+10} CALL CLEAR", file=fout)
line_num += 20

for i,c in enumerate(udg):
    print(f'{line_num} CALL CHAR({i+first_char}, "', end="", file=fout)
    for t in c:
        print(f"{t:02X}",end="", file=fout)
    print('")', file=fout)
    line_num += 10

# Next output all characters.
# We take advantage of the fact that the very first character is used most.
print(f"{line_num} CALL HCHAR(1,1,{first_char}, 768)", file=fout)
print(f"{line_num+10} GOTO {line_num+100}", file=fout)
# Subroutine to convert from printable characters to el weirdo
sub = line_num+20
print(f"{line_num+20} FOR I=1 TO LEN(A$)", file=fout)
print(f"{line_num+30} CALL HCHAR(Y, X+I-1, ASC(SEG$(A$,I,1))+50)", file=fout)
print(f"{line_num+40} NEXT I", file=fout)
print(f"{line_num+50} RETURN", file=fout)
line_num += 100

def flush_string(x : int, y : int, m : str):
    global line_num
    if len(m) == 0:
        return
    print(f"{line_num} X={x}", file=fout)
    print(f"{line_num+10} Y={y}", file=fout)
    print(f'{line_num+20} A$="{m}"', file=fout)
    print(f'{line_num+30} GOSUB {sub}', file=fout)
    line_num += 40
    

# Construct strings for other parts of the screen
# Start for parts where the char in question is not first_char i.e. the default
w = width >> 3
for y in range(height >> 3):
    k = ""
    sx = -1
    for x in range(w):
        if charmap[ y*w + x] == first_char:
            flush_string(sx+1, y+1, k)
            k=""
            sx = -1
            continue
        if sx == -1:
            sx = x # save X coordinate
        k += chr(charmap[y*w+x]-50)    # add to string
    # end of x loop, flush if we have something in k
    flush_string(sx+1, y+1, k)

line_num += 100
print(f"{line_num} GOTO {line_num}", file=fout)
fout.close()
