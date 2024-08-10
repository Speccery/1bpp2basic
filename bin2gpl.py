# bin2gpl.py
# A program to convert a binary file into a GPL file which can be used in a GPL program.
# Primary use case is to embed assembly code into a GPL program.
# EP 2024-07-28
#

import argparse
import datetime

def read_bin(name):
    # Be ready to compare with system rom
    romf=open(name, "rb")
    romdata = romf.read(1024)
    romf.close()    
    return romdata

def save_as_gpl(filename : str, romdata, label : str, lenlabel : str):
    fout = open(filename, "wt")
    print(f"* bin2gpl.py output to {filename}", file = fout)
    print(f"* {datetime.datetime.now().ctime()}", file = fout)
    print("* Binary data", file=fout)
    print(f"{label}:", file=fout)
    rom16 = [(romdata[2*x] << 8) | romdata[2*x+1] for x in range(len(romdata) // 2)]
    for d in rom16:
        print(f"  DATA >{d:04x}", file=fout)
    print(f"{lenlabel} EQU >{len(rom):02X}   ; {len(rom)}", file=fout)   
    print(file=fout) 
    fout.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="bin2gpl.py Binary to GPL code")
    parser.add_argument('--maxlen', type=int, help='Maximum length of binary data. Useful to ensure fitting in scratchpad.', default=32)
    parser.add_argument('--label', type=str, default="BINDATA", help="Name of label for data.")
    parser.add_argument('--lenlabel', type=str, help="Name of EQU for length of data", default="BINLEN")
    parser.add_argument('src_name', help = "Name of binary source file")
    parser.add_argument('dest_name', help = 'Name of destination GPL file')
    a = parser.parse_args()
    rom = read_bin(a.src_name)
    if len(rom) > a.maxlen:
        print(f"error: File length {len(rom)} exceeds given maximum {a.maxlen}")
        exit(5)
    save_as_gpl(a.dest_name, rom, a.label, a.lenlabel)
    # rom16 = [(rom[2*x] << 8) | rom[2*x+1] for x in range(len(rom)// 2)]
    # for d in rom16:
    #     print(f"  DATA >{d:04x}")
    # print(f"BINLEN EQU >{len(rom):02X}   ; {len(rom)}")

