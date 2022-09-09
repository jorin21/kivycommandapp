def sGen(LineNum,Command):
    i = LineNum
    text = Command

    eStr = ''

    for l in range(5):
        if l != i-1 and l != 4:
            eStr += '.\n'
        
        elif l != i-1 and l == 4:
            eStr += '.'

        elif l == i-1 and l == 4:
            eStr += text

        else:
            eStr += f'{text}\n'

    return eStr


