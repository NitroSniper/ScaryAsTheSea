from inspect import getfullargspec
def aMethod(arg1, arg2): pass
print(inspect.getfullargspec(aMethod))
def foo(a,b,c=4, *arglist, **keywords): pass
print(inspect.getfullargspec(foo).args)



name =0
hello = 1
pineapple = 9
alist = [name, hello, pineapple]
print (alist)
alist[0] = 1
print (alist)
print (name)



def getName(hello):
    return f'{foo=}'.split('=')[0]
print (getName(hello))
print (getattr(object, 'name'))