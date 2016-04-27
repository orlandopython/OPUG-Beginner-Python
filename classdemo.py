#!/usr/bin/python3

# ^ This is called the sha-bang (# sha - ! bang)
#It's used by UNIX to determine the program that should execute a script
#This let's us run this file like "./classdemo.py"
#Running with "python3 classdemo.py" will also work as normal
#It also makes it clear that this file is designed with Python3 in mind

##--Michael duPont - michael@mdupont.com
##--Beginning Python: Making Classes

#Let's start by making a new Person class
#Every class inherits methods from the base object class in Python
#This includes an initializer (__init__) and "toString" method (__str__)
class Person():
    '''A base Person class with a first and last name'''
    #We use strings without a variable to describe our classes and methods
    #Many IDEs interpret these strings as the object's documentation
    
    #This is called when a new object is created, ex: Person('Bob', 'Jones')
    #All non-static methods must use "self" as its first variable, and
    #"self" does not need to be declared when calling the function
    def __init__(self, firstName, lastName):
        '''Initialize the Person with their first and last name'''
        #self is what we use to set or refer to variables and methods
        #within its own class, similar to "this" in other languages
        self.first = firstName
        self.last = lastName
    
    def greet(self):
        '''Prints a greeting with the person's name'''
        print('Hello', self.first, self.last)
    
    #We use decorators (the @ syntax) to specify static methods
    #Note that the method definition does not use "self"
    @staticmethod
    def reminder():
        '''Prints a reminder for the person'''
        print("YOU'RE AWESOME")
    
    #Normally, printing an object looks like this:
    #<Person object at 0x7f4fcb8705c0> <= last part is location in memory
    #We want to overwrite the default print method to something more useful
    def __str__(self):
        '''Returns a print string of "last, first"'''
        return "{}, {}".format(self.last, self.first)

#We're going to extend our Person class by calling it in the class definition
class Student(Person):
    '''Student extends Person but also has a grade'''
    
    #Like methods, we can set properties in the class without using "self"
    #"self" is only required inside method definitions
    #We use an underscore (_) at the start of private properties and methods
    #Technically, there's no such thing as private in Python as you can still
    #change them directly, but they are not callable by any child classes
    _grade = None
    
    def __str__(self):
        '''Extends the Person print string'''
        #super() makes a direct call to the parent class
        #Here we run the parent's str method and add to its result
        return super().__str__() + ' (Student)'
    
    #We can make getter methods by using the property decorator
    #We are creating a property called obj.grade whose value is calculated
    #This is used in place of making a getGrade() method
    @property
    def grade(self):
        '''Getter for the letter grade of the student'''
        if not self._grade:
            return None
        elif self._grade > 89:
            return 'A'
        elif 89 >= self._grade > 79:
            return 'B'
        elif 79 >= self._grade > 69:
            return 'C'
        elif 69 >= self._grade > 64:
            return 'D'
        else:
            return 'F'
    
    #One big advantage to using properties with getter/setter is type checking
    #For the setter, we use a decorator with the property name and .setter
    @grade.setter
    def grade(self, num):
        '''Setter for grade which checks that the value is an int'''
        #We use isinstance to check if types match
        #It is more versitile and forgiving than using type(num) == int
        if isinstance(num, int):
            self._grade = num
        else:
            print('Requires an int')

class ClassRoom():
    '''Classroom which has a name and a list of students'''
    _students = []
    
    def __init__(self, name):
        self.name = name
    
    def addStudent(self, student):
        '''Adds a Student to the list of students'''
        #We only want to add if the given object is a Student
        if isinstance(student, Student):
            self._students.append(student)
    
    def gradeClass(self):
        '''Prints out the letter grade for each student in the classroom'''
        print('Grades for {}:'.format(self.name))
        for student in self._students:
            #Because of the work we did in Person and Student,
            #it's really easy to get the info we need
            print('\t', student, student.grade)

#Since our file is itself an object, it has its own properties
#The __name__ property is "__main__" only when called via "python3 myfile.py"
#This if statement prevents our test code from running when imported elsewhere
if __name__ == '__main__':
    me = Person('Michael', 'duPont')
    me.greet()      # => "Hello Michael duPont"
    me.reminder()   # => "YOU'RE AWESOME"
    #Person.reminder() will also will also work because it is a static method
    print(me)       # => "duPont, Michael"

    matt = Student('Matt', 'Smith')
    print(matt)         # => "Smith, Matt (Student)"
    matt.grade = 'fish' # => "Requires an int"
    matt.grade = 85
    print("{}'s grade: {}".format(matt.first, matt.grade))
                        #=> "Matt's grade: B"

    cindy = Student('Cidny', 'Hoo')
    cindy.grade = 92

    room = ClassRoom('CSC100')
    #Oops our coder made a typo
    room.name = 'CSC101'
    #me shouldn't add because it's not a Student
    room.addStudent(me)
    room.addStudent(matt)
    room.addStudent(cindy)
    #Asserts raise an AssertionError if it fails
    assert(len(room._students) == 2)
    room.gradeClass()
    # =>
    #Grades for CSC101:
    #   Smith, Matt (Student) B
    #   Hoo, Cidny (Student) A
