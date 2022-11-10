#Here goes some tests

def testkw(**kw):
    print(kw['n'])


dict = {'hi':'fun', 'n':1}
testkw(**dict)