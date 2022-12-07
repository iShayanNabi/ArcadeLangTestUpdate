from Menu import *
import os
import sys
import re


def statement(st):# Help with statment 
    st = st.strip()

    if not st:
        return
    
    regex_intialWord = re.findall("^[a-zA-Z_]* ", st)

    if not regex_intialWord:
        raise Exception("Invalid Syntax")
    
    initalWord = regex_intialWord[0].strip()

    if initalWord in  datatypes :
        said(st)

    elif initalWord == XP['RESTART']:
        loop(st)

    elif initalWord == XP['CHECK']:
        condition(st)

    elif initalWord in stack:
        stated(st)

    else:
        raise Exception(f'{initalWord} n/a')


def stated(st): #Process Stated
   
    rmatch = re.findall("([^;]+);(.*)", st.strip())

    assignStatement = rmatch[0][0]
    restStatement = rmatch[0][1]

    variable, expr = assignStatement.split("=")

    variable = variable.strip()
    expr = expr.strip()

    stack[variable][1] = expression(expr)
    statement(restStatement.strip())

def condition(st): #Process COnditional 
    st = st.replace("Check ", "", 1)

    [booleanStatement, restStatement] = insideBrackets(st, XP["OP"], XP["CP"])
    [insideStatement, restStatement] = insideBrackets(restStatement.strip(), XP["CODEBLOCKSTART"], XP["CODEBLOCKEND"])

    if booleanEquation(booleanStatement):
        statement(insideStatement)

    statement(restStatement)

def loop(st): #Process Loop 
    
    st = st.replace("Restart ", "", 1).strip()
    [boolStatement, restStatement] = insideBrackets(st, XP["OP"], XP["CP"])
    [ifStatement, restStatement] = insideBrackets(restStatement.strip(), XP["CODEBLOCKSTART"], XP["CODEBLOCKEND"])

    while True:
        if booleanEquation(boolStatement):
            statement(ifStatement)
        else:
            break
    
    statement(restStatement)

def said(st): #Process Said 
    rmatch = re.split("([^;]+);(.*)", st.strip())
    
    stStatement = rmatch[1]
    restStatement = rmatch[2]
    

    vType, variable = stStatement.split(" ")

    vType = vType.strip()
    variable = variable.strip()

    if variable in stack:
        raise Exception("{} exist".format(variable))

    stack[variable] = [vType, None]
    statement(restStatement.strip())

def main():
       
    text = open('Test.Arcade', 'r', encoding='utf-8').read()# read  file 
    text = text.replace("\n", " ")
    text = re.sub('\s+', " ", text)
    text = re.findall(r'Go (.*) Stop', text)[0]# From Start and End 
    statement(text)
    print(stack)

main()
