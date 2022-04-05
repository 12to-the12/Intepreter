










co_consts = (None, 0, 35, False, 10, 'whats ya guess laddie?', 1, 'too low', 'too high', True, 'you got it!', 'you lost, better luck next time!')

co_names = ('int', 'input', 'print')#global variable names
co_varnames = ('guessed', 'num', 'won', 'guess')#local variable names
var_values = {
    'int':int,
    'input':input,
    'num' :35,
    'print' :print,
    'guessed':0,
    'won':False
    }

def value(varname):
    return var_values[ varname ]
cmp_op = ['<',1,2,3,'>']
program_pointer = 0
data_stack = []
opcodes = {}
    
print(co_varnames[0])
code =\
"""  4           0 LOAD_CONST               1 (0)
              2 STORE_FAST               0 (guessed)

  5           4 LOAD_CONST               2 (35)
              6 STORE_FAST               1 (num)

  6           8 LOAD_CONST               3 (False)
             10 STORE_FAST               2 (won)

  7     >>   12 LOAD_FAST                0 (guessed)
             14 LOAD_CONST               4 (10)
             16 COMPARE_OP               0 (<)
             18 POP_JUMP_IF_FALSE       86
             20 LOAD_FAST                2 (won)
             22 POP_JUMP_IF_TRUE        86

  8          24 LOAD_GLOBAL              0 (int)
             26 LOAD_GLOBAL              1 (input)
             28 LOAD_CONST               5 ('whats ya guess laddie?')
             30 CALL_FUNCTION            1
             32 CALL_FUNCTION            1
             34 STORE_FAST               3 (guess)

  9          36 LOAD_FAST                0 (guessed)
             38 LOAD_CONST               6 (1)
             40 INPLACE_ADD
             42 STORE_FAST               0 (guessed)

 10          44 LOAD_FAST                3 (guess)
             46 LOAD_FAST                1 (num)
             48 COMPARE_OP               0 (<)
             50 POP_JUMP_IF_FALSE       62

 11          52 LOAD_GLOBAL              2 (print)
             54 LOAD_CONST               7 ('too low')
             56 CALL_FUNCTION            1
             58 POP_TOP
             60 JUMP_ABSOLUTE           12

 12     >>   62 LOAD_FAST                3 (guess)
             64 LOAD_FAST                1 (num)
             66 COMPARE_OP               4 (>)
             68 POP_JUMP_IF_FALSE       80

 13          70 LOAD_GLOBAL              2 (print)
             72 LOAD_CONST               8 ('too high')
             74 CALL_FUNCTION            1
             76 POP_TOP
             78 JUMP_ABSOLUTE           12

 15     >>   80 LOAD_CONST               9 (True)
             82 STORE_FAST               2 (won)
             84 JUMP_ABSOLUTE           12

 16     >>   86 LOAD_FAST                2 (won)
             88 POP_JUMP_IF_FALSE      100
             90 LOAD_GLOBAL              2 (print)
             92 LOAD_CONST              10 ('you got it!')
             94 CALL_FUNCTION            1
             96 POP_TOP
             98 JUMP_FORWARD             8 (to 108)

 17     >>  100 LOAD_GLOBAL              2 (print)
            102 LOAD_CONST              11 ('you lost, better luck next time!')
            104 CALL_FUNCTION            1
            106 POP_TOP
        >>  108 LOAD_CONST               0 (None)
            110 RETURN_VALUE"""


code = code.replace('\n\n','\n')
code = code.split('\n')
for line in code:
    print(line)
code = [e[13:] for e in code]#takes the first 13 characters off each line
code = [e[3:] for e in code]

#for line in code:
#    print(line)

code = [e.split() for e in code]# this crazy line takes each line of bytecode and splits it by whitespace

new_code = []
for line in code:#the indexes count by twos to make room for the args i think
    new_code.append(line)
    new_code.append([])
code = new_code

#for i in code:
#    print(i)

def pop():
    return data_stack.pop()
def push(data):
    data_stack.append(data)


def run_funct(funct, args):#*args
    #print('im inside the run funct function!')
    #print('args[0] is', args[0])
    #print('funct is',funct)
    push( funct(args[0]) )


#opcodes['']
def LOAD_CONST (target):
    push(  co_consts[target]  )
opcodes['LOAD_CONST'] = LOAD_CONST


def LOAD_FAST (target):
    #print('TROUBLESHOOTING')
    #print(type(target ))
    #print(target)
    #print(  co_varnames  )
    push(  value(    co_varnames[target]  )   )
opcodes['LOAD_FAST'] = LOAD_FAST


def LOAD_GLOBAL (target):
    #print(type(target ))
    #print (target)
    #print (  co_names[target]  )
    push(  value(  co_names[target]    ) )
opcodes['LOAD_GLOBAL'] = LOAD_GLOBAL


def STORE_FAST (target):
    var_values  [  co_varnames[target]  ] = pop()
opcodes['STORE_FAST'] = STORE_FAST


def STORE_GLOBAL (target):
    pass
    #target = pop()
opcodes['LOAD_GLOBAL'] = LOAD_GLOBAL


def POP_JUMP_IF_TRUE (target):
    global program_pointer
    #print('Inside POP_JUMP_IF_TRUE')
    #print('target is',target)
    #print(data_stack)
    info = pop()
    #print(info)
    #print('x')
    #print(info=='True')
    #info = info=='True'
    #print(info)
    if info:
        #print('it actuated')
        program_pointer = target -2 #the minus two because it will be auto incremented
opcodes['POP_JUMP_IF_TRUE'] = POP_JUMP_IF_TRUE


def POP_JUMP_IF_FALSE (target):
    global program_pointer
    #print('Inside POP_JUMP_IF_FALSE')
    #print('target is',target)
    #print(data_stack)
    #info = pop()=='True'
    info = pop()
    #print(info)
    if not info:
        #print('it actuated')
        program_pointer = target -2 #the minus two because it will be auto incremented
opcodes['POP_JUMP_IF_FALSE'] = POP_JUMP_IF_FALSE


def COMPARE_OP (target):
    OP = cmp_op[target]
    b = int(pop()  )
    a = int(pop()  )
    value = False
    if OP == '==':
        if a == b:
            value = True
    if OP == '<':
        if a < b:
            value = True
    if OP == '>':
        if a > b:
            value = True
    if OP == '<=':
        if a <= b:
            value = True
    if OP == '>=':
        if a >= b:
            value = True
    if OP == '!=':
        if a != b:
            value = True
    push(value)
           
opcodes['COMPARE_OP'] = COMPARE_OP


def CALL_FUNCTION (target):
    arguments = []
    for i in range(target):
        arguments.append(  pop()  )
    run_funct(  pop(), arguments  )
opcodes['CALL_FUNCTION'] = CALL_FUNCTION


def INPLACE_ADD (target):
    b = int(pop()  )
    a = int(pop()  )
    push( str(a + b) )
opcodes['INPLACE_ADD'] = INPLACE_ADD


def JUMP_ABSOLUTE (target):
    global program_pointer
    program_pointer = target - 2 # the minus two because the counter is always incremented two
opcodes['JUMP_ABSOLUTE'] = JUMP_ABSOLUTE


def POP_TOP (target):
    pop()
opcodes['POP_TOP'] = POP_TOP


def JUMP_FORWARD (target):
    global program_pointer
    #print('program_pointer:',program_pointer)
    #print('target:',target)
    #print('should end up at',program_pointer+target-2+2)
    program_pointer += target #nvm- 2 # the minus two because the counter is always incremented two
opcodes['JUMP_FORWARD'] = JUMP_FORWARD

def RETURN_VALUE (target):
    pass
opcodes['RETURN_VALUE'] = RETURN_VALUE

#print(code)
print(len(code))
while program_pointer<=len(code)-2:

    #print('co_varnames:', co_varnames)
    #print('co_names:', co_names)
    #print('program_pointer:',program_pointer)
    WORD = code[program_pointer]
    #print('WORD:',WORD)
    #print(type(WORD))
   
   
    OPCODE = WORD[0]
    #print(OPCODE)
    try:
       target = WORD[1]
    except:
       target = 0
    #print('target:',target)
    target = int(target)
   
    opcodes[OPCODE](target)

    '''
    print()
    print('data_stack:')
    
    print()
    for item in data_stack:
        print(data_stack.index(item),':',item)
    '''
    #print('\n'*1)
    program_pointer += 2

"""4           0 LOAD_CONST               1 (0)
              2 STORE_FAST               0 (guessed)

  5           4 LOAD_CONST               2 (35)
              6 STORE_FAST               1 (num)

  6           8 LOAD_CONST               3 (False)
             10 STORE_FAST               2 (won)

  7     >>   12 LOAD_FAST                0 (guessed)
             14 LOAD_CONST               4 (10)
             16 COMPARE_OP               0 (<)
             18 POP_JUMP_IF_FALSE       86
             20 LOAD_FAST                2 (won)
             22 POP_JUMP_IF_TRUE        86

  8          24 LOAD_GLOBAL              0 (int)
             26 LOAD_GLOBAL              1 (input)
             28 LOAD_CONST               5 ('whats ya guess laddie?')
             30 CALL_FUNCTION            1
             32 CALL_FUNCTION            1
             34 STORE_FAST               3 (guess)

  9          36 LOAD_FAST                0 (guessed)
             38 LOAD_CONST               6 (1)
             40 INPLACE_ADD
             42 STORE_FAST               0 (guessed)

 10          44 LOAD_FAST                3 (guess)
             46 LOAD_FAST                1 (num)
             48 COMPARE_OP               0 (<)
             50 POP_JUMP_IF_FALSE       62

 11          52 LOAD_GLOBAL              2 (print)
             54 LOAD_CONST               7 ('too low')
             56 CALL_FUNCTION            1
             58 POP_TOP
             60 JUMP_ABSOLUTE           12

 12     >>   62 LOAD_FAST                3 (guess)
             64 LOAD_FAST                1 (num)
             66 COMPARE_OP               4 (>)
             68 POP_JUMP_IF_FALSE       80

 13          70 LOAD_GLOBAL              2 (print)
             72 LOAD_CONST               8 ('too high')
             74 CALL_FUNCTION            1
             76 POP_TOP
             78 JUMP_ABSOLUTE           12

 15     >>   80 LOAD_CONST               9 (True)
             82 STORE_FAST               2 (won)
             84 JUMP_ABSOLUTE           12

 16     >>   86 LOAD_FAST                2 (won)
             88 POP_JUMP_IF_FALSE      100
             90 LOAD_GLOBAL              2 (print)
             92 LOAD_CONST              10 ('you got it!')
             94 CALL_FUNCTION            1
             96 POP_TOP
             98 JUMP_FORWARD             8 (to 108)

 17     >>  100 LOAD_GLOBAL              2 (print)
            102 LOAD_CONST              11 ('you lost, better luck next time!')
            104 CALL_FUNCTION            1
            106 POP_TOP
        >>  108 LOAD_CONST               0 (None)
            110 RETURN_VALUE
"""
