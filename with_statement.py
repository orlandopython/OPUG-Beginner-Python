#!/usr/bin/python3

# ^ This is called the sha-bang (# sha - ! bang)
#It's used by UNIX to determine the program that should execute a script
#This let's us run this file like "./classdemo.py"
#Running with "python3 classdemo.py" will also work as normal
#It also makes it clear that this file is designed with Python3 in mind

"""
Michael duPont - michael@mdupont.com
Beginning Python: Using the 'with' statement
"""

#Imports should always be at the top of the file
import sys
from contextlib import contextmanager

#This code is going to use file operations
#Since the file won't change, we can declare the file name as a global "constant"
#Technically it's not a constant, but Python requires some extra code to change it
FILENAME = 'example.txt'

##---------------------------------------------------------------------------##

#First off, we're going to start with a basic example of how you might use 'with'
#This function is a fairly standard implementation of writing to a file
#However, it still looks a bit clunky
#Note: this function has a code annotation in it - "txt: str"
def meh_file_write(txt: str):
    """Write a given string to a file (FILENAME)
    """
    #Open the file object in append mode
    fout = open(FILENAME, 'a')
    #We want to put things in a try block in case something happens
    try:
        #Write the text to the file
        fout.write(txt)
    #Whether it worked or not, we want to close our connection to the file
    #We often use 'finally' when we need to clean up our objects
    finally:
        #Close the file so other programs can use it
        fout.close()

#There's a much simpler way to write the code above using 'with'
#It allows us to write shorter code and automatically cleans up for us
def better_file_write(txt: str):
    """Identical to meh_file_write but uses 'with'
    """
    #Open the file object in append mode as the variable 'fout'
    with open(FILENAME, 'a') as fout:
        #Write the text to the file
        fout.write(txt)
    #The file has already been closed for us
    #Note: 'fout' is no longer a variable at this point, only inside the indent

#meh_file_write('This is meh')
#better_file_write('This is better')
#Both of these functions should write the given string to a file

##---------------------------------------------------------------------------##

#Now that we know how to use 'with', let's learn how to support it
#We'll start with a class that shows off the runtime order
class WithClass:
    """A basic print-only class that can be used in a 'with' statement

    The only functions required for it are __enter__ and __exit__
    """

    #The __init__ function runs when the object is made
    #You aren't reuired to make your own, but we will here for the print statement
    def __init__(self):
        """Initialize the class
        """
        print('Initializing class')

    #Static methods don't refer to self and therefore do not need it as a parameter
    @staticmethod
    def print_stuff(stuff: str):
        """Print a given string
        """
        print(stuff)

    def __enter__(self):
        """This class function is called upon entering the code block
        """
        print('Now entering')
        #We return 'self' because it will be the value of " as var_name"
        return self

    def __exit__(self, *_):
        """This class function is called upon exiting the code block
        """
        #The __exit__ function takes more than 'self' as parameters
        #These give info on any errors that were thrown
        #We don't need them, so we discard them with underscores
        print('Now exiting')

def example_with_class():
    with WithClass() as example:
        example.print_stuff('OPUG is awesome!')

#example_with_class()
#We would expect the following output:
#>  Initializing class
#>  Now entering
#>  OPUG is awesome!
#>  Now exiting

##---------------------------------------------------------------------------##

#Here's an example of when you might use __enter__ and __exit__ with a class
#We're going to redirect stdout to a file
#Think of stdout (standard out) as "print in the terminal window"
#Systems also come with stderr (error messages) and stdin (user/process input)
class FileWriterClass:
    """Class which, when called in a 'with' statement, will redirect
    all print statements into a file inside of the code block
    """

    def __init__(self, file_name: str):
        """Init takes the name of the output file
        """
        #We need to make a copy of the system's normal stdout
        #If we don't, we can't restore it later
        self.stdout = sys.stdout
        self.fout = open(file_name, 'a')

    def __enter__(self):
        """Set stdout to the file upon entering the code block
        """
        sys.stdout = self.fout

    def __exit__(self, *_):
        """Close the file and restore the normal system stdout
        """
        self.fout.close()
        sys.stdout = self.stdout


def example_file_writer_class():
    print('Goes to console')
    with FileWriterClass(FILENAME):
        print('Now into file')
    print('Back to console')

#example_file_writer_class()
#We would expect the following output:
#>  Goes to console
#Writes 'Now into file' to file object
#>  Back to console

##---------------------------------------------------------------------------##

#We've seen how to use classes in a 'with' statement
#However, you don't always need or want the overhead of a class
#We can use the contextmanager decorator to give functions the same ability
@contextmanager
def with_cmanager():
    """Print-only function that can be used in a 'with' statement
    """
    #Anything before 'yield' is run before entering the code block
    #This is essentially the __enter__ function of a class
    print('Now entering')
    yield
    #Anything after 'yield' is run after the code block (__exit__)
    print('Now exiting')

def example_with_cmanager():
    with with_cmanager():
        print('OPUG is awesome!')

#example_with_cmanager()
#We would expect the following output:
#>  Now entering
#>  OPUG is awesome!
#>  Now exiting

#Using this method, we are able to offer the same functionality with far less code

##---------------------------------------------------------------------------##

#Now that we know how to use contextmanager, let's rewrite our FileWriterClass
#Arguably, this is a much better way to implement it since we aren't extending a class
@contextmanager
def file_writer_cmanager(file_name: str):
    """Functionally identical to FileWriterClass but implemented as a function
    """
    #We're going to combine __init__ and __enter__ here
    #Any variables that we make before the 'yield' are available after it
    #However, they are not available to the code inside the code block
    stdout = sys.stdout
    fout = open(file_name, 'a')
    sys.stdout = fout
    yield
    #Now we provide the __exit__ clean up
    fout.close()
    sys.stdout = stdout

def example_file_writer_cmanager():
    """Runs identically to example_file_writer_class but using a function
    """
    print('Goes to console')
    with file_writer_cmanager(FILENAME):
        print('Now into file')
    print('Back to console')

#example_file_writer_cmanager()
#We would expect the following output:
#>  Goes to console
#Writes 'Now into file' to file object
#>  Back to console

##---------------------------------------------------------------------------##

"""In case you're wondering when this might be useful, here's something from
a shipped program I made using it. It lives in a web page class and pauses
the code after performing some action until the new page has finished loading.

@contextmanager
def wait_for_load(self, timeout: int=60) -> 'generator-with':
    '''Wait until a new page has finished loading in the same window'''
    old_page = self.driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(self.driver, timeout).until(staleness_of(old_page))

And here's how it would be used in context

with self.wait_for_load():
    button.click()
"""
