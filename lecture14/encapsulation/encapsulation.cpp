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
