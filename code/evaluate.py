# UTILIS


def rindex(lst, val, start=None):
    if start is None:
        start = len(lst)-1
    for i in range(start,-1,-1):
        if lst[i] == val:
            return i


# TOKENS


TOKENS = {
    "LBRACKET": '(',
    "RBRACKET": ')',
    "OPERATOR": '^*/+-',
    "DIGITS": '0123456789.'}

MATH = "().+-*/^0123456789"


# (VALUE, TOKEN)


def lexer(expr):
    bracketCount = 0
    CURRENT_NUMBER = ''
    KEYS = []
    expr = expr.replace(' ', '')
    expr = expr.replace('\n', '')

    for char in expr:
        if char not in MATH: return f'Invalid character {char}'

        for token, content in TOKENS.items():
            if char in content:
                if token == 'DIGITS':
                    CURRENT_NUMBER += char
                else:
                    if CURRENT_NUMBER != '':
                        if CURRENT_NUMBER.count('.') > 1:
                            return 'Invalid expression'
                        KEYS.append((CURRENT_NUMBER, 'NUMBER'))
                        CURRENT_NUMBER = ''
                    if char == '(':
                         bracketCount += 1
                    elif char == ')':
                         bracketCount -= 1
                    KEYS.append((char, token))
    if CURRENT_NUMBER != '':
        KEYS.append((CURRENT_NUMBER, 'NUMBER'))
    if bracketCount != 0:
        return 'Unbalanced ('
    return KEYS


def parser(expr):
    lex = lexer(expr)
    if type(lex) is str:
        return lex
    POS_TOKENS = {"NUMBER": ('OPERATOR', 'RBRACKET'),
                  "RBRACKET": ('OPERATOR', 'RBRACKET')}

    if lex[0][1] not in ('NUMBER', 'LBRACKET') and lex[0][0] not in ['+', '-']:
        return 'Invalid expression'
    if lex[-1][1] not in ('NUMBER', 'RBRACKET'):
        return 'Invalid expression'

    for i in range(0, len(lex)):
        if i < len(lex) - 1:
            if lex[i][1] == 'LBRACKET':
                if lex[i + 1][1] not in ('NUMBER','LBRACKET') and lex[i + 1][0] not in ['+','-']:
                    return 'Invalid syntax'
            elif lex[i][1] == "OPERATOR":
                if lex[i + 1][1] not in ('LBRACKET','NUMBER') and lex[i + 1][0] not in ['+','-']:
                    return 'Invalid syntax'
            else:
                if lex[i + 1][1] not in POS_TOKENS[lex[i][1]]:
                    return 'Invalid syntax'

    for p in range(0, lex.count(('+','OPERATOR')) + lex.count(('-','OPERATOR'))):
        for i in range(0, len(lex)):
            if i < len(lex) - 1:
                if lex[i][0] in ('+','-'):
                    if lex[i+1][1] == 'NUMBER':
                        if lex[i+1][0][0] not in ('+','-'):
                            if i == 0:
                                    temp = (lex[i][0] + lex[i+1][0], 'NUMBER')
                                    lex.insert(0, temp)
                                    for x in range(0,2):
                                        lex.pop(1)
                            else:
                                if lex[i - 1][1] in ('OPERATOR', 'LBRACKET'):
                                    temp = (lex[i][0] + lex[i + 1][0], 'NUMBER')
                                    lex.insert(i, temp)
                                    for x in range(0, 2):
                                        lex.pop(i+1)
                    elif lex[i+1][0] in ('-','+'):
                        if lex[i+1][0][0] == lex[i][0]:
                            final = '+' + lex[i+1][0][1:]
                        else:
                            final = '-' + lex[i+1][0][1:]
                        lex[i+1] = (final,'NUMBER')
                        lex.pop(i)
    return lex


def calc(number1, number2, operator):
    x = float(number1)
    y = float(number2)
    if operator == '+':
        return x + y
    elif operator == '-':
        return x - y
    elif operator == '*':
        return x * y
    elif operator == '/':
        if y == 0.0:
            return 'Division by zero'
        return x / y
    elif operator == '^':
        op = str(x ** y)
        if 'j' in op:
            return 'Invalid expression'
        else:
            return x ** y

def evaluate(expr):
    prs = parser(expr)
    order = (('^','^'),('*','/'),('+','-'))

    if type(prs) is str:
        return prs

    if ('(', 'LBRACKET') in prs:
        for i in range(0, prs.count(('(', 'LBRACKET'))):
            FIRST_BR = prs.index((')', 'RBRACKET'))
            LAST_BR = rindex(prs,('(', 'LBRACKET'),FIRST_BR)

            if FIRST_BR < LAST_BR:
                LAST_BR = prs.index(('(', 'LBRACKET'))

            temp = prs[LAST_BR:FIRST_BR + 1]

            temp.pop(-1)
            temp.pop(0)

            for op in order:
                calcOP = 0

                if (op[0], 'OPERATOR') in temp:
                    calcOP += temp.count((op[0], 'OPERATOR'))
                if (op[1], 'OPERATOR') in temp and op[0] != op[1]:
                    calcOP += temp.count((op[1], 'OPERATOR'))

                if calcOP > 0:
                    for p in range(0,calcOP):
                        okOP = -1
                        if (op[0], 'OPERATOR') in temp:
                            okOP += 1
                        if (op[1], 'OPERATOR') in temp:
                            okOP += 2

                        if okOP == 2:
                            if temp.index((op[0], 'OPERATOR')) < temp.index((op[1], 'OPERATOR')):
                                pos = temp.index((op[0], 'OPERATOR'))
                                cOP = op[0]
                            else:
                                pos = temp.index((op[1], 'OPERATOR'))
                                cOP = op[1]
                        else:
                            pos = temp.index((op[okOP], 'OPERATOR'))
                            cOP = op[okOP]

                        calcu = calc(temp[pos - 1][0], temp[pos + 1][0], cOP)
                        if type(calcu) is str:
                            return calcu

                        temp.insert(pos - 1, (str(calcu), 'NUMBER'))

                        for p in range(0,3):
                            temp.pop(pos)
            prs[LAST_BR:FIRST_BR + 1] = temp
            ex = ''
            for y in prs:
                ex += y[0]
            prs = parser(ex)

    for op in order:
        calcOP = 0

        if (op[0], 'OPERATOR') in prs:
            calcOP += prs.count((op[0], 'OPERATOR'))
        if (op[1], 'OPERATOR') in prs and op[0] != op[1]:
            calcOP += prs.count((op[1], 'OPERATOR'))

        if calcOP > 0:
            for p in range(0, calcOP):
                okOP = -1
                if (op[0], 'OPERATOR') in prs:
                    okOP += 1
                if (op[1], 'OPERATOR') in prs:
                    okOP += 2

                if okOP == 2:
                    if prs.index((op[0], 'OPERATOR')) < prs.index((op[1], 'OPERATOR')):
                        pos = prs.index((op[0], 'OPERATOR'))
                        cOP = op[0]
                    else:
                        pos = prs.index((op[1], 'OPERATOR'))
                        cOP = op[1]
                else:
                    pos = prs.index((op[okOP], 'OPERATOR'))
                    cOP = op[okOP]

                calcu = calc(prs[pos - 1][0], prs[pos + 1][0], cOP)
                if type(calcu) is str:
                    return calcu
                prs.insert(pos - 1,(str(calcu), 'NUMBER'))

                for p in range(0, 3):
                    prs.pop(pos)
        ex = ''
        for y in prs:
            ex += y[0]
        prs = parser(ex)

    return float(prs[0][0])
