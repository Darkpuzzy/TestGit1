import time


def add_func(func):
    def _wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result + 1
    return _wrapper


@add_func
def logger(a, b):
    return a + b

print(logger(1, 2))


class Someone:

    def __init__(self, name, lastname):
        self.name = name
        self.lname = lastname

    def who(self):
        return f'Name is {self.name} and Lname is {self.lname}'

# someone = Someone(name='Nick', lastname= 'Zhirko')


class Theysome(Someone):
    def __init__(self, name, lastname, pay):
        self.pay = pay
        super().__init__(name, lastname)

    def payday(self):
        return f'{self.name} pay is {self.pay}'


ths = Theysome(name='Mark', lastname='Jebryk', pay='15000')


class Personal:

    def __init__(self, name, lname, tax, dec, yo):
        self.name = name
        self._lname = lname
        self.tax = tax
        self.dec = dec
        self.yo = yo

    @property
    def infor(self):
        return f'PERSONAL CARD:\nFULL NAME:{self.name} {self._lname}\nYEARS: {self.yo}'

    @infor.setter
    def infor(self, name, lname, yo):
        self.name = name
        self._lname = lname
        self.yo = yo

    def full_info(self):
        full_name = self.name + ' ' + self._lname
        return f'PERSONAL CARD A WORKER:\nFULL NAME:{full_name}\nYEARS: {self.yo}\nTAX: {self.tax}'


prs = Personal(
    name='Mark', lname='Chadson', tax='30000', yo='32', dec='1'
)

print('___________________INFO_______________')
print(prs.infor)
print(prs.full_info())
print('__________________CHANGED______________')
prs.yo = '29'
print(prs.infor)

