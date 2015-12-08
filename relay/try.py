import sys

sys.dog =True
print(id(sys.dog))
print(sys.dog==True)
print(id(True))

sys.dog=False
print(id(sys.dog))
print(sys.dog==True)
