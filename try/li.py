
class AA(object):
    tt= ''

class BB(AA):
    class mm(object):
        name = 'hello'
    def __init__(self):
        print('hello')

yy = BB()