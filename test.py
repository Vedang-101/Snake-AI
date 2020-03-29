class a(object):
    def __init__(self):
        self.a = 10
        self.b = 2
    def show(self):
        print(self.a)
        print(self.b)

s = a()
s.a = 0
b = s
b.a = 9
b.show()
s.show()
