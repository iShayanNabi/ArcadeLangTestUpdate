# ArcadeLangTestUpdate# Lexical Analyzer

## Lexical Rules

Code starts with `Go` and ends with `Stop`. Between the block will have all the statements.

## Types of statements

- Declaration
- Assign
- Condition
- Loop

## Tokens

### Mathematical Operators

| Token Code       | Operation | Regex |
| ---------------- | --------- | ----- |
| ADDITION              | +         | +     |
| SUBTRACTION              | -         | -     |
| MULTIPLICATION              | \*        | \*    |
| DIVISION              | /         | /     |
| MODULUS              | %         | %     |
| OP               | (         | (     |
| CP               | )         | )     |

### Mathematical Equators

| Token Code | Operation | Regex |
| ---------- | --------- | ----- |
| LessThan         | <         | <     |
| GreaterThan         | >         | >     |
| LessThanEqual        | <=        | <=    |
| GreaterThanEqual        | >=        | >=    |
| Equal         | ==        | ==    |
| NotEqual         | !=        | !=    |

### Integer Types

| Token Code | Size    | Literal |
| ---------- | ------- | ------- |
| MINI       | 1 byte  | 1b      |
| NORMAL     | 2 bytes | 2b      |
| PRO        | 4 bytes | 3b      |
| PROMAX     | 8 bytes | 4b      |

### Keyword Types

| Token Code | Regex         |
| ---------- | ------------- |
| VAR        | [a-zA-Z_]{6,8} |
| CHECK      | Check          |
| RESTART    | Restart       |
| GO         | Go            |
| STOP       | Stop          |

### Extras

| Token Code       | Operation | Regex |
| ---------------- | --------- | ----- |
| ASSIGNMENT       | =         | =     |
| CODEBLOCKOPEN    | {         | {     |
| CODEBLOCKCLOSE   | }         | }     |
| OP               | (         | (     |
| CP               | )         | )     |

## Priority Order

- \-
- \+
- \*
- / 
- ()

## Production Rules

```txt

<Program> --> Begin <stmt_list> End
<stmt_list> --> {<stmt> `;`}
<stmt> --> <if_stmt> | <while_stmt> | <as_s>  | <declaration>
<if_stmt> --> Check  `(` <bool> `)` `{` <stmt_list> `}`
<while_stmt> --> Restart `(` <bool> `)` `{` <stmt_list> `}`
<as_s> --> <var> = <expression> `;`
<declaration> --> <datatype> <var> `;`

<datatype> --> (MINI|NORMAL|PRO|PROMAX)
<var> -->  [a-zA-Z_]{6,8} // Restrictions
<expression> --> <term> { (`*`|`\`| '%' ) <term> }
<term> --> <term> { (`+`|`-`) <term> }
<factor> --> [0-9]+ | <var>  | `(` <expression> `)`
<bool> --> <expression> (`<=`|`>=` | `<` | `>`) <expression>


```

## Grammar Rules

```txt

E -> E + T           Expression + Term
E -> E - T           Expression - Term
E -> T               Expresions can sometimes be Term
T -> T * F           Term * Expression
T -> T / F           Term / Expression
T -> F               Term can be a Factor
F -> -F              Unary Minus Factor
F -> +F              Unary Plus Factor
F ->( E )            Factor can be an Expression inside a parenthese
F -> s               Factor can be Constant

```

## Is it a LL Grammar? 

The code works on LR Grammar aswell as LL Grammar. It has pairwise disjoint. Go and Stop is one code section. Datatype is a Decleration, Variable is a assigment statment, Restart is a loop statment, Check is a Condition statment. This is LR when an expression tree is constructed and being solved.

## Is it Ambiguous Grammar? 

The LR table would have turned red incase of any ambiguity, the action block would have the highlight portion. 
If you scroll down to the end you can see the images. 

## Program

To run the program in VS Code run "python JoyStick.py"

## Working and failing 

### Failing Case

```txt

Go

  MINI var1X;
  varX = 6 - (2 + (2 * 10))

  check (varX != 20) {
    varX = 16;
    }

  NOMAL varXx;
  varXx = var1X + 6
  }

Stop

```

Errors:

- var1X. Lexical Error**, can't have numbers in variable name. Correct varX
- (2 * 10). Syntax Error, parantheses should be have a space. 
- NOMAL. Is a Semantic Error, data type is not valid. Correct NORMAL
- check. Is supposed to be Check. Correct Check
- {. Syntax Error. Missing opening bracket.

```txt

Go

  PRO varY;
  varY = 10*-2;

  Check(varY != 0){
    varY = -20;

  ProMax varX;

  varX = -20 + 40 * varY

Stop

```

Error:

- varX. Semantic Error. varX n/a in stack.
- 10*-2. Syntax Error, need to be separated by a space.
- ProMax. **Lexical Error**, all characters need to be capitalized. Correct PROMAX
- }. Syntax Error, Check needs to end with }.
- varY. Lexical Error, doesn't follow the var regex. 

### Working Code

```txt

Go 
    MINI var;
    var = 3 - (4 * 2);

    Check (var < 5){
        var = var + 1;
    }
Stop

```

```txt

Go

    PROMAX varX;
    varOne = 10 * 10 - 1;

    MINI varY;
    varY = 8;

    PRO varXx;

    Check (varY < varX){
        varXx = 12;
    }
Stop

```

## LR(1) Grammar and parse tree 

### LR(1) Grammar/Parse Table

![Grammar table](https://raw.githubusercontent.com/iShayanNabi/ArcadeLangTestUpdate/main/T.JPG)

### Fail I
![Grammar table](https://raw.githubusercontent.com/iShayanNabi/ArcadeLangTestUpdate/main/f1.JPG)

### Pass I
![Grammar table](https://raw.githubusercontent.com/iShayanNabi/ArcadeLangTestUpdate/main/p1.JPG)

### Fail II
![Grammar table](https://raw.githubusercontent.com/iShayanNabi/ArcadeLangTestUpdate/main/f2.JPG)

### Pass II
![Grammar table](https://raw.githubusercontent.com/iShayanNabi/ArcadeLangTestUpdate/main/p2.JPG)
