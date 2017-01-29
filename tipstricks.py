from multiprocessing import Pool
from random import randint
from time import sleep
from timeit import Timer

def formatted_strings():
    """Special string formatting including new Py3.6 formatted strings"""
    crazy_num = 13/11
    print(crazy_num)
    print('{:.3f}'.format(crazy_num))
    
    name = 'Michael'
    print(f'Hello there, {name}')

def number_underscores():
    """Demo how to use and print _ separators to improve number readability"""

    #These two are the same number, but the underscores make it easier to read
    print(1000000000000000000)
    print(1_000_000_000_000_000_000)

    #This also works with hex values
    print(0x_FF_FF_FF_FF)
    print(0b0110_0101)

    #We can use string formatting to add in the underscores as well
    print('{:_}'.format(1000000000000000000))
    print('{:_b}'.format(0b01100001))

def with_example():
    """Demos how to configure a class to be used in a 'with' statement"""
    class WithEx():

        my_var: Dict[str, int] = None
        def __enter__(self):
            print('Enter')
            return self
        def __exit__(self, *_):
            print('Exit')

    with WithEx() as we:
        print(we)
        print('Inside')

def print_to_file():
    """Demos how to use the print statement to send text to a file"""

    #The normal print statement sends text to the console
    print('Prints to console')

    #Opening a file is robust but not always necessary
    with open('test.txt', 'w') as fout:
        fout.write('Writes to file')
    
    #Using print with the 'file' kwarg can handle the most common logging situations
    print('\nPrints to file (append)', file=open('test.txt', 'a'))

def use_annotations():
    """Demos how to use variable (Py3.6) and function (Py3.0) annotations"""

    #Inline variable annotations are new as of Py3.6
    my_ints: List[int] = [1, 2, 3]

    #Vars can be annotated without being given an initial value (not declared)
    my_int: int
    #print(my_int) <- Causes "referenced before assignment" error
    my_int = 0

    #Type annotations are not enforced by stdlib
    my_dict: Dict[str, int] = {}
    my_dict[1.45] = None

    #Function annotations make your existing code much more readable
    def foo(bar: str,
            stew: 'Could be int or None'=None
            ) -> {str: [str]}:
        val: List[str] = [bar] * stew if stew is not None else [bar]
        return {bar: val}
    print('foo("hi", 4) =>', foo('hi', 4))
    print('Annotations:', foo.__annotations__)

def random_wait(val: int):
    """Wait between .1 and .5 seconds to print a given number"""
    sleep(randint(1, 5)/10)
    print(val)

def no_pooling():
    """Process 10 random_wait calls sequentially"""
    def seq():
        for i in range(10):
            random_wait(i)
    t = Timer(lambda: seq())
    print('{:.5f} seconds'.format(t.timeit(number=1)))

def use_pooling():
    """Process 10 random_wait calls 5 at a time"""
    def pooled():
        with Pool(5) as pool:
            pool.map(random_wait, range(10))
    t = Timer(lambda: pooled())
    print('{:.5f} seconds'.format(t.timeit(number=1)))

def memoization():
    """Demo how to save values to improve program performance"""

    #Create a memoization table to store values and a function to store them
    memo_table = {}
    def grab_data(key: str) -> int:
        """"""
        if key not in memo_table:
            memo_table[key] = randint(0, 100)
            sleep(2)
        return memo_table[key]
    
    #Now we can request values and have them stored for faster lookup later
    print('These initial requests will take some time')
    print('a:', grab_data('a'))
    print('b:', grab_data('b'))

    print('These requests should be instantaneous')
    print('a:', grab_data('a'))
    print('b:', grab_data('b'))

def dict_from_lists():
    """Demo creating dictionary objects"""
    
    #Lets say we have two lists that we want to turn into a dict
    keys = ['a', 'b', 'c']
    values = [1, 2, 3]
    #We'll first turn them into key-value pairs using zip()
    print(list(zip(keys, values)))
    #The dict object can accept a list of key-value pairs
    my_dict = dict(zip(keys, values))
    print(my_dict)

    #Just to prove this is true, we can run this assert
    assert(my_dict == dict(zip(my_dict.keys(), my_dict.values())))

def equals():
    """Demos equivilence for use in 'if' statements"""

    #All of these values are evaluated to be True
    if True and 1 and -1 and 2.34 and 'foo' and [1, 2, 3] and {'a': 1}:
        print('All True')
    #All of these values are evaluated to be False
    if not (False or None or 0 or 0.0 or '' or [] or {}):
        print('All False')

    if 'thing':
        print('Non-empty objects work')
    if not []:
        print("Empty objects don't")

def use_decorators():
    """Demos how to make a use decorators"""

    #Create a function that takes and returns a function
    def in_and_out(func):
        """Prints 'in' and 'out' around the executing function"""
        def wrapper(*args, **kwargs):
            print('In')
            output = func(*args, **kwargs)
            print('Out')
            return output
        return wrapper
    
    #The function gets placed here and is given the function defined below it
    @in_and_out
    def foo(val: int):
        print('Executing')
        return ['bar'] * val
    
    print(foo(1))
    print()
    print(foo(3))
            
#Functions callable by index
funcs = [
    formatted_strings,
    number_underscores,
    with_example,
    print_to_file,
    use_annotations,
    no_pooling,
    use_pooling,
    memoization,
    dict_from_lists,
    equals,
    use_decorators
]    

import begin
@begin.start
def main(code_block: 'Index of desired function'):
    """Run a desired block of example code"""
    func = funcs[int(code_block)]
    print(func.__doc__)
    func()
