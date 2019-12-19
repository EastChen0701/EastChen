import os
import re
import sys
import argparse
import struct
import shutil
import subprocess
import platform


def main():
    BcPath = "C:\\\"Program Files (x86)\"\\\"Beyond Compare 3\"\\BCompare.exe"
    parser = argparse.ArgumentParser()
    parser.add_argument("ProjectFolder", help="Project A")
    parser.add_argument("ProjectFolder2", help="Project B")
    args = parser.parse_args()
    folder1 = args.ProjectFolder+"\\BUILD\\"
    folder2 = args.ProjectFolder2+"\\BUILD\\"
    #Token1 = folder1+ "\\BUILD\\Token"
    #Token2 = folder2+ "\\BUILD\\Token"



    FileName1 = folder1 + "Token.h"
    FileName2 = folder2 + "Token.h"
    OutFileName1 = folder1 + "Token_sort.h"
    OutFileName2 = folder2 + "Token_sort.h"
    
    CompareTokenH(FileName1,FileName2, OutFileName1, OutFileName2)

    CommndString = BcPath+" "+FileName1+" "+FileName2
    process = subprocess.Popen(CommndString, shell=True)


    FileName1 = folder1 + "Token.mak"
    FileName2 = folder2 + "Token.mak"
    OutFileName1 = folder1 + "Token_sort.mak"
    OutFileName2 = folder2 + "Token_sort.mak"
    
    CompareTokenMak(FileName1,FileName2, OutFileName1, OutFileName2)

    # useing this method, we can launch EXE tool and didn't waiting for tool finish.
    CommndString = BcPath+" "+FileName1+" "+FileName2
    process = subprocess.Popen(CommndString, shell=True)




def CompareTokenH(FileName1, FileName2, OutFileName1, OutFileName2):
    MyItemList = []
    PreProcessTokenH(FileName1, MyItemList)
    OutputFIle(OutFileName1, MyItemList)
    MyItemList = []
    PreProcessTokenH(FileName2, MyItemList)
    OutputFIle(OutFileName2, MyItemList)


def CompareTokenMak(FileName1, FileName2, OutFileName1, OutFileName2):
    MyItemList = []
    PreProcessTokenMak(FileName1, MyItemList)
    OutputFIle(OutFileName1, MyItemList)
    MyItemList = []
    PreProcessTokenMak(FileName2, MyItemList)
    OutputFIle(OutFileName2, MyItemList)

def CheckMultiLine(String):
    mString = String.rstrip()
    if len(mString) > 0 and mString[len(mString)-1] == "\\" :
        return 1
    else:
        return 0
    
def OutputFIle(Filename, ItemList):
    TheFile = open (Filename, 'w')
    TheFile.writelines(ItemList)
    TheFile.close()
    
#################################################################
#
#   For Token.mak
#
#   This function can keep header and return sorted result.
#
#################################################################
def PreProcessTokenMak(Filename, ItemList ):
    Header = 1
    ElinkCase = 0
    HeaderString = ""
    TheFile = open (Filename, 'r')
    
    for line in iter(TheFile):

        if (line[0] == '#' or len(line.rstrip()) == 0) and  Header == 1:
            HeaderString = HeaderString +line
            continue
        
        if ElinkCase == 1:
            ItemList[len(ItemList)-1]=ItemList[len(ItemList)-1]+line
            ElinkCase = CheckMultiLine(line)
            if ElinkCase == 0:
                ItemList[len(ItemList)-1]=ItemList[len(ItemList)-1]+"\n"
            continue
        if "=" in line:
            Header = 0;
            ItemList.append(line)
            ElinkCase = CheckMultiLine(line)
            
    ItemList.sort()
    ItemList.insert(0,HeaderString )
                
    TheFile.close()


#################################################################
#
#   For Token.h
#
#   This function need to keep header and footer
#
#   return sorted result.
#
#################################################################
def PreProcessTokenH(Filename, ItemList ):
    
    HeaderString = ""
    FooterString = ""
    PhaseFlag = 0  # 0: header     1: data     2: footer

    TheFile = open (Filename, 'r')
    
    for line in iter(TheFile):
        if (line.find("//") == 0 or len(line.rstrip()) == 0) or line.find("#if") == 0 or line.find("_TOKEN_SDL_H") != -1  :
            if PhaseFlag == 0:
                HeaderString = HeaderString +line
                continue
            elif PhaseFlag == 2:
                FooterString = FooterString +line
                continue
            
        if "#define" in line:
            PhaseFlag = 1;
            ItemList.append(line)
            
        if "#endif" in line:
            PhaseFlag = 2;
            FooterString = FooterString +line
            
    ItemList.sort()
    ItemList.append(FooterString )
    ItemList.insert(0,HeaderString )
    
    
    TheFile.close()



if __name__ == '__main__':
    sys.exit(main())   


