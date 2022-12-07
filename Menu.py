import re
from typing import Union


stack = {}
datatypes = {"MINI", "NORMAL", "PRO", "PROMAX"}
XP = { #Token 
    'ASSIGN': "=",
    'STOP': "Stop",
    'GO': "Go",
    'CHECK': "Check",
    'RESTART': "Restart",
    'ADDITION': "+",
    'SUBTRACTION': "-",
    'MULTIPLICATION': "*",
    'DIVISION': "/",
    'MODULUS': "%",
    'FLOORRDIV': "$",
    'GreaterThan': ">",
    'LessThan': "<",
    'GreaterThanEqual': ">=",
    'LessThanEqual': "<=",
    'Equal': "==",
    'NotEqual': "!=",
    'OP': "(",
    'CP': ")",
    'CODEBLOCKSTART': "{",
    'CODEBLOCKEND': "}",
}

def booleanEquation(equation): #Evaluate Equation for Boolean 
    
    operators = [XP["LessThan"], XP["GreaterThan"], XP["GreaterThanEqual"], XP["LessThanEqual"], XP["Equal"], XP["NotEqual"]]

    for i in range(0, len(operators)):
        
        hasXP = f' {operators[i]} ' in equation

        if not hasXP:
            continue

        expression1, expression2 = equation.split(operators[i])

        value1 = expression(expression1)
        value2 = expression(expression2)

        Coin = operators[i]

        if Coin == operators[0]:
            return value1 < value2
        
        if Coin == operators[1]:
            return value1 > value2
        
        if Coin == operators[2]:
            return value1 >= value2
        
        if Coin == operators[3]:
            return value1 <= value2
        
        if Coin == operators[4]:
            return value1 == value2
        
        if Coin == operators[5]:
            return value1 != value2

    raise Exception("Invalid Boolean")



class BN:

    val: Union[str,int]

    def __init__(self, val = "") -> None:
        self.right = None
        self.left = None
        self.val = val


def indexPairBracket(st, startBracket, endBracket, startIndex): #Helper to find bracket 
    bracketCounter = 1
    currentIndex = startIndex + 1
    while bracketCounter > 0:
        if currentIndex >= len(st):
            raise Exception("Invalid Expression")
        if st[currentIndex] == startBracket:
            bracketCounter = bracketCounter + 1
        elif st[currentIndex] == endBracket:
            bracketCounter = bracketCounter - 1
        
        currentIndex = currentIndex + 1
    return currentIndex

def inParenthesis(exp):
    if exp[0] != XP["OP"]: #Helper to find in parenthesis 
        return False
    val = indexPairBracket(exp, XP["OP"], XP["CP"], 0)
    return val >= len(exp)

def tree(exp, node: BN):
    
    exp = exp.strip()

    if inParenthesis(exp):
        exp = exp[1:len(exp)-1]

    if not exp:
        raise Exception("Invalid Expression")

    if len(exp) == 0:
        return 

    if exp.isnumeric():
        node.val = int(exp)
        return

    temp = exp

    index_addition = None;
    index_subtraction = None;
    index_multiplication = None;
    index_division = None;
    index_modulus = None;

    i = 0 
    while i < len(temp):
        if temp[i] == XP["OP"]:
            i = indexPairBracket(temp, XP["OP"], XP["CP"],i)
        elif temp[i-1:i+2] == f' {XP["ADDITION"]} ':
            index_addition = i
        elif temp[i-1:i+2] == f' {XP["SUBTRACTION"]} ':
            index_subtraction = i
        elif temp[i-1:i+2] == f' {XP["MULTIPLICATION"]} ':
            index_multiplication = i
        elif temp[i-1:i+2] == f' {XP["DIVISION"]} ':
            index_division = i
        elif temp[i-1:i+2] == f' {XP["MODULUS"]} ':
            index_modulus = i
        i = i + 1

    
    if index_addition or index_subtraction or index_multiplication or index_division:
        node.left = BN("")
        node.right = BN("")
    else:
        if  exp not in stack or stack[exp][1] == None:
            raise Exception("Vairable missing")
        
        if stack[exp] != None:
            node.val = stack[exp][1]
        return 

    if index_subtraction:
        node.val = XP["SUBTRACTION"]
        tree(exp[0:index_subtraction], node.left)
        tree(exp[index_subtraction+2:], node.right)
        return 

    if index_addition:
        node.val = XP["ADDITION"]
        tree(exp[0:index_addition], node.left)
        tree(exp[index_addition+2:], node.right)
        return 

    if index_multiplication:
        node.val = XP["MULTIPLICATION"]
        tree(exp[0:index_multiplication], node.left)
        tree(exp[index_multiplication+2:], node.right)
        return 
   
    if index_division:
        node.val = XP["DIVISION"]
        tree(exp[0:index_division], node.left)
        tree(exp[index_division+2:], node.right)
        return 
    
    if index_modulus:
        node.val = XP["MODULUS"]
        tree(exp[0:index_modulus], node.left)
        tree(exp[index_modulus+2:], node.right)
        return 
    
    


def DT(node: BN): # Math Solver 
    if not node:
        return 0
    
    if type(node.val) is int:
        return node.val
    
    if node.val == XP["MULTIPLICATION"]:
        return DT(node.left) * DT(node.right)
    elif node.val == XP["SUBTRACTION"]:
        return DT(node.left) - DT(node.right)
    elif node.val == XP["ADDITION"]:
        return DT(node.left) + DT(node.right)
    elif node.val == XP["DIVISION"]:
        return int(DT(node.left) / DT(node.right))
    elif node.val == XP["MODULUS"]:
        return int(DT(node.left) % DT(node.right))


def expression(exp:str): #Help with expression 
    exp = exp.strip()
    
    root = BN()

    tree(exp, root)
    return DT(root)

def insideBrackets(statement, startBracket, endBracket):#Inside Bracket 
    
    bracketCounter = 1
    currentIndex = 1

    while bracketCounter > 0 :
        if statement[currentIndex] == startBracket:
            bracketCounter += 1
        elif statement[currentIndex] == endBracket:
            bracketCounter -= 1

        currentIndex += 1
    
    return [statement[1:currentIndex-1], statement[currentIndex:]]

