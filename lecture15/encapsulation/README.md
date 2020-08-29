# Lecture 15 Problem 2

Consider the program [encapsulation.cpp](encapsulation.cpp):

```cxx
#include <stdio.h>

class Rectangle {
public:
    float length;
    float width;
};

class Circle {
public:
    float radius;
};

float rectangle_perimeter(Rectangle *r) {
    return 2.0 * (r->length + r->width);
}

float circle_circumference(Circle *c) {
    return 2.0 * 3.14 * c->radius;
}

int main(int argc, char **argv) {
    Rectangle r;
    Circle c;

    r.length = 10;
    r.width = 20;

    c.radius = 1;

    printf("Rectangle l: %f, w: %f, perimeter: %f\n",
            r.length, r.width, rectangle_perimeter(&r));
    printf("Circle r: %f, circumference: %f\n",
            c.radius, circle_circumference(&c));
    return 0;
}
```

All variable members of both classes `Rectangle` and `Circle` are public and
can be read/written from outside, as it is the case in `main`,
`rectangle_perimeter` and `circle_circumference`. Apply the principles of
encapsulation and rewrite this program to implement:

- `private` visibility for all class member variables
- constructors
- the transformation of both perimeter/circumference computing functions into
  member methods named `perimeter` for the rectangle and `circumference` for
  the circle
- getter functions for class member variables, named `get_length`,
  `get_radius`, etc.

The expected output is:
```shell
./encapsulation
Rectangle l: 10.000000, w: 20.000000, perimeter: 60.000000
Circle r: 1.000000, circumference: 6.280000
```

To check the correctness of your program, use CS50 [sandbox](sandbox.cs50.io)
or [IDE](ide.cs50.io) and write it in a file named `encapsulation.cpp`. In a
terminal, with that file in the local directory, check with this command:
```shell
check50 -l --log olivierpierre/comp26020-problems/master/lecture15/encapsulation
```
