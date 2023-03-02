class A:
    def __init__(self):
        self.a = 123

    def afunc(self):
        self.a = 234

class B:

    def __init__(self):
        self.b = 456
        self.a = "A"

    def bfunc(self):
        self.b  = 567

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)

c = C()
print(c.a)
print(c.b)
c.afunc()
c.bfunc()
print(c.a,c.b)