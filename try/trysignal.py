from heStruct.heSignal import connect,reciver,fire

@reciver('dog_bite')
def t1():
    print('i m t1')

def t3():
    print('i m t3')

def t2():
    print('in to t2')
    fire('dog_bite')
    print('out t2')

connect('dog_bite',t3)

t2()

