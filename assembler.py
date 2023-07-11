from sys import stdin
import sys
def findop(a,typeis):
    ins = a[0]
    if(typeis == "A"):
        if(ins == "add"):
            return("00000")
        if(ins == "sub"):
            return("00001")
        if(ins == "mul"):
            return("00110")
        if(ins == "xor"):
            return("01010")
        if(ins == "or"):
            return("01011")
        if(ins == "and"):
            return("01100")
    elif(typeis == "B"):
        if(ins == "mov"):
            return("00010")
        if(ins == "rs"):
            return("01000")
        if(ins == "ls"):
            return("01001")
    elif(typeis == "C"):
        if(ins == "mov"):
            return("00011")
        if(ins == "div"):
            return("00111")
        if(ins == "not"):
            return("01101")
        if(ins == "cmp"):
            return("01110")
    elif(typeis == "D"):
        if(ins == "ld"):
            return("00100")
        if(ins == "st"):
            return("00101")
    elif(typeis == "E"):
        if(ins == "jmp"):
            return("01111")
        if(ins == "jlt"):
            return("10000")
        if(ins == "jgt"):
            return("10001")
        if(ins == "je"):
            return("10011")
    elif(typeis == "F"):
        if(ins == "hlt"):
            return("10011")
    else:
        return("WRONG INSTRUCTION IN LINE ")

def findtype(a):
    ins = a[0]
    if(ins == "add" or ins == "sub" or ins == "mul" or ins == "xor" or ins == "or" or ins == "and"):
        return("A")
    elif((ins == "mov" and a[2][0] == "$") or ins == "rs" or ins == "ls"):
        return("B")
    elif(ins == "mov" or ins == "div" or ins == "not" or ins == "cmp"):
        return("C")
    elif(ins == "ld" or ins == "st"):
        return("D")
    elif(ins == "jmp" or ins == "jlt" or ins == "jgt" or ins == "je"):
        return("E")
    elif(ins == "hlt"):
        return("F")
    return("WRONG INSTRUCTION IN LINE ")

def regbin(c):
    data = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
    if c in data.keys():
        return(data[c])
    else:
        return ("WRONG REGISTOR NAME IN LINE ")

def immbin(c):
    return str(format(int(c),'08b')) 

    


b = []
a = []
var = []
varop = {}
label={}
l = 0


for line in stdin:
    if line == "": #if empty line no more input
        break
    while line[0] == " ":
        line = line[1:]
    a = line.split(" ")
    if a[-1] != "hlt":
      a[-1]=a[-1][:-1]
    if a[0][-1]==":":  #find label,save binary, remove label
        a[0] = a[0][:-1]
        label[a[0]] = immbin(str(l))
        a.pop(0)
    if len(a)==0:
        sys.stdout.write("EMPTY LABEL")
        quit()

    if a[0] == "var": #find variable save variable in list 
        if(l>0): 
            print("VARIABLE DECLARED IN BETWEEN CODE IN LINE "+ str(l))
            quit()
        var.append(a[1])
        continue
    b.append(a)
    l = l + 1

for a in b[:len(b)-1]:
    if a[0] == "hlt": 
        print("hlt IS IN BETWEEN LINE IN LINE "+ str(l))
        quit()

if b[-1][-1] != "hlt": 
    print("NO hlt")
    quit()

if len(var)>0:
    for i in var:
        varop[i] = immbin(l)
        l=l+1
i = 0
for a in b :
    i = i + 1
    typeis = findtype(a)
    if typeis == "WRONG INSTRUCTION IN LINE ":
        sys.stdout.write(typeis + str(i))
        quit()
    opis = findop(a,typeis)
    if opis == "WRONG INSTRUCTION IN LINE ":
        sys.stdout.write(typeis + str(i))
        quit()
    if(typeis == "A"):
        x = regbin(a[1])
        y = regbin(a[2])
        z = regbin(a[3])
        binary = opis + "00" + x + y + z
        if x == "WRONG INSTRUCTION in line":
            sys.stdout.write(x + str(i))
            quit()
        if y == "WRONG INSTRUCTION in line":
            sys.stdout.write(y + str(i))
            quit()
        if z == "WRONG INSTRUCTION in line":
            sys.stdout.write(z + str(i))
            quit()
    elif(typeis == "B"):
        x = regbin(a[1])
        y = immbin(a[2][1:])
        binary = opis + x + y
        if x == "WRONG INSTRUCTION IN LINE ":
            sys.stdout.write(x + str(i))
            quit()
        if int(a[2][1:]) > 255:
            sys.stdout.write("ILLEGAL VALUE IN LINE " + str(i)) 
        if int(a[2][1:]) < 0:
            sys.stdout.write("ILLEGAL VALUE IN LINE " + str(i))
    elif(typeis == "C"):
        x = regbin(a[1])
        y = regbin(a[2])
        binary = opis + "00000" + x + y
        if x == "WRONG INSTRUCTION IN LINE ":
            sys.stdout.write(x + str(i))
        if y == "WRONG INSTRUCTION IN LINE ":
            sys.stdout.write(y + str(i))
    elif(typeis == "D"):
        x = regbin(a[1])
        y = varop[a[2]] 
        binary = opis + regbin(a[1]) + varop[a[2]]
        if x == "WRONG INSTRUCTION IN LINE ":
            sys.stdout.write(x + str(i))
    elif(typeis == "E"):
        binary = opis + "000" + label[a[1]]
    elif(typeis == "F"):
        binary = opis + "00000000000" 
    sys.stdout.write(binary)
    sys.stdout.write("\n")