
def convert(rgb):
    """
    rgb=(255,0,0)
    """
    out=''
    for i in rgb:
        tmp=hex(i)[2:]
        if len(tmp)==1:
            tmp='0'+tmp
        out+=tmp
    return '#'+out


print(convert( (255,0,0) ))
print(convert( (0,139,139)) )

    