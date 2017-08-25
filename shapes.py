"""
Michael duPont - michael@mdupont.com
Orlando Python: Beginners Series

Examples of class structure, inheritance, and usage
"""

from math import sqrt, pi

class Shape(object):
    """A shape object"""

    sides: int = 0

    def __init__(self, x: int, y: int):
        """Init a shape with coordinates"""
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """The representation of the class object"""
        return f'A {self.__class__.__name__} at ({self.x}, {self.y})'

    def distance(self, shape: 'Shape') -> float:
        """Returns the distance between this and a given shapes"""
        x1, y1 = self.x, self.y
        x2, y2 = shape.x, shape.y
        dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return dist

    @property
    def area(self) -> float:
        """The area of the shape. Must be implemented by child class"""
        raise NotImplementedError()

    @staticmethod
    def hello(name: str):
        """Say hello to a given name. Static methods can be used without init"""
        print(f'Hello, {name}')

class Triangle(Shape):
    """A Triangle"""

    sides: int = 3

    @property
    def area(self) -> float:
        """Area of the Triangle"""
        return self.side_length ** 2 * sqrt(3) / 4

class Square(Shape):
    """A Square"""

    sides: int = 4

    def __init__(self, x: int, y: int, side_length: float):
        super().__init__(x, y)
        self.side_length = side_length

    @property
    def area(self) -> float:
        """Area of the Square"""
        return self.side_length ** 2

class Circle(Shape):
    """A Circle"""

    def __init__(self, x: int, y: int, radius: float):
        super().__init__(x, y)
        self.radius = radius

    @property
    def area(self) -> float:
        """Area of the Circle"""
        return pi * self.radius ** 2

# This code will only execute if this file is run directly
if __name__ == '__main__':
    ashape = Triangle(1, 2)
    bshape = Triangle(3, 4)
    print(ashape)
    print(bshape)
    print(ashape.distance(bshape))

    for shape in (Square(1, 2, 4), Circle(4, 8, 1.1)):
        print(shape)
        print(shape.sides)
        print(shape.area)

    tri = Triangle(0, 0)
    print(Triangle.hello('Pythonista'))
