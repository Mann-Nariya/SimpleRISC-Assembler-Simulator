import sys
#initialising the flags for different error cases
error_a,error_b,error_c,error_d,error_e,error_f,error_g,error_h,error_i=0,0,0,0,0,0,0,0,0
error_count=0

#functions for printing the different types of machine codes sepereated by their types
def Fn_A(i):
    s=(Type_A[i[0]])
    s+='00'
    s+=register[i[1]]
    s+=register[i[2]]
    s+=register[i[3]]
    s+='\n'
    sys.stdout.write(s)


def Fn_B(i):
    s=(Type_B[i[0]])
    s+='0'
    s+=register[i[1]]
    p=i[2]
    p=p[1:]
    s+=format(int(p),'07b')
    s+='\n'
    sys.stdout.write(s)

def Fn_C(i):
    s=(Type_C[i[0]])
    s+='00000'
    s+=register[i[1]]
    s+=register[i[2]]
    s+='\n'
    sys.stdout.write(s)


def Fn_D(i):
    s=(Type_D[i[0]])
    s+='0'
    s+=register[i[1]]
    s+=variable['var'][i[2]]
    s+='\n'
    sys.stdout.write(s)


def Fn_E(i):
    s=(Type_E[i[0]])
    s+='0000'
    s+=new_label[i[1]]
    s+='\n'
    sys.stdout.write(s)


def Fn_F(i):
    s=(Type_F[i[0]])
    s+='00000000000'
    s+='\n'
    sys.stdout.write(s)


#main program
# f=open("stdin.txt")
assemb_prg=[]
# for i in f.readlines():
#     words=i.strip().split()
#     assemb_prg.append(words)
for kx in sys.stdin:
    words=kx.strip().split()
    assemb_prg.append(words)   



#removing the empty elements of the program given
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)

variable={}
var=[]




#assemb_prg is a 2-D list containing all the words of the progaram seperated as seperate words
for inst in assemb_prg:
    if inst[0]=='var':
        if "var" in variable:
            variable["var"].append(inst[1])
        else:
            variable["var"]=[inst[1]]
            assemb_prg
    else:
        break
#checking for error of type G


# if len(variable) == 0:
#     error_g=1
#     error_count+=1
#     print("Variables not declared at the beginning")
#     exit()

#var is a 2-D list having variables inside the second list
for j in variable.values():
    var.append(j)
if len(variable)==0:
    pass
else:
    variable_dict = {var: i for i, var in enumerate(variable['var'])}
    variable['var'] = variable_dict

#converting all the variables in the list to None
for i,j in variable.items():
    for var in range(len(j)):
        assemb_prg[var]=None

#removing all the none in the program
i=0
while(i<len(assemb_prg)):
    if None in assemb_prg:
        assemb_prg.remove(None)
    i+=1

#checking for error of type G

for i in assemb_prg:
    if i[0]=='var':
        error_g=1

#assigning the addrersses to the variables
for k in variable.values():
    for i,j in k.items():
        k[i]=format(len(assemb_prg)+j,'07b')

label={}
c=0

#removing the halt_label: form the assemb_prg 
#+ checking for the error of type_H
error_h=1
for i in assemb_prg:
    for j in i:
        if j=='hlt':
            error_h=0
            break
    if ':' in i[0]:
        label[i[0]]=format(assemb_prg.index(i),'07b')
        i.remove(i[0])

if(error_h==1):
    error_count+=1

#assigning the address to the hlt statement
new_label = {}
for k, v in label.items():
    new_label[k.rstrip(':')] = v

#removing label
for i in assemb_prg:
    if i==[]:
        assemb_prg.remove(i)
        
#checking for the error of type_i
if assemb_prg[-1][-1]!="hlt":
    error_i=1
    error_count+=1

Type_A={"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100"}
Type_B={"mov":"00010","rs":"01000","ls":"01001"}
Type_C={"mov":"00011","div":"00111","not":"01101","cmp":"01110"}
Type_D={"ld":"00100","st":"00101"}
Type_E={"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"}
Type_F={"hlt":"11010"}

register={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}



#checking for the error of type E
for i in assemb_prg:
    if i[0] in Type_B:
        temp_e=i[2][1:]
        if temp_e.isdigit()==False:
            pass
        elif int(temp_e)>=128:
            error_e=1
            error_count+=1

#checking for error of type A
def detect_typo(assemb_prg):          
    inst_name = ["add" , "sub" , "mul" , "xor" , "or" , "and" , "mov" , "div" , "not" , "cmp" , "ld" , "st" , "jmp" , "jlt" , "jgt" , "je" , "hlt"]
    reg_name = ["R0" , "R1" ,"R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
    isError = False
    for i in assemb_prg:           #i -> instruction
        if i[0] not in inst_name:
            isError = True
        
        for r in i[1:]:  
                if 'var' not in r:
                    if 'label' not in r:
                            if '$' not in r:
                                if "R" in r:
                                    if r not in reg_name:
                                        isError = True   
               
    return isError 

if detect_typo(assemb_prg) == True:
    error_a = 1
    error_count += 1

#checking for error of type B

def detect_undefined_var(assemb_prg):
    isError = False
    for i in assemb_prg:
        if i[0]=='st' or i[0]== 'ld':
            if i[2] not in variable['var'].keys():
                isError=True
                       #print the error message           
    return isError  

if detect_undefined_var(assemb_prg) == True:
    error_b = 1
    error_count += 1

#checking for error of type C
def detect_undefined_label(assemb_prg):             
    labels = set(new_label.keys())
    isError = False
    for i in assemb_prg:
        if i[0] in ["jmp", "jlt", "jgt", "je"]:
            if i[1] not in labels:
                isError = True
            elif 'label' in label:
                isError = True
    return isError
                
if detect_undefined_label(assemb_prg) == True:
    error_c = 1
    error_count += 1 


#checking for error of type D``
def detect_illegal_flags(assemb_prg):          
    isIllegal = False

    for i in assemb_prg:
        if i[0] in ["add", "sub", "mul", "xor", "or", "and", "div", "not", "cmp"]:
            for j in i[1:]:
                if j == "FLAGS":
                    isIllegal = True
    
    return isIllegal

if detect_illegal_flags(assemb_prg) == True:
    error_d = 1
    error_count += 1

#checking of error of type_F

def Error_f(assemb_prg):
    isError=False
    for i in assemb_prg:
        if i[0] in ["jmp", "jlt", "jgt", "je"]:
            if len(i)<2:
                isError=-1
            elif len(i)>2:
                isError=1
        if i[0] in  ["mov" , "div" , "not" , "cmp" , "ld" , "st" ]:
            if len(i)<3:
                isError = -1
            elif len(i)>3:
                isError=1
        if i[0] in ["add" , "sub" , "mul" , "xor" , "or" , "and"]:
            if len(i)<4:
                isError=-1
            elif len(i)>4:
                isError=1
    
    return isError


error_f=Error_f(assemb_prg)
if error_f!=0:
    error_count+=1

# f1=open('stdout.txt','w')
#handeling errors because of different flags that could be raised because of possible errors
if(error_count>=1):
    if(error_b==1):
        sys.stdout.write("Use of undefined variables\n")
    if(error_c==1):
        sys.stdout.write("Use of undefined labels\n")
    if(error_d==1):
        sys.stdout.write("Illegal use of FLAGS register\n")
    if(error_e==1):
        sys.stdout.write("Illegal Immediate values (more than 7 bits)\n")
    if(error_f==-1):
        sys.stdout.write("Incomplete Parameters\n")
    if(error_f==1):
        sys.stdout.write("Extra Parameters\n")
    if(error_h==1):
        sys.stdout.write("Missing hlt instruction\n")
    if(error_i==1):
        sys.stdout.write("hlt not being used as the last instruction\n")
    elif (error_a==1):
        sys.stdout.write("Typo in instruction name or register name\n")
    exit()        
# elif(error_count>1):
#     print("General Syntax Error")
#     exit()


#printing the machine code by calling different functions

for i in assemb_prg:
    if i[0] == 'mov':
        if '$' in i[2]:
            Fn_B(i)
        else:
            Fn_C(i)
    else:
        if i[0] in Type_A.keys():
            Fn_A(i)
        elif i[0] in Type_B:
            Fn_B(i)
        elif i[0] in Type_C:
            Fn_C(i)
        elif i[0] in Type_D:
            Fn_D(i)
        elif i[0] in Type_E:
            Fn_E(i)
        elif i[0] in Type_F:
            Fn_F(i)
