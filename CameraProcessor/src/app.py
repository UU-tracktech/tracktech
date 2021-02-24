import numpy as np

class Hello(object):
    def __init__(self, msg):
        self._msg = msg
    
    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, v):
        self._msg = v
    

def main():
    hello = Hello("Hello World")
    print(hello.msg)
    print(3*3)
    print(np.array([2, 3, 4]))

if __name__ == '__main__':
    main()
